import pytest
from django.urls import reverse

from grupos.models import Horario
from inscripciones.models import Inscripcion

pytestmark = pytest.mark.django_db


def test_lista_grupos_bloquea_a_quien_no_es_admin(profesor_client):
    response = profesor_client.get(reverse('lista_grupos'))
    assert response.status_code == 302
    assert response.url == reverse('inicio')


def test_cupo_disponible_resta_inscripciones_activas(grupo, estudiante):
    assert grupo.cupo_disponible() == grupo.capacidad

    Inscripcion.objects.create(estudiante=estudiante, grupo=grupo)

    assert grupo.cupo_disponible() == grupo.capacidad - 1


def test_cupo_disponible_ignora_inscripciones_eliminadas(grupo, estudiante):
    inscripcion = Inscripcion.objects.create(estudiante=estudiante, grupo=grupo)
    inscripcion.eliminar()

    assert grupo.cupo_disponible() == grupo.capacidad


def test_mi_horario_rechaza_hora_fin_antes_de_la_de_inicio(profesor_client, grupo):
    response = profesor_client.post(reverse('mi_horario'), {
        'grupo': grupo.id, 'dia_semana': 0,
        'hora_inicio': '10:00', 'hora_fin': '09:00',
    })
    assert response.status_code == 200
    assert 'posterior' in response.context['error']
    assert not Horario.objects.filter(grupo=grupo).exists()


def test_mi_horario_crea_horario_con_datos_validos(profesor_client, grupo):
    response = profesor_client.post(reverse('mi_horario'), {
        'grupo': grupo.id, 'dia_semana': 0,
        'hora_inicio': '09:00', 'hora_fin': '10:00',
    })
    assert response.status_code == 302
    assert Horario.objects.filter(grupo=grupo).count() == 1
