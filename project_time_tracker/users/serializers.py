from rest_framework import serializers

from users.models import UserCustom


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ('id', 'username', 'email')
