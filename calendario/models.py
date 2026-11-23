
from django.db import models
from grupos.models import Grupo


class Clase(models.Model):

    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name='clases'
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tema = models.CharField(max_length=150, blank=True)
    es_festivo = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['fecha', 'hora_inicio']
        constraints = [
            models.UniqueConstraint(
                fields=['grupo', 'fecha', 'hora_inicio'],
                name='clase_unica_por_grupo_fecha_hora'
            )
        ]

    def __str__(self):
        return f"{self.grupo.nombre} - {self.fecha}"


class Festivo(models.Model):

    fecha = models.DateField(unique=True)
    nombre = models.CharField(max_length=150)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"{self.fecha} - {self.nombre}"
