import logging
import sys

from django.core.management.base import BaseCommand
from projects.models import Project

from users.models import UserCustom

logger = logging.getLogger(__name__)


class MockUsersManager:
    @staticmethod
    def create_user(username, password, superuser: bool = False):
        if superuser and not UserCustom.objects.filter(username=username).exists():
            user = UserCustom.objects.create_superuser(username=username, password=password)
        else:
            user, _ = UserCustom.objects.get_or_create(username=username)
            user.set_password(password)
            user.save()
        logger.info(f"creating mock {'super' if superuser else ''}user {username}")
        return user


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            for i in range(15):
                username = f"user_{i+1}"
                password = "Passw0rd!"
                MockUsersManager.create_user(username=username, password=password)
            admin = MockUsersManager.create_user(
                username='admin',
                password=password,
                superuser=True
            )

            for i in range(3):
                proj_name = f"project_{i+1}"
                logger.info(f"creating mock project {proj_name}")
                project, _ = Project.objects.get_or_create(
                    name=proj_name,
                    description=proj_name,
                    creator=admin
                )
                if i != 2:
                    logger.info(f'Assigning project {proj_name} to users from user_{i*5+1} to user_{i*5+5}')
                    project.assignees.set(UserCustom.objects.order_by('date_joined').all()[(i * 5):(i + 1) * 5])

        except Exception as ex:
            logger.exception(ex)
            sys.exit(1)
