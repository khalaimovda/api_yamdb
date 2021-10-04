from enum import Enum
from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)

class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        blank=True,
    )
