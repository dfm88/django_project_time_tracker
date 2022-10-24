from rest_framework import serializers

from common.serializers import BaseMeta
from users.serializers import UserSerializer

from .models import Project, ProjectAssignment


class ProjectSerializer(serializers.ModelSerializer):
    assignees = UserSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta(BaseMeta):
        model = Project


class ProjectAssignmentSerializer(serializers.ModelSerializer):

    class Meta(BaseMeta):
        model = ProjectAssignment
