from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import CustomUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            'name',
            'phone',
            'address',
        ]

