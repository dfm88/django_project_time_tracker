from projects.crud import project_assign_crud
from projects.models import Project
from projects.views import ProjectIdPermissionMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from time_log.crud import time_log_crud
from time_log.permissions import IsLogOwner
from time_log.serializers import TimeLogSerializer


class TimeLogListCreateApi(ProjectIdPermissionMixin, APIView):

    def get(self, request, project: Project, *args, **kwargs):
        time_logs = time_log_crud.get_logs_by_project(project_id=project.id)
        data = TimeLogSerializer(time_logs, many=True).data
        return Response(data)

    def post(self, request, project: Project, *args, **kwargs):
        time_log_serializer = TimeLogSerializer(data=request.data)

        if time_log_serializer.is_valid(raise_exception=True):
            data = time_log_serializer.data

        project_assignemnt_obj = project_assign_crud.get_by(
            user_id=request.user.id,
            project_id=project.id
        )

        time_log_obj = time_log_crud.create_time_log(
            project_assignment=project_assignemnt_obj,
            **data
        )

        ser_data = TimeLogSerializer(time_log_obj).data
        return Response(ser_data)


class TimeLogRetrieveUpdateDelete(ProjectIdPermissionMixin, APIView):

    permission_classes = (IsLogOwner, )

    def get(self, request, item_id: int, *args, project=None):
        time_log = time_log_crud.get_by(pk=item_id)
        self.check_object_permissions(request, time_log)
        data = TimeLogSerializer(time_log).data
        return Response(data)
