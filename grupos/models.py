
from django.db import models
from core.models import SoftDeleteModel
from cursos.models import Curso
from profesores.models import Profesor


class Grupo(SoftDeleteModel):

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
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.curso.nombre}"

    def cupo_disponible(self):
        return self.capacidad - self.inscripciones.filter(activa=True).count()


class Horario(models.Model):

    class DiaSemana(models.IntegerChoices):
        LUNES = 0, 'Lunes'
        MARTES = 1, 'Martes'
        MIERCOLES = 2, 'Miércoles'
        JUEVES = 3, 'Jueves'
        VIERNES = 4, 'Viernes'
        SABADO = 5, 'Sábado'
        DOMINGO = 6, 'Domingo'

    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    dia_semana = models.IntegerField(choices=DiaSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ['dia_semana', 'hora_inicio']
        constraints = [
            models.UniqueConstraint(
                fields=['grupo', 'dia_semana', 'hora_inicio'],
                name='horario_unico_por_grupo_dia_hora'
            )
        ]

    def __str__(self):
        return f"{self.grupo.nombre} - {self.get_dia_semana_display()} {self.hora_inicio}"

    @property
    def columna(self):
        return self.dia_semana + 2

    @property
    def fila_inicio(self):
        return 2 + (self.hora_inicio.hour - HORARIO_HORA_BASE) * 2 + (1 if self.hora_inicio.minute >= 30 else 0)

    @property
    def fila_fin(self):
        return 2 + (self.hora_fin.hour - HORARIO_HORA_BASE) * 2 + (1 if self.hora_fin.minute >= 30 else 0)


HORARIO_HORA_BASE = 7
HORARIO_HORAS = list(range(HORARIO_HORA_BASE, HORARIO_HORA_BASE + 14))
