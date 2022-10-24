from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.serializers import serialize_input_data
from projects.crud import project_assign_crud
from projects.models import Project
from projects.views import IsAssignedToProjectOrAdmin, ProjectIdMixin
from time_log.crud import time_log_crud
from time_log.permissions import IsLogOwnerOrAdmin
from time_log.serializers import TimeLogSerializer


class TimeLogListCreateApi(ProjectIdMixin, APIView):
    permission_classes = (IsAssignedToProjectOrAdmin,)

    def get(self, request, project: Project, *args, **kwargs):
        self.check_object_permissions(request, project)
        time_logs = time_log_crud.filter_by(project_id=project.id)
        data = TimeLogSerializer(time_logs, many=True).data
        return Response(data)

    def post(self, request, project: Project, *args, **kwargs):
        self.check_object_permissions(request, project)

        # serialize input data
        validated_data = serialize_input_data(
            serializer=TimeLogSerializer,
            data=request.data
        )

        # take the relation user-project
        project_assignment_obj = project_assign_crud.get_by(
            user_id=request.user.id,
            project_id=project.id
        )

        # create time log
        time_log_obj = time_log_crud.create_time_log(
            project_assignment=project_assignment_obj,
            **validated_data
        )

        ser_data = TimeLogSerializer(time_log_obj).data
        return Response(ser_data, status=status.HTTP_201_CREATED)


class TimeLogRetrieveUpdateDelete(APIView):

    permission_classes = (IsLogOwnerOrAdmin, )

    def get(self, request, item_id: int):
        time_log = time_log_crud.get_by(pk=item_id)
        self.check_object_permissions(request, time_log)
        data = TimeLogSerializer(time_log).data
        return Response(data)

    def put(self, request, item_id: int):
        time_log = time_log_crud.get_by(pk=item_id)
        self.check_object_permissions(request, time_log)

        # serialize input data
        validated_data = serialize_input_data(
            serializer=TimeLogSerializer,
            data=request.data
        )

        # update time log
        time_log_crud.update_time_log(
            time_log_id=item_id,
            **validated_data
        )

        ser_data = TimeLogSerializer(time_log).data
        return Response(ser_data)

    def delete(self, request, item_id: int):
        time_log = time_log_crud.get_by(pk=item_id)
        self.check_object_permissions(request, time_log)
        time_log_crud.delete(instance=time_log)
        return Response(status=status.HTTP_204_NO_CONTENT)
