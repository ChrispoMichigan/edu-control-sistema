import pytest
from django.urls import reverse

from estudiantes.models import Estudiante
from usuarios.models import Usuario

pytestmark = pytest.mark.django_db


def test_crear_estudiante_rechaza_correo_duplicado(admin_client, estudiante):
    response = admin_client.post(reverse('crear_estudiante'), {
        'first_name': 'Otro', 'last_name': 'Nombre',
        'email': estudiante.usuario.email, 'matricula': 'EST-999',
        'password': 'clave12345',
    })
    assert response.status_code == 200
    assert 'correo' in response.context['error'].lower()
    assert not Estudiante.objects.filter(matricula='EST-999').exists()


def test_crear_estudiante_rechaza_matricula_duplicada(admin_client, estudiante):
    response = admin_client.post(reverse('crear_estudiante'), {
        'first_name': 'Otro', 'last_name': 'Nombre',
        'email': 'otro@test.local', 'matricula': estudiante.matricula,
        'password': 'clave12345',
    })
    assert response.status_code == 200
    assert 'matricula' in response.context['error'].lower()
    assert not Usuario.objects.filter(email='otro@test.local').exists()


def test_crear_estudiante_exitoso_crea_usuario_y_perfil(admin_client):
    response = admin_client.post(reverse('crear_estudiante'), {
        'first_name': 'Carlos', 'last_name': 'Ramirez',
        'email': 'carlos@test.local', 'matricula': 'EST-200',
        'password': 'clave12345',
    })
    assert response.status_code == 302
    nuevo = Estudiante.objects.get(matricula='EST-200')
    assert nuevo.usuario.email == 'carlos@test.local'


def test_eliminar_estudiante_es_soft_delete_y_desactiva_el_usuario(admin_client, estudiante):
    admin_client.post(reverse('eliminar_estudiante', args=[estudiante.id]))

    assert not Estudiante.objects.filter(id=estudiante.id).exists()
    estudiante.usuario.refresh_from_db()
    assert estudiante.usuario.is_active is False
