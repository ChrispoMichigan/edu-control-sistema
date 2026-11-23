
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('crear/', views.crear_curso, name='crear_curso'),
    path('editar/<int:id>/', views.editar_curso, name='editar_curso'),
    path('eliminar/<int:id>/', views.eliminar_curso, name='eliminar_curso'),
    path('estado/<int:id>/', views.cambiar_estado, name='cambiar_estado'),

    path('<int:curso_id>/contenido/', views.gestionar_contenido, name='gestionar_contenido'),
    path('<int:curso_id>/contenido/seccion/crear/', views.crear_seccion, name='crear_seccion'),
    path('seccion/<int:id>/editar/', views.editar_seccion, name='editar_seccion'),
    path('seccion/<int:id>/eliminar/', views.eliminar_seccion, name='eliminar_seccion'),
    path('seccion/<int:seccion_id>/leccion/crear/', views.crear_leccion, name='crear_leccion'),
    path('leccion/<int:id>/editar/', views.editar_leccion, name='editar_leccion'),
    path('leccion/<int:id>/eliminar/', views.eliminar_leccion, name='eliminar_leccion'),

    path('catalogo/', views.catalogo_cursos, name='catalogo_cursos'),
    path('catalogo/<int:id>/', views.detalle_curso, name='detalle_curso'),
    path('leccion/<int:leccion_id>/marcar/', views.marcar_leccion, name='marcar_leccion'),
]
