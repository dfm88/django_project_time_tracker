from django.db import models

from common.models import BaseModel
from projects.models import ProjectAssignment


class TimeLog(BaseModel):
    project_assignment = models.ForeignKey(
        ProjectAssignment,
        on_delete=models.CASCADE,
        related_name='logs_list'
    )
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(null=True, blank=True, default=None, db_index=True)

    def clean(self) -> None:
        from time_log.core import ensure_ranges_dont_overlap
        ensure_ranges_dont_overlap(time_log=self)
        return super().clean()

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
        start_time = self.start_time.strftime(format=dt_format)
        end_time = self.end_time and self.end_time.strftime(format=dt_format)
        return (
            f'{self.id} - {self.project_assignment.user.username} - '
            f'{self.project_assignment.project.name} '
            f'{start_time} | '
            f'{end_time}'
        )
