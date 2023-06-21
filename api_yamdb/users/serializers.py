import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser

User = CustomUser  # get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
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


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all())],
        max_length=150
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all())],
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate(self, data):
        if User.objects.filter(
            username=data['username']
        ) and not User.objects.filter(email=data['email']):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(
            email=data['email']
        ) and not User.objects.filter(username=data['username']):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(
                'Введенное имя недопустимо!'
            )
        if not re.match(r'^[\w.@+-]+\Z', name):
            raise serializers.ValidationError(
                'В username использованы недопустимые символы!'
            )
        return name
