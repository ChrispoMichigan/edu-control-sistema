
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UsuarioManager


class Usuario(AbstractBaseUser, PermissionsMixin):

    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administracion'
        PROFESOR = 'PROFESOR', 'Profesor'
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ESTUDIANTE
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
