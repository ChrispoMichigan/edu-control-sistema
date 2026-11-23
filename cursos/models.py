
from django.db import models
from core.models import SoftDeleteModel


class Curso(SoftDeleteModel):

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    duracion_horas = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='cursos/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def progreso_para(self, estudiante):
        total = Leccion.objects.filter(seccion__curso=self).count()
        if total == 0:
            return 0
        completadas = Progreso.objects.filter(
            leccion__seccion__curso=self,
            estudiante=estudiante,
            completado=True
        ).count()
        return round(completadas * 100 / total)


class Seccion(models.Model):

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='secciones'
    )
    nombre = models.CharField(max_length=150)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.curso.nombre} - {self.nombre}"


class Leccion(models.Model):

    seccion = models.ForeignKey(
        Seccion,
        on_delete=models.CASCADE,
        related_name='lecciones'
    )
    titulo = models.CharField(max_length=150)
    texto = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"{self.seccion.nombre} - {self.titulo}"


class Progreso(models.Model):

    estudiante = models.ForeignKey(
        'estudiantes.Estudiante',
        on_delete=models.CASCADE,
        related_name='progresos'
    )
    leccion = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name='progresos'
    )
    completado = models.BooleanField(default=False)
    completado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'leccion'],
                name='progreso_unico_por_leccion'
            )
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.leccion}"
