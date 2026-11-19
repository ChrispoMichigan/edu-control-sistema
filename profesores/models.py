
from django.db import models
from usuarios.models import Usuario


class Profesor(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_profesor'
    )
    especialidad = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"
