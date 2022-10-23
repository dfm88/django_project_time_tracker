from django.db import models

from common.models import BaseModel
from projects.models import Project
from time_log import core
from users.models import UserCustom


class TimeLog(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(default=None)

    def clean(self):
        core.ensure_log_assigned_project(time_log=self)

    def __str__(self):
        dt_format = r'%Y-%m-%d %H:%M'
        return (
            f'{self.id} - {self.user.username} - {self.project.name} '
            f'{self.start_time.strftime(format=dt_format)} | '
            f'{self.start_time.strftime(format=dt_format)}'
        )
