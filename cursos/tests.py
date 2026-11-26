import pytest
from django.urls import reverse

from cursos.models import Curso, Leccion, Progreso, Seccion

pytestmark = pytest.mark.django_db


def test_lista_cursos_bloquea_a_quien_no_es_admin(estudiante_client):
    response = estudiante_client.get(reverse('lista_cursos'))
    assert response.status_code == 302
    assert response.url == reverse('inicio')


def test_lista_cursos_admin_ve_los_cursos(admin_client, curso):
    response = admin_client.get(reverse('lista_cursos'))
    assert response.status_code == 200
    assert curso in response.context['cursos']


def test_crear_curso_admin_crea_registro(admin_client):
    response = admin_client.post(reverse('crear_curso'), {
        'nombre': 'Ingles Conversacional',
        'descripcion': 'Practica oral',
        'duracion_horas': 40,
    })
    assert response.status_code == 302
    assert Curso.objects.filter(nombre='Ingles Conversacional').exists()


def test_eliminar_curso_es_soft_delete(admin_client, curso):
    admin_client.post(reverse('eliminar_curso', args=[curso.id]))
    assert not Curso.objects.filter(id=curso.id).exists()
    assert Curso.todos.filter(id=curso.id).exists()


def test_cambiar_estado_invierte_activo(admin_client, curso):
    assert curso.activo is True
    admin_client.post(reverse('cambiar_estado', args=[curso.id]))
    curso.refresh_from_db()
    assert curso.activo is False


def test_progreso_para_sin_lecciones_es_cero(curso, estudiante):
    assert curso.progreso_para(estudiante) == 0


def test_progreso_para_calcula_porcentaje_de_lecciones_completadas(curso, estudiante):
    seccion = Seccion.objects.create(curso=curso, nombre='Introduccion')
    leccion_1 = Leccion.objects.create(seccion=seccion, titulo='Leccion 1')
    Leccion.objects.create(seccion=seccion, titulo='Leccion 2')
    Progreso.objects.create(estudiante=estudiante, leccion=leccion_1, completado=True)

    assert curso.progreso_para(estudiante) == 50
