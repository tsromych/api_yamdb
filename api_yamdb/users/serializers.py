from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(required=True, max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    bio = serializers.CharField()

    def validate_username(self, data):
        username = data
        if not re.match(r'^[\w.@+-]+\z', username):
            raise serializers.ValidationError(
                'в username использованы недопустимые символы'
            )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'])
        return user
