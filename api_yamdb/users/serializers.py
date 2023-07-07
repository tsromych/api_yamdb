from rest_framework import serializers

from api.service_functions import check_username
from .models import CustomUser

User = CustomUser

USERNAME_FIELD_LENGTH = 150
EMAIL_FIELD_LENGTH = 254


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class RoleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class ConformationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_FIELD_LENGTH,
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_FIELD_LENGTH,
    )

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)

    def validate(self, data):
        if (User.objects.filter(username=data['username'])
                and not User.objects.filter(email=data['email'])):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if (User.objects.filter(email=data['email'])
                and not User.objects.filter(username=data['username'])):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data

    def validate_username(self, name):
        return check_username(name)
