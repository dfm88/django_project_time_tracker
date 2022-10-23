from dataclasses import dataclass

from django.db import models
from rest_framework.exceptions import NotFound


@dataclass
class BaseCRUD:
    model: models.Model

    def get_by(self, **kwargs) -> models.Model:
        """Get a model based on kwargs

        Raises:
            NotFound: if object doesn't exists

        Returns:
            models.Model
        """
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise NotFound(f'{self.model.__name__} not found with {kwargs}')

    def get_all(self) -> models.QuerySet:
        return self.model.objects.all()
