from dataclasses import dataclass, field

from common.mixins import ObjectFromIdMixin
from projects.crud import ProjectCRUD, project_crud


@dataclass
class ProjectFromIdMixin(ObjectFromIdMixin):
    crud_instance: ProjectCRUD = field(default=project_crud)
    lookup_name: str = 'project_id'
    injection_name: str = 'project'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)


@dataclass
class ProjectIdQueryStringMixin(ProjectFromIdMixin):
    required: bool = True
    required_error_msg: str = 'project_id query param is required'

    def initial(self, request, *args, **kwargs):
        """
        Raises:
            ParseError: if query_param `project_id` was not passed
        """
        project_id = self.request.query_params.get('project_id')
        kwargs['project_id'] = project_id
        super().initial(request, *args, **kwargs)
