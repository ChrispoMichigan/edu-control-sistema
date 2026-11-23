
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_profesores, name='lista_profesores'),
    path('crear/', views.crear_profesor, name='crear_profesor'),
    path('editar/<int:id>/', views.editar_profesor, name='editar_profesor'),
    path('eliminar/<int:id>/', views.eliminar_profesor, name='eliminar_profesor'),
    path('estado/<int:id>/', views.cambiar_estado, name='cambiar_estado_profesor'),

    path('mis-grupos/', views.mis_grupos, name='mis_grupos'),
    path('grupo/<int:grupo_id>/estudiantes/', views.ver_estudiantes_grupo, name='ver_estudiantes_grupo'),
    path('inscripcion/<int:inscripcion_id>/dar-de-baja/', views.dar_de_baja_estudiante, name='dar_de_baja_estudiante'),
    path('grupo/<int:grupo_id>/progreso/', views.progreso_grupo, name='progreso_grupo'),
]
