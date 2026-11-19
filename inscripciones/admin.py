
from django.contrib import admin
from .models import Inscripcion


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'grupo', 'fecha_inscripcion', 'activa')
    search_fields = (
        'estudiante__matricula',
        'estudiante__usuario__first_name',
        'grupo__nombre'
    )
    list_filter = ('activa', 'grupo')
