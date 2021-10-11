from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
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

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin' 

    class Meta:
        ordering = ['id', ]
