
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asistencia
from calendario.models import Clase


@login_required
def tomar_asistencia(request, clase_id):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    clase = get_object_or_404(Clase, id=clase_id, grupo__profesor__usuario=request.user)
    inscripciones = clase.grupo.inscripciones.filter(activa=True).select_related('estudiante__usuario')

    if request.method == 'POST':
        for insc in inscripciones:
            Asistencia.objects.update_or_create(
                inscripcion=insc,
                fecha=clase.fecha,
                defaults={
                    'estado': request.POST.get(f'estado_{insc.id}', Asistencia.Estados.PRESENTE),
                    'observaciones': request.POST.get(f'observaciones_{insc.id}', '')
                }
            )

        return redirect('lista_clases', grupo_id=clase.grupo_id)

    registros = {
        a.inscripcion_id: a
        for a in Asistencia.objects.filter(inscripcion__in=inscripciones, fecha=clase.fecha)
    }

    filas = [
        {'inscripcion': insc, 'asistencia': registros.get(insc.id)}
        for insc in inscripciones
    ]

    return render(request, 'asistencias/formulario.html', {
        'clase': clase,
        'filas': filas,
        'estados': Asistencia.Estados.choices
    })
