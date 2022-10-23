from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAssignedToProjectOrAdmin
from projects.crud import project_crud

from time_log.crud import time_log_crud
from time_log.permissions import IsLogOwner
from time_log.serializers import TimeLogSerializer


class TimeLogApiViewMixin:
    """Override `initial` method of ApiVIEW"""
    def initial(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        super().initial(request, *args, **kwargs)
        project_id = self.request.query_params.get('project_id')
        if not project_id:
            raise ParseError('project_id query param is required')


class TimeLogListCreateApi(TimeLogApiViewMixin, APIView):

    permission_classes = (IsAssignedToProjectOrAdmin,)

    def get(self, request):
        project_id = request.query_params['project_id']
        proj = project_crud.get_by(pk=project_id)
        # checks that user belongs to project
        self.check_object_permissions(request, proj)
        time_logs = time_log_crud.get_logs_by_project(project_id=project_id)
        data = TimeLogSerializer(time_logs, many=True).data
        return Response(data)


class TimeLogRetrieveUpdateDelete(TimeLogApiViewMixin, APIView):

    permission_classes = (IsLogOwner, )

    def get(self, request, item_id: int):
        time_log = time_log_crud.get_by(pk=item_id)
        self.check_object_permissions(request, time_log)
        data = TimeLogSerializer(time_log).data
        return Response(data)
