
from django.contrib import admin
from .models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_horas', 'activo', 'created_at')
    search_fields = ('nombre',)
    list_filter = ('activo',)
