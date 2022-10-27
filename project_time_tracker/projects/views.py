import functools

from django.db import models
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdminForWriting, IsAssignedToProjectOrAdmin
from common.serializers import serialize_input_data
from projects.crud import project_assign_crud, project_crud
from projects.mixins import ProjectFromIdMixin
from projects.models import Project
from projects.serializers import ProjectSerializer
from time_log.core import calculate_spent_time
from time_log.crud import time_log_crud
from users.crud import user_crud
from users.mixins import UserIdQueryStringMixin
from users.models import UserCustom


class ProjectListCreateApi(APIView):
    permission_classes = (IsAdminForWriting,)

    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request):
        projects = project_crud.get_projects_per_user_role(
            user=request.user
        )
        data = ProjectSerializer(projects, many=True).data
        return Response(data)

    def post(self, request):
        # serialize input data
        validated_data = serialize_input_data(
            serializer=ProjectSerializer,
            data=request.data
        )

        # create project
        project_obj = project_crud.create_project(
            creator=request.user,
            **validated_data,
        )

        ser_data = ProjectSerializer(project_obj).data
        return Response(ser_data, status=status.HTTP_201_CREATED)


class ProjectRetrieveUpdateDelete(ProjectFromIdMixin, APIView):
    permission_classes = (IsAdminForWriting, IsAssignedToProjectOrAdmin,)

    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, project_id: int, project: Project):
        self.check_object_permissions(request, project)
        data = ProjectSerializer(project).data
        return Response(data)

    def put(self, request, project_id: int, project: Project):
        # serialize input data
        validated_data = serialize_input_data(
            serializer=ProjectSerializer,
            data=request.data,
            partial=True,
        )

        # update project log
        project_crud.update_project(
            project_id=project_id,
            **validated_data
        )
        project.refresh_from_db()

        ser_data = ProjectSerializer(project).data
        return Response(ser_data)

    def delete(self, request, project_id: int, project: Project):
        project_crud.delete(instance=project)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectHandleUsers(ProjectFromIdMixin, APIView):
    permission_classes = (IsAdminForWriting, )

    @staticmethod
    @functools.lru_cache(maxsize=64)
    def _get_users_from_body(body: list) -> models.QuerySet:
        return user_crud.get_users_from_usernames(usernames=body)

    def post(self, request, project_id: int, project: Project):
        """Add users in request body from project
        request.data: ["user2", "user2", "user3]

        """
        users = self._get_users_from_body(body=request.data)
        project_assign_crud.add_users_to_project(
            project=project,
            users=users,
        )
        return Response()

    def delete(self, request, project_id: int, project: Project):
        """Remove users in request body from project
        request.data: ["user2", "user2", "user3]
        """
        users = self._get_users_from_body(body=request.data)
        project_assign_crud.remove_users_from_project(
            project=project,
            users=users,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectStatistics(UserIdQueryStringMixin, APIView):
    permission_classes = (IsAssignedToProjectOrAdmin, )

    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, project_id: int, project: Project, user: UserCustom = None):
        """
        Total time spent on the given project from all assignees

        Optional query_parameter `user_id` to show only time of a specific user
        """
        resp = {
            "project": project.id,
            "total_time": {}
        }

        time_logs = time_log_crud.get_logs_for_statistics(
            project_id=project.id,
            user=user
        )

        resp['total_time'] = calculate_spent_time(
            time_logs=time_logs
        )

        return Response(resp)
