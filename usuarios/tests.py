import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_login_con_credenciales_correctas_redirige_a_inicio(client, admin_user):
    response = client.post(reverse('login'), {
        'email': admin_user.email, 'password': 'clave12345'
    })
    assert response.status_code == 302
    assert response.url == reverse('inicio')


def test_login_con_credenciales_incorrectas_muestra_error(client, admin_user):
    response = client.post(reverse('login'), {
        'email': admin_user.email, 'password': 'incorrecta'
    })
    assert response.status_code == 200
    assert 'incorrectos' in response.context['error']


def test_inicio_sin_sesion_redirige_a_login(client):
    response = client.get(reverse('inicio'))
    assert response.status_code == 302
    assert response.url == reverse('login')


def test_inicio_expone_el_rol_del_usuario(admin_client):
    response = admin_client.get(reverse('inicio'))
    assert response.status_code == 200
    assert response.context['rol'] == 'ADMIN'
