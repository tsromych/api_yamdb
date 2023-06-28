import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser

User = CustomUser


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
            queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

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
