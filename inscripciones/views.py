
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Inscripcion
from grupos.models import Grupo, Horario, HORARIO_HORAS


@login_required
def inscribirse(request, grupo_id):
    if request.user.role != 'ESTUDIANTE':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=grupo_id)
    estudiante = request.user.perfil_estudiante

    if request.method != 'POST':
        return redirect('detalle_curso', id=grupo.curso_id)

    if not (grupo.activo and grupo.curso.activo):
        messages.error(request, 'Este grupo ya no está disponible.')
        return redirect('detalle_curso', id=grupo.curso_id)

    if grupo.cupo_disponible() <= 0:
        messages.error(request, 'Este grupo ya no tiene cupo disponible.')
        return redirect('detalle_curso', id=grupo.curso_id)

    if Inscripcion.objects.filter(estudiante=estudiante, grupo=grupo, activa=True).exists():
        messages.error(request, 'Ya estás inscrito en este grupo.')
        return redirect('detalle_curso', id=grupo.curso_id)

    horarios_nuevo = list(grupo.horarios.all())
    otras_inscripciones = estudiante.inscripciones.filter(activa=True).exclude(grupo=grupo)
    for insc in otras_inscripciones:
        for existente in insc.grupo.horarios.all():
            for nuevo in horarios_nuevo:
                if nuevo.dia_semana == existente.dia_semana \
                   and nuevo.hora_inicio < existente.hora_fin \
                   and nuevo.hora_fin > existente.hora_inicio:
                    messages.error(
                        request,
                        f"No puedes inscribirte: el horario de '{grupo.nombre}' "
                        f"choca con '{insc.grupo.nombre}', en el que ya estás inscrito."
                    )
                    return redirect('detalle_curso', id=grupo.curso_id)

    anterior = Inscripcion.todos.filter(estudiante=estudiante, grupo=grupo).first()
    if anterior:
        anterior.restaurar()
        anterior.activa = True
        anterior.save(update_fields=['activa'])
    else:
        Inscripcion.objects.create(estudiante=estudiante, grupo=grupo)

    return redirect('detalle_curso', id=grupo.curso_id)


@login_required
def horario_estudiante(request):
    if request.user.role != 'ESTUDIANTE':
        return redirect('inicio')

    estudiante = request.user.perfil_estudiante
    grupos_ids = estudiante.inscripciones.filter(activa=True).values_list('grupo_id', flat=True)
    horarios = Horario.objects.filter(grupo_id__in=grupos_ids).select_related('grupo')

    return render(request, 'inscripciones/horario.html', {
        'horarios': horarios,
        'dias': Horario.DiaSemana.choices,
        'horas': HORARIO_HORAS
    })
