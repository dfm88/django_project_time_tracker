from django.urls import path

from time_log.views import TimeLogListCreateApi, TimeLogRetrieveUpdateDelete

urlpatterns = [
    path(
        '',
        TimeLogListCreateApi.as_view(),
        name='list_create__time_log'
    ),
    path(
        '<int:time_log_id>',
        TimeLogRetrieveUpdateDelete.as_view(),
        name='retrieve_update_delete__time_log'
    ),
]
