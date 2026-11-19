
from django.contrib import admin
from .models import Profesor


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad', 'telefono', 'activo')
    search_fields = ('usuario__email', 'usuario__first_name', 'usuario__last_name')
    list_filter = ('activo',)
