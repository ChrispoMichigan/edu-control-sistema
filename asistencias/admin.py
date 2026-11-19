
from django.contrib import admin
from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'fecha', 'estado')
    search_fields = (
        'inscripcion__estudiante__matricula',
        'inscripcion__grupo__nombre'
    )
    list_filter = ('estado', 'fecha')
