from django.db import models

from common.models import BaseModel
from users.models import UserCustom


class Project(BaseModel):
    name = models.CharField(max_length=32)
    description = models.TextField()
    creator = models.ForeignKey(
        UserCustom,
        on_delete=models.SET_NULL,
        related_name='created_projects',
        null=True,
    )
    assignees = models.ManyToManyField(
        UserCustom,
        related_name='assigned_projects',
        blank=True
    )

    def __str__(self):
        return f'{self.id} - {self.name}'
