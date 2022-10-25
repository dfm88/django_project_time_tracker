from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.urls import path
from django.views.decorators.cache import cache_page

from projects.views import (ProjectHandleUsers, ProjectListCreateApi,
                            ProjectRetrieveUpdateDelete, ProjectStatistics)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    path(
        '',
        cache_page(timeout=CACHE_TTL)(ProjectListCreateApi.as_view()),
        name='list_create__project'
    ),
    path(
        '<int:project_id>',
        cache_page(timeout=CACHE_TTL)(ProjectRetrieveUpdateDelete.as_view()),
        name='retrieve_update_delete__project'
    ),
    path(
        '<int:project_id>/handle_users',
        cache_page(timeout=CACHE_TTL)(ProjectHandleUsers.as_view()),
        name='handle_users__project'
    ),
    path(
        '<int:project_id>/statistics',
        cache_page(timeout=CACHE_TTL)(ProjectStatistics.as_view()),
        name='statistics__project'
    ),
]
