from dataclasses import dataclass, field

from django.db import models, transaction

from common.crud import BaseCRUD
from users.models import UserCustom

from .models import Project, ProjectAssignment


@dataclass
class ProjectCRUD(BaseCRUD):
    model: Project = field(default=Project, init=False)

    def get_projects_per_user_role(self, user: UserCustom) -> models.QuerySet:
        """Return only project assigned to user if is not admin
        else returns all projects

        Args:
            user (UserCustom):

        Returns:
            models.QuerySet
        """
        if user.is_staff:
            return self.get_all()
        return user.assigned_projects.all()

    @transaction.atomic
    def update_project(self, project_id: int, **data) -> None:
        self.model.objects.filter(
            pk=project_id
        ).update(
            **data
        )

    @transaction.atomic
    def create_project(self, creator: UserCustom, **data) -> Project:
        project_obj: Project = self.model.objects.create(
            creator=creator,
            **data
        )
        project_obj.full_clean()
        project_obj.save()
        project_obj.refresh_from_db()
        return project_obj


@dataclass
class ProjectAssignmentCRUD(BaseCRUD):
    model: ProjectAssignment = field(default=ProjectAssignment, init=False)

    def add_users_to_project(
        self,
        project: Project,
        users: models.QuerySet[UserCustom]
    ) -> models.QuerySet:
        project.assignees.set(users)

    def remove_users_from_project(
        self,
        project: Project,
        users: models.QuerySet[UserCustom]
    ) -> models.QuerySet:
        self.filter_by(**{
            'project_id': project.id,
            'user__in': users
        }).delete()


project_crud = ProjectCRUD()
project_assign_crud = ProjectAssignmentCRUD()
