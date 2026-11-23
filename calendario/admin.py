
from django.contrib import admin
from .models import Clase, Festivo


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = (
        'grupo',
        'fecha',
        'hora_inicio',
        'hora_fin',
        'tema',
        'es_festivo'
    )
    search_fields = ('grupo__nombre', 'tema')
    list_filter = ('fecha', 'es_festivo')


@admin.register(Festivo)
class FestivoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('fecha',)
