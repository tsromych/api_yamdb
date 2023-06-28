import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('superuser', 'Superuser'),
    ]

    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True,
    )
    role = models.CharField(
        max_length=150,
        choices=ROLE_CHOICES,
        default='user',
    )
    confirmation_code = models.CharField(
        max_length=36,
        blank=True,
        unique=True,
        default=uuid.uuid4
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator' or self.is_admin
