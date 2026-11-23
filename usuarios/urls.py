from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('inicio/', views.inicio_view, name='inicio'),
    path('cerrar-sesion/', views.logout_view, name='logout'),
]
