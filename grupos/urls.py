
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_grupos, name='lista_grupos'),
    path('crear/', views.crear_grupo, name='crear_grupo'),
    path('editar/<int:id>/', views.editar_grupo, name='editar_grupo'),
    path('eliminar/<int:id>/', views.eliminar_grupo, name='eliminar_grupo'),
    path('estado/<int:id>/', views.cambiar_estado, name='cambiar_estado_grupo'),
]
