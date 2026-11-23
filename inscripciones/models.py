
from django.db import models
from core.models import SoftDeleteModel
from estudiantes.models import Estudiante
from grupos.models import Grupo


class Inscripcion(SoftDeleteModel):

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
                condition=models.Q(eliminado_en__isnull=True),
                name='inscripcion_unica_por_grupo_activa'
            )
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.grupo}"
