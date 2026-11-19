
from django.contrib import admin
from .models import Clase


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
