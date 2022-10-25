from dataclasses import dataclass, field

from django.db import models, transaction

from common.crud import BaseCRUD
from projects.models import ProjectAssignment
from time_log.models import TimeLog
from users.models import UserCustom


@dataclass
class TimeLogCRUD(BaseCRUD):
    model: TimeLog = field(default=TimeLog, init=False)

    def get_by(self, **kwargs) -> models.Model:
        try:
            return self.model.objects.prefetch_related(
                'project_assignment'
            ).select_related(
                'project_assignment__project'
            ).get(**kwargs)
        except Exception:
            return super().get_by(**kwargs)

    def get_logs_by_user_project(self, project_id: int, user_id: int) -> models.QuerySet:
        return self.model.objects.filter(
            project_assignment__user=user_id,
            project_assignment__project=project_id
        )

    def get_logs_for_statistics(self, project_id, user: UserCustom = None) -> models.QuerySet:
        """Get all logs by project and optionally by user"""
        user_filter = models.Q()
        if user:
            user_filter = models.Q(project_assignment__user=user)
        return self.model.objects.filter(
            project_assignment__project=project_id,
        ).filter(
            user_filter
        ).exclude(
            end_time__isnull=True
        )

    @transaction.atomic
    def update_time_log(self, time_log_id: int, **data) -> None:
        self.model.objects.filter(
            pk=time_log_id
        ).update(
            **data
        )

    @transaction.atomic
    def create_time_log(self, project_assignment: ProjectAssignment, **data) -> TimeLog:
        time_log_obj: TimeLog = self.model.objects.create(
            project_assignment=project_assignment,
            **data
        )
        time_log_obj.full_clean()
        time_log_obj.save()
        time_log_obj.refresh_from_db()
        return time_log_obj

    def filter_by(self, **kwargs) -> models.QuerySet:
        """Get a queryset based on kwargs

        Returns:
            models.QuerySet
        """
        return self.model.objects.select_related(
            'project_assignment'
        ).select_related(
            'project_assignment__project'
        ).filter(**kwargs)


time_log_crud = TimeLogCRUD()
