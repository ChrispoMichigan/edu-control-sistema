
from django.contrib import admin
from .models import Grupo


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'curso',
        'profesor',
        'capacidad',
        'fecha_inicio',
        'fecha_fin',
        'activo'
    )
    search_fields = ('nombre', 'curso__nombre')
    list_filter = ('activo', 'curso')
