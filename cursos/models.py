
from django.db import models


class Curso(models.Model):

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    duracion_horas = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
