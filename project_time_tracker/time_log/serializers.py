from rest_framework import serializers

from common.serializers import BaseMeta

from .models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):

    class Meta(BaseMeta):
        model = TimeLog
