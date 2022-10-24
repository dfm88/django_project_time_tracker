from common.serializers import BaseMeta
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Project, ProjectAssignment


class ReadProjectSerializer(serializers.ModelSerializer):
    assignees = UserSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta(BaseMeta):
        model = Project


class ReadProjectAssignmentSerializer(serializers.ModelSerializer):

    class Meta(BaseMeta):
        model = ProjectAssignment
