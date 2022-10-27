import datetime

import factory
from django.utils import timezone

from projects.models import Project, ProjectAssignment
from time_log.models import TimeLog
from users.models import UserCustom

# # BASE FACTORIEs


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"test_proj{n}")
    description = 'test proj'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserCustom
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f"test_user{n+1}")
    password = factory.PostGenerationMethodCall(
        'set_password', 'test'
    )


class AdminFactory(UserFactory):
    class Meta:
        model = UserCustom

    username = 'admin'
    is_staff = True
    is_superuser = True


class ProjectAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectAssignment
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)


class TimeLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeLog
    project_assignment = factory.SubFactory(ProjectAssignmentFactory)


# # COMPLEX FACTORIEs

class TimeLogOnlyStartFactory(TimeLogFactory):
    """
    start_time = '2022-01-01 11:00:00+00:00'
    end_time = None
    """
    class Meta:
        model = TimeLog
    start_time = datetime.datetime(
        year=2022,
        month=1,
        day=1,
        hour=11,
        minute=00,
        tzinfo=timezone.utc
    )


class TimeLogCompleteFactory7h(TimeLogFactory):
    """
    start_time = '2022-02-01 11:00:00+00:00'
    end_time = '2022-02-01 18:00:00+00:00'
    total_work_time = 7
    """
    class Meta:
        model = TimeLog
        exclude = ('total_time',)

    start_time = datetime.datetime(
        year=2022,
        month=2,
        day=1,
        hour=11,
        minute=00,
        tzinfo=timezone.utc
    )

    end_time = datetime.datetime(
        year=2022,
        month=2,
        day=1,
        hour=18,
        minute=00,
        tzinfo=timezone.utc
    )


class TimeLogCompleteFactory3h(TimeLogFactory):
    """
    start_time = '2022-03-01 11:00:00+00:00'
    end_time = '2022-03-01 14:00:00+00:00'
    total_work_time = 3
    """
    class Meta:
        model = TimeLog
        exclude = ('total_time',)

    start_time = datetime.datetime(
        year=2022,
        month=3,
        day=1,
        hour=11,
        minute=00,
        tzinfo=timezone.utc
    )

    end_time = datetime.datetime(
        year=2022,
        month=3,
        day=1,
        hour=14,
        minute=00,
        tzinfo=timezone.utc
    )
