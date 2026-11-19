
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso


@login_required
def lista_cursos(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    cursos = Curso.objects.all().order_by('nombre')

    return render(request, 'cursos/lista.html', {
        'cursos': cursos
    })


@login_required
def crear_curso(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        duracion_horas = request.POST.get('duracion_horas')

        Curso.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            duracion_horas=duracion_horas
        )

        return redirect('lista_cursos')

    return render(request, 'cursos/formulario.html')


@login_required
def editar_curso(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    curso = get_object_or_404(Curso, id=id)

    if request.method == 'POST':
        curso.nombre = request.POST.get('nombre')
        curso.descripcion = request.POST.get('descripcion')
        curso.duracion_horas = request.POST.get('duracion_horas')
        curso.save()

        return redirect('lista_cursos')

    return render(request, 'cursos/formulario.html', {
        'curso': curso
    })


@login_required
def eliminar_curso(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    curso = get_object_or_404(Curso, id=id)

    if request.method == 'POST':
        curso.delete()

    return redirect('lista_cursos')


@login_required
def cambiar_estado(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    curso = get_object_or_404(Curso, id=id)

    if request.method == 'POST':
        curso.activo = not curso.activo
        curso.save()

    return redirect('lista_cursos')
