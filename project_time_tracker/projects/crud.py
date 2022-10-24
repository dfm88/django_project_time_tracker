from dataclasses import dataclass, field

from common.crud import BaseCRUD

from .models import Project, ProjectAssignment


@dataclass
class ProjectCRUD(BaseCRUD):
    model: Project = field(default=Project, init=False)


@dataclass
class ProjectAssignmentCRUD(BaseCRUD):
    model: ProjectAssignment = field(default=ProjectAssignment, init=False)


project_crud = ProjectCRUD()
project_assign_crud = ProjectAssignmentCRUD()
