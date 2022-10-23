from dataclasses import dataclass, field
from django.db import models
from common.crud import BaseCRUD

from .models import TimeLog


@dataclass
class TimeLogCRUD(BaseCRUD):
    model: TimeLog = field(default=TimeLog, init=False)

    def get_logs_by_project(self, project_id: int) -> models.QuerySet:
        return self.model.objects.filter(project_assignee__project=project_id)


time_log_crud = TimeLogCRUD()
