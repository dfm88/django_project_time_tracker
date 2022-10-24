from django.urls import path

from projects.views import (ProjectHandleUsers, ProjectListCreateApi,
                            ProjectRetrieveUpdateDelete, ProjectStatistics)

urlpatterns = [
    path(
        '',
        ProjectListCreateApi.as_view(),
        name='list_create__project'
    ),
    path(
        '<int:project_id>',
        ProjectRetrieveUpdateDelete.as_view(),
        name='retrieve_update_delete__project'
    ),
    path(
        '<int:project_id>/handle_users',
        ProjectHandleUsers.as_view(),
        name='handle_users__project'
    ),
    path(
        '<int:project_id>/statistics',
        ProjectStatistics.as_view(),
        name='statistics__project'
    ),
]
