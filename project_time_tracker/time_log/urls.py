from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from time_log.views import TimeLogListCreateApi, TimeLogRetrieveUpdateDelete

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    path(
        '',
        cache_page(timeout=CACHE_TTL)(TimeLogListCreateApi.as_view()),
        name='list_create__time_log'
    ),
    path(
        '<int:time_log_id>',
        cache_page(timeout=CACHE_TTL)(TimeLogRetrieveUpdateDelete.as_view()),
        name='retrieve_update_delete__time_log'
    ),
]
