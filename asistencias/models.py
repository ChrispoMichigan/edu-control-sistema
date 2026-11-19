
from django.db import models
from inscripciones.models import Inscripcion


class Asistencia(models.Model):

    class Estados(models.TextChoices):
        PRESENTE = 'PRESENTE', 'Presente'
        TARDE = 'TARDE', 'Retardo'
        AUSENTE = 'AUSENTE', 'Ausente'
        JUSTIFICADO = 'JUSTIFICADO', 'Justificado'

    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='asistencias'
    )
    fecha = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=Estados.choices,
        default=Estados.PRESENTE
    )
    observaciones = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['inscripcion', 'fecha'],
                name='asistencia_unica_por_fecha'
            )
        ]

    def __str__(self):
        return f"{self.inscripcion} - {self.fecha} - {self.estado}"
