
from django.contrib import admin
from .models import Estudiante


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'usuario', 'telefono', 'fecha_registro', 'activo')
    search_fields = ('matricula', 'usuario__email', 'usuario__first_name', 'usuario__last_name')
    list_filter = ('activo',)
