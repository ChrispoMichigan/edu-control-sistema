
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Estudiante
from usuarios.models import Usuario


@login_required
def lista_estudiantes(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    estudiantes = Estudiante.objects.all().order_by('matricula')

    return render(request, 'estudiantes/lista.html', {
        'estudiantes': estudiantes
    })


@login_required
def crear_estudiante(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        matricula = request.POST.get('matricula')

        if Usuario.objects.filter(email=email).exists():
            error = 'El correo ya esta registrado.'
        elif Estudiante.objects.filter(matricula=matricula).exists():
            error = 'La matricula ya esta registrada.'
        elif not request.POST.get('password'):
            error = 'La contrasena es obligatoria.'
        else:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    email=email,
                    password=request.POST.get('password'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    role='ESTUDIANTE'
                )

                Estudiante.objects.create(
                    usuario=usuario,
                    matricula=matricula,
                    telefono=request.POST.get('telefono')
                )

            return redirect('lista_estudiantes')

    return render(request, 'estudiantes/formulario.html', {
        'error': error
    })


@login_required
def editar_estudiante(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    estudiante = get_object_or_404(Estudiante, id=id)
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        matricula = request.POST.get('matricula')

        if Usuario.objects.filter(email=email).exclude(
            id=estudiante.usuario_id
        ).exists():
            error = 'El correo ya esta registrado.'
        elif Estudiante.objects.filter(matricula=matricula).exclude(
            id=estudiante.id
        ).exists():
            error = 'La matricula ya esta registrada.'
        else:
            estudiante.usuario.email = email
            estudiante.usuario.first_name = request.POST.get('first_name')
            estudiante.usuario.last_name = request.POST.get('last_name')
            estudiante.usuario.save()

            estudiante.matricula = matricula
            estudiante.telefono = request.POST.get('telefono')
            estudiante.save()

            return redirect('lista_estudiantes')

    return render(request, 'estudiantes/formulario.html', {
        'estudiante': estudiante,
        'error': error
    })


@login_required
def eliminar_estudiante(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    estudiante = get_object_or_404(Estudiante, id=id)

    if request.method == 'POST':
        estudiante.usuario.delete()

    return redirect('lista_estudiantes')


@login_required
def cambiar_estado(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    estudiante = get_object_or_404(Estudiante, id=id)

    if request.method == 'POST':
        estudiante.activo = not estudiante.activo
        estudiante.usuario.is_active = estudiante.activo

        estudiante.save()
        estudiante.usuario.save()

    return redirect('lista_estudiantes')
