
from django.urls import path
from . import views

urlpatterns = [
    path('clase/<int:clase_id>/', views.tomar_asistencia, name='tomar_asistencia'),
]
