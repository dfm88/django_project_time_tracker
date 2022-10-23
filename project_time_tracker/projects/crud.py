from dataclasses import dataclass, field

from common.crud import BaseCRUD

from .models import Project


@dataclass
class ProjectCRUD(BaseCRUD):
    model: Project = field(default=Project, init=False)


project_crud = ProjectCRUD()
