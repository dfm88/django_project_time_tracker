from rest_framework import serializers

from common.serializers import BaseMeta
from projects.serializers import ProjectAssignmentSerializer
from time_log.models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    project_assignment = ProjectAssignmentSerializer(read_only=True)

    class Meta(BaseMeta):
        model = TimeLog
