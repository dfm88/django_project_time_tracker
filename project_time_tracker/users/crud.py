from dataclasses import dataclass, field

from django.db import models

from common.crud import BaseCRUD
from users.models import UserCustom


@dataclass
class UserCustomCRUD(BaseCRUD):
    model: UserCustom = field(default=UserCustom, init=False)

    def get_users_from_usernames(self, usernames: list[str]) -> models.QuerySet:
        return self.model.objects.filter(username__in=usernames)


user_crud = UserCustomCRUD()
