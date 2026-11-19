
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grupo
from cursos.models import Curso
from profesores.models import Profesor


@login_required
def lista_grupos(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    grupos = Grupo.objects.all().order_by('nombre')

    return render(request, 'grupos/lista.html', {
        'grupos': grupos
    })


@login_required
def crear_grupo(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    cursos = Curso.objects.filter(activo=True)
    profesores = Profesor.objects.filter(activo=True)

    if request.method == 'POST':
        Grupo.objects.create(
            curso_id=request.POST.get('curso'),
            profesor_id=request.POST.get('profesor'),
            nombre=request.POST.get('nombre'),
            capacidad=request.POST.get('capacidad'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin'),
            dias_clase=request.POST.get('dias_clase')
        )

        return redirect('lista_grupos')

    return render(request, 'grupos/formulario.html', {
        'cursos': cursos,
        'profesores': profesores
    })


@login_required
def editar_grupo(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=id)
    cursos = Curso.objects.filter(activo=True)
    profesores = Profesor.objects.filter(activo=True)

    if request.method == 'POST':
        grupo.curso_id = request.POST.get('curso')
        grupo.profesor_id = request.POST.get('profesor')
        grupo.nombre = request.POST.get('nombre')
        grupo.capacidad = request.POST.get('capacidad')
        grupo.fecha_inicio = request.POST.get('fecha_inicio')
        grupo.fecha_fin = request.POST.get('fecha_fin')
        grupo.dias_clase = request.POST.get('dias_clase')
        grupo.save()

        return redirect('lista_grupos')

    return render(request, 'grupos/formulario.html', {
        'grupo': grupo,
        'cursos': cursos,
        'profesores': profesores
    })


@login_required
def eliminar_grupo(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=id)

    if request.method == 'POST':
        grupo.delete()

    return redirect('lista_grupos')


@login_required
def cambiar_estado(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=id)

    if request.method == 'POST':
        grupo.activo = not grupo.activo
        grupo.save()

    return redirect('lista_grupos')
