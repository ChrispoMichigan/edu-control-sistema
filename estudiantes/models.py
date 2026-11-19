
from django.db import models
from usuarios.models import Usuario


class Estudiante(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_estudiante'
    )
    matricula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.matricula} - {self.usuario.first_name} {self.usuario.last_name}"
