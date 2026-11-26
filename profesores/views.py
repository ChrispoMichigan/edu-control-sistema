
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Profesor
from usuarios.models import Usuario
from grupos.models import Grupo
from inscripciones.models import Inscripcion


@login_required
def lista_profesores(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    profesores = Profesor.objects.all().order_by('usuario__first_name')

    return render(request, 'profesores/lista.html', {
        'profesores': profesores
    })


@login_required
def crear_profesor(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    error = None

    if request.method == 'POST':
        email = request.POST.get('email')

        if Usuario.objects.filter(email=email).exists():
            error = 'El correo ya esta registrado.'
        elif not request.POST.get('password'):
            error = 'La contrasena es obligatoria.'
        else:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    email=email,
                    password=request.POST.get('password'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    role='PROFESOR'
                )

                Profesor.objects.create(
                    usuario=usuario,
                    especialidad=request.POST.get('especialidad', ''),
                    telefono=request.POST.get('telefono', '')
                )

            return redirect('lista_profesores')

    return render(request, 'profesores/formulario.html', {
        'error': error
    })


@login_required
def editar_profesor(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    profesor = get_object_or_404(Profesor, id=id)
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')

        if Usuario.objects.filter(email=email).exclude(id=profesor.usuario_id).exists():
            error = 'El correo ya esta registrado.'
        else:
            profesor.usuario.email = email
            profesor.usuario.first_name = request.POST.get('first_name')
            profesor.usuario.last_name = request.POST.get('last_name')
            profesor.usuario.save()

            profesor.especialidad = request.POST.get('especialidad', '')
            profesor.telefono = request.POST.get('telefono', '')
            profesor.save()

            return redirect('lista_profesores')

    return render(request, 'profesores/formulario.html', {
        'profesor': profesor,
        'error': error
    })


@login_required
def eliminar_profesor(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    profesor = get_object_or_404(Profesor, id=id)

    if request.method == 'POST':
        profesor.eliminar()
        profesor.usuario.is_active = False
        profesor.usuario.save(update_fields=['is_active'])

    return redirect('lista_profesores')


@login_required
def cambiar_estado(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    profesor = get_object_or_404(Profesor, id=id)

    if request.method == 'POST':
        profesor.activo = not profesor.activo
        profesor.usuario.is_active = profesor.activo

        profesor.save()
        profesor.usuario.save()

    return redirect('lista_profesores')


@login_required
def mis_grupos(request):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    grupos = Grupo.objects.filter(profesor__usuario=request.user).select_related('curso')

    return render(request, 'profesores/mis_grupos.html', {
        'grupos': grupos
    })


@login_required
def ver_estudiantes_grupo(request, grupo_id):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=grupo_id, profesor__usuario=request.user)
    inscripciones = grupo.inscripciones.filter(activa=True).select_related('estudiante__usuario')

    return render(request, 'profesores/estudiantes_grupo.html', {
        'grupo': grupo,
        'inscripciones': inscripciones
    })


@login_required
def dar_de_baja_estudiante(request, inscripcion_id):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    inscripcion = get_object_or_404(
        Inscripcion, id=inscripcion_id, grupo__profesor__usuario=request.user
    )
    grupo_id = inscripcion.grupo_id

    if request.method == 'POST':
        inscripcion.eliminar()

    return redirect('ver_estudiantes_grupo', grupo_id=grupo_id)


@login_required
def progreso_grupo(request, grupo_id):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=grupo_id, profesor__usuario=request.user)
    inscripciones = grupo.inscripciones.filter(activa=True).select_related('estudiante__usuario')

    filas = [
        {
            'estudiante': insc.estudiante,
            'porcentaje': grupo.curso.progreso_para(insc.estudiante)
        }
        for insc in inscripciones
    ]

    return render(request, 'profesores/progreso.html', {
        'grupo': grupo,
        'filas': filas
    })
