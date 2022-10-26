# constants args
ARG DEFAULT_IMAGE_NAME=ptt_backend
ARG DEFAULT_POETRY_VERSION=1.2.1

##############################
# build stage (install libraries)
##############################
FROM python:3.10.8-slim AS build

# recall common arguments
ARG DEFAULT_IMAGE_NAME
ARG DEFAULT_POETRY_VERSION

# set env arg for current build
ENV IMAGE_NAME=${DEFAULT_IMAGE_NAME}
ENV POETRY_VERSION=${DEFAULT_POETRY_VERSION}

RUN mkdir /${IMAGE_NAME}

# required for postgres installation
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*  

# add user and group named as ${IMAGE_NAME}
# not to run pip command as root user
RUN groupadd --gid 500 ${IMAGE_NAME}
RUN useradd \
    --uid 500 \
    --gid 500 \
    --home /${IMAGE_NAME} \
    --shell /bin/bash \
    ${IMAGE_NAME} \
    && chown \
        --recursive \
        ${IMAGE_NAME}:${IMAGE_NAME} \
        /${IMAGE_NAME} \
    && chmod -R g+rwx /${IMAGE_NAME}

# change default user
USER ${IMAGE_NAME}

# set env PATH and PYTHONPATH
ENV PATH="/${IMAGE_NAME}/.local/bin:${PATH}"
ENV PATH /root/.poetry/bin:$PATH
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# upgrade pip
RUN pip install --upgrade pip

WORKDIR /${IMAGE_NAME}

# install poetry and create .venv (--copies uses copies rather than symlinks)
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv --copies .venv \
    && poetry config virtualenvs.path /${IMAGE_NAME}/

# add .venv to PATH to use it as default .venv
ENV PATH /${IMAGE_NAME}/.venv/bin:$PATH

# copy .toml and .lock file and install libraries in .venv
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip \
    && poetry install --only main --no-root

 
##############################
# final stage (copy .venv and codebase)
##############################
FROM python:3.10.8-slim AS final

# recall common arguments
ARG DEFAULT_IMAGE_NAME
ENV IMAGE_NAME=${DEFAULT_IMAGE_NAME}


# additional installations
RUN apt-get update && apt-get install -y \
    vim \
    postgresql-client \
    curl \
 && rm -rf /var/lib/apt/lists/*  
 

# copy .venv form build stage
COPY --from=build /${IMAGE_NAME}/.venv /${IMAGE_NAME}/.venv/
# add .venv to PATH to use it as default .venv
ENV PATH /${IMAGE_NAME}/.venv/bin:$PATH

# copying codebase
WORKDIR /${IMAGE_NAME}

COPY . ./

RUN chmod +x /${IMAGE_NAME}/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]