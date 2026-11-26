import datetime

import pytest

from cursos.models import Curso
from estudiantes.models import Estudiante
from grupos.models import Grupo
from profesores.models import Profesor
from usuarios.models import Usuario

CLAVE = 'clave12345'


@pytest.fixture(autouse=True)
def _hasher_rapido_para_pruebas(settings):
    # PBKDF2 real tarda ~100-300ms por usuario creado; MD5 es instantáneo y
    # solo aplica en esta corrida de pytest, nunca en producción.
    settings.PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']


@pytest.fixture
def admin_user(db):
    return Usuario.objects.create_user(
        email='admin@test.local', password=CLAVE,
        first_name='Admin', last_name='EduControl', role='ADMIN'
    )


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    return client


@pytest.fixture
def profesor(db):
    usuario = Usuario.objects.create_user(
        email='profesor@test.local', password=CLAVE,
        first_name='Laura', last_name='Garcia', role='PROFESOR'
    )
    return Profesor.objects.create(usuario=usuario)


@pytest.fixture
def profesor_client(client, profesor):
    client.force_login(profesor.usuario)
    return client


@pytest.fixture
def estudiante(db):
    usuario = Usuario.objects.create_user(
        email='estudiante@test.local', password=CLAVE,
        first_name='Ana', last_name='Lopez', role='ESTUDIANTE'
    )
    return Estudiante.objects.create(usuario=usuario, matricula='EST-100')


@pytest.fixture
def estudiante_client(client, estudiante):
    client.force_login(estudiante.usuario)
    return client


@pytest.fixture
def curso(db):
    return Curso.objects.create(nombre='Excel Avanzado', duracion_horas=20)


@pytest.fixture
def grupo(db, curso, profesor):
    return Grupo.objects.create(
        curso=curso, profesor=profesor, nombre='EXC-A', capacidad=5,
        fecha_inicio=datetime.date(2026, 1, 12), fecha_fin=datetime.date(2026, 3, 20)
    )
