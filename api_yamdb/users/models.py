from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('superuser', 'Superuser')
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user')
    confirmation_code = models.CharField(
        max_length=10,
        blank=True,
        null=True)
    bio = models.CharField(
        max_length=10,
        blank=True,
        null=True)
