
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Clase, Festivo
from .services import obtener_festivos
from grupos.models import Grupo


@login_required
def lista_clases(request, grupo_id):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=grupo_id, profesor__usuario=request.user)
    clases = grupo.clases.all()

    return render(request, 'calendario/lista.html', {
        'grupo': grupo,
        'clases': clases
    })


@login_required
def crear_clase(request, grupo_id):
    if request.user.role != 'PROFESOR':
        return redirect('inicio')

    grupo = get_object_or_404(Grupo, id=grupo_id, profesor__usuario=request.user)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        anio = int(fecha[:4])
        obtener_festivos(anio)

        es_festivo = request.POST.get('es_festivo') == 'on'
        if not es_festivo:
            es_festivo = Festivo.objects.filter(fecha=fecha).exists()

        Clase.objects.create(
            grupo=grupo,
            fecha=fecha,
            hora_inicio=request.POST.get('hora_inicio'),
            hora_fin=request.POST.get('hora_fin'),
            tema=request.POST.get('tema'),
            observaciones=request.POST.get('observaciones'),
            es_festivo=es_festivo
        )

        return redirect('lista_clases', grupo_id=grupo.id)

    return render(request, 'calendario/formulario.html', {
        'grupo': grupo
    })
