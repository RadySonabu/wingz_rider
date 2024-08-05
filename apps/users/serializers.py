from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id_user", "role", "email", "first_name", "last_name", "phone_number"]


class UserSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id_user", "role", "email", "first_name", "last_name", "phone_number"]
