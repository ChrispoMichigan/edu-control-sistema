import datetime

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from estudiantes.models import Estudiante
from grupos.models import Grupo, Horario
from inscripciones.models import Inscripcion
from usuarios.models import Usuario

pytestmark = pytest.mark.django_db


def _mensajes(response):
    return [m.message.lower() for m in get_messages(response.wsgi_request)]


def test_inscribirse_exitoso_crea_inscripcion(estudiante_client, estudiante, grupo):
    response = estudiante_client.post(reverse('inscribirse', args=[grupo.id]))

    assert response.status_code == 302
    assert Inscripcion.objects.filter(estudiante=estudiante, grupo=grupo, activa=True).exists()


def test_inscribirse_bloqueado_si_el_grupo_esta_lleno(estudiante_client, estudiante, grupo):
    grupo.capacidad = 1
    grupo.save()
    otro_usuario = Usuario.objects.create_user(
        email='otro-estudiante@test.local', password='clave12345',
        first_name='Otro', last_name='Estudiante', role='ESTUDIANTE'
    )
    otro = Estudiante.objects.create(usuario=otro_usuario, matricula='EST-300')
    Inscripcion.objects.create(estudiante=otro, grupo=grupo)

    response = estudiante_client.post(reverse('inscribirse', args=[grupo.id]))

    assert not Inscripcion.objects.filter(estudiante=estudiante, grupo=grupo).exists()
    assert any('cupo' in m for m in _mensajes(response))


def test_inscribirse_bloqueado_si_ya_esta_inscrito(estudiante_client, estudiante, grupo):
    Inscripcion.objects.create(estudiante=estudiante, grupo=grupo)

    response = estudiante_client.post(reverse('inscribirse', args=[grupo.id]))

    assert Inscripcion.objects.filter(estudiante=estudiante, grupo=grupo).count() == 1
    assert any('inscrito' in m for m in _mensajes(response))


def test_inscribirse_bloqueado_por_choque_de_horario(estudiante_client, estudiante, grupo, curso, profesor):
    otro_grupo = Grupo.objects.create(
        curso=curso, profesor=profesor, nombre='EXC-B', capacidad=5,
        fecha_inicio=datetime.date(2026, 1, 12), fecha_fin=datetime.date(2026, 3, 20),
    )
    Horario.objects.create(grupo=grupo, dia_semana=0, hora_inicio='09:00', hora_fin='10:00')
    Horario.objects.create(grupo=otro_grupo, dia_semana=0, hora_inicio='09:30', hora_fin='11:00')
    Inscripcion.objects.create(estudiante=estudiante, grupo=grupo)

    response = estudiante_client.post(reverse('inscribirse', args=[otro_grupo.id]))

    assert not Inscripcion.objects.filter(estudiante=estudiante, grupo=otro_grupo).exists()
    assert any('choca' in m for m in _mensajes(response))


def test_inscribirse_reactiva_una_inscripcion_eliminada_antes(estudiante_client, estudiante, grupo):
    inscripcion = Inscripcion.objects.create(estudiante=estudiante, grupo=grupo)
    inscripcion.eliminar()

    response = estudiante_client.post(reverse('inscribirse', args=[grupo.id]))

    assert response.status_code == 302
    assert Inscripcion.todos.filter(estudiante=estudiante, grupo=grupo).count() == 1
    reactivada = Inscripcion.objects.get(estudiante=estudiante, grupo=grupo)
    assert reactivada.activa is True
    assert reactivada.eliminado_en is None
