
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grupo, Horario, HORARIO_HORAS
from cursos.models import Curso
from profesores.models import Profesor


@login_required
def lista_grupos(request):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    grupos = Grupo.objects.select_related('curso', 'profesor__usuario').order_by('nombre')

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
            fecha_fin=request.POST.get('fecha_fin')
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
        grupo.eliminar()

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


@login_required
def mi_horario(request):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    mis_grupos = Grupo.objects.filter(profesor__usuario=request.user, activo=True)
    horarios = Horario.objects.filter(grupo__in=mis_grupos).select_related('grupo')

    error = None
    if request.method == 'POST':
        grupo = get_object_or_404(mis_grupos, id=request.POST.get('grupo'))
        dia_semana = request.POST.get('dia_semana')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')

        if not (dia_semana and hora_inicio and hora_fin):
            error = 'Completa día, hora de inicio y hora de fin.'
        elif hora_fin <= hora_inicio:
            error = 'La hora de fin debe ser posterior a la hora de inicio.'
        else:
            Horario.objects.create(
                grupo=grupo,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            return redirect('mi_horario')

    return render(request, 'grupos/mi_horario.html', {
        'mis_grupos': mis_grupos,
        'horarios': horarios,
        'dias': Horario.DiaSemana.choices,
        'horas': HORARIO_HORAS,
        'error': error
    })


@login_required
def eliminar_horario(request, id):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    horario = get_object_or_404(Horario, id=id, grupo__profesor__usuario=request.user)

    if request.method == 'POST':
        horario.delete()

    return redirect('mi_horario')
