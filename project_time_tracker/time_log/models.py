from django.db import models

from common.models import BaseModel
from projects.models import ProjectAssignment


class TimeLog(BaseModel):
    project_assignee = models.ForeignKey(
        ProjectAssignment,
        on_delete=models.CASCADE,
        related_name='logs_list'
    )
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(default=None, db_index=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    end_time__isnull=True) | models.Q(
                        end_time__gte=models.F('start_time')
                ),
                name="End time (when not null) must be grater than Start time",
            )
        ]

    def __str__(self):
        dt_format = r'%Y-%m-%d %H:%M'
        return (
            f'{self.id} - {self.project_assignee.user.username} - '
            f'{self.project_assignee.project.name} '
            f'{self.start_time.strftime(format=dt_format)} | '
            f'{self.start_time.strftime(format=dt_format)}'
        )
