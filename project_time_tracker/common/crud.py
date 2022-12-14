from abc import ABC
from dataclasses import dataclass

from django.db import models
from rest_framework.exceptions import NotAcceptable, NotFound


@dataclass
class BaseCRUD(ABC):
    model: models.Model

    def get_by(self, **kwargs) -> models.Model:
        """Get a model based on kwargs

        Raises:
            rest_framework.exceptions.NotFound: if object doesn't exists
            rest_framework.exceptions.NotAcceptable: if multiple objects are returned

        Returns:
            models.Model
        """
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            # rest framework exception so that view will handle the response
            raise NotFound(
                f'{self.model.__name__} not found with {kwargs}'
            )
        except self.model.MultipleObjectsReturned:
            # rest framework exception so that view will handle the response
            raise NotAcceptable(
                f'Found multiple instances of {self.model.__name__} with {kwargs}, use filter_by'
            )

    def get_by_or_none(self, **kwargs) -> models.Model | None:
        """Get a model based on kwargs. Doesn't throw exceptions

        Returns:
            models.Model | None
        """
        try:
            return self.get_by(**kwargs)
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            return None

    def filter_by(self, **kwargs) -> models.QuerySet:
        """Get a queryset based on kwargs

        Returns:
            models.QuerySet
        """
        return self.model.objects.filter(**kwargs)

    def get_all(self) -> models.QuerySet:
        return self.model.objects.all()

    def delete_by(self, **kwargs) -> None:
        instance = self.get_by(**kwargs)
        instance.delete()

    def delete(self, instance: models.Model) -> None:
        instance.delete()
