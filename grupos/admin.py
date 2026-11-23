
from django.contrib import admin
from .models import Grupo, Horario


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


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('grupo', 'dia_semana', 'hora_inicio', 'hora_fin')
    list_filter = ('dia_semana',)
