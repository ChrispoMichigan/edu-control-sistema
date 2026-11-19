
from django.db import models
from estudiantes.models import Estudiante
from grupos.models import Grupo


class Inscripcion(models.Model):

    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'grupo'],
                name='inscripcion_unica_por_grupo'
            )
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.grupo}"
