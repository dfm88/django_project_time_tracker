from rest_framework import serializers

from .models import UserCustom


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ('id', 'username', 'email')
