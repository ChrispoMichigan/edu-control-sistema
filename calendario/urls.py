
from django.urls import path
from . import views

urlpatterns = [
    path('grupo/<int:grupo_id>/', views.lista_clases, name='lista_clases'),
    path('grupo/<int:grupo_id>/nueva/', views.crear_clase, name='crear_clase'),
]
