import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from api.service_functions import check_username

CHAR_COUNT_254 = 254
CHAR_COUNT_150 = 150
CHAR_COUNT_36 = 36
ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'
ROLE_USER = 'user'


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MODERATOR, 'Moderator'),
    ]

    username = models.CharField(
        max_length=CHAR_COUNT_150,
        validators=(check_username,),
        blank=False,
        unique=True,
        db_index=True,
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        max_length=CHAR_COUNT_254,
        blank=False,
        unique=True,
        verbose_name='Почта',
    )
    role = models.CharField(
        max_length=CHAR_COUNT_150,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        verbose_name='Роль',
    )
    confirmation_code = models.CharField(
        max_length=CHAR_COUNT_36,
        blank=True,
        unique=True,
        default=uuid.uuid4
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR or self.is_admin
