from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAssignedToProjectOrAdmin, IsLogOwnerOrAdmin
from common.serializers import serialize_input_data
from projects.crud import project_assign_crud
from projects.mixins import ProjectIdQueryStringMixin
from projects.models import Project
from time_log.crud import time_log_crud
from time_log.mixins import TimeLogFromIdMixin
from time_log.models import TimeLog
from time_log.serializers import TimeLogSerializer


class TimeLogListCreateApi(ProjectIdQueryStringMixin, APIView):
    permission_classes = (IsAssignedToProjectOrAdmin,)

    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, project: Project, *args, **kwargs):
        self.check_object_permissions(request, project)
        time_logs = time_log_crud.filter_by(project_assignment__project=project.id)
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


class TimeLogRetrieveUpdateDelete(TimeLogFromIdMixin, APIView):

    permission_classes = (IsLogOwnerOrAdmin, )

    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, time_log_id: int, time_log: TimeLog):
        self.check_object_permissions(request, time_log)
        data = TimeLogSerializer(time_log).data
        return Response(data)

    def put(self, request, time_log_id: int, time_log: TimeLog):
        self.check_object_permissions(request, time_log)

        # serialize input data
        validated_data = serialize_input_data(
            serializer=TimeLogSerializer,
            data=request.data
        )

        # update time log
        time_log_crud.update_time_log(
            time_log_id=time_log_id,
            **validated_data
        )
        time_log.refresh_from_db()

        ser_data = TimeLogSerializer(time_log).data
        return Response(ser_data)

    def delete(self, request, time_log_id: int, time_log: TimeLog):
        self.check_object_permissions(request, time_log)
        time_log_crud.delete(instance=time_log)
        return Response(status=status.HTTP_204_NO_CONTENT)
