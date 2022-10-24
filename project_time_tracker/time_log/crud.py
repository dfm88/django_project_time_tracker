from dataclasses import dataclass, field

from common.crud import BaseCRUD
from django.db import models, transaction
from projects.models import ProjectAssignment

from .models import TimeLog


@dataclass
class TimeLogCRUD(BaseCRUD):
    model: TimeLog = field(default=TimeLog, init=False)

    def get_logs_by_project(self, project_id: int) -> models.QuerySet:
        return self.model.objects.filter(project_assignment__project=project_id)

    @transaction.atomic
    def update_time_log(self, time_log_id: int, **data) -> TimeLog:
        pass

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


time_log_crud = TimeLogCRUD()
