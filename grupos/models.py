
from django.db import models
from cursos.models import Curso
from profesores.models import Profesor


class Grupo(models.Model):

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='grupos'
    )
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.PROTECT,
        related_name='grupos'
    )
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dias_clase = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.curso.nombre}"
