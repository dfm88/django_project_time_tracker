from django.db import models


class BaseCRUD:

    def __init__(self, model: models.Model):
        self.model = model

    def get_by(self, **kwargs) -> models.Model | None:
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def get_all(self) -> models.QuerySet:
        return self.model.objects.all()
