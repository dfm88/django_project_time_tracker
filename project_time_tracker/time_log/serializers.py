from common.serializers import BaseMeta
from projects.serializers import ReadProjectAssignmentSerializer
from rest_framework import serializers

from .models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    project_assignment = ReadProjectAssignmentSerializer(read_only=True)

    class Meta(BaseMeta):
        model = TimeLog
