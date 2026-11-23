
from django.urls import path
from . import views

urlpatterns = [
    path('inscribirse/<int:grupo_id>/', views.inscribirse, name='inscribirse'),
    path('horario/', views.horario_estudiante, name='horario_estudiante'),
]
