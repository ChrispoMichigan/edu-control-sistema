
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Curso, Seccion, Leccion, Progreso
from estudiantes.models import Estudiante


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
        Curso.objects.create(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            duracion_horas=request.POST.get('duracion_horas'),
            imagen=request.FILES.get('imagen')
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
        if request.FILES.get('imagen'):
            curso.imagen = request.FILES.get('imagen')
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
        curso.eliminar()

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


@login_required
def gestionar_contenido(request, curso_id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    curso = get_object_or_404(Curso, id=curso_id)
    secciones = curso.secciones.prefetch_related('lecciones')

    return render(request, 'cursos/contenido.html', {
        'curso': curso,
        'secciones': secciones
    })


@login_required
def crear_seccion(request, curso_id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        Seccion.objects.create(
            curso=curso,
            nombre=request.POST.get('nombre'),
            orden=request.POST.get('orden') or 0
        )

    return redirect('gestionar_contenido', curso_id=curso.id)


@login_required
def editar_seccion(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    seccion = get_object_or_404(Seccion, id=id)

    if request.method == 'POST':
        seccion.nombre = request.POST.get('nombre')
        seccion.orden = request.POST.get('orden') or 0
        seccion.save()

        return redirect('gestionar_contenido', curso_id=seccion.curso_id)

    return render(request, 'cursos/seccion_formulario.html', {
        'seccion': seccion
    })


@login_required
def eliminar_seccion(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    seccion = get_object_or_404(Seccion, id=id)
    curso_id = seccion.curso_id

    if request.method == 'POST':
        seccion.delete()

    return redirect('gestionar_contenido', curso_id=curso_id)


@login_required
def crear_leccion(request, seccion_id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    seccion = get_object_or_404(Seccion, id=seccion_id)

    if request.method == 'POST':
        Leccion.objects.create(
            seccion=seccion,
            titulo=request.POST.get('titulo'),
            texto=request.POST.get('texto', ''),
            orden=request.POST.get('orden') or 0
        )

    return redirect('gestionar_contenido', curso_id=seccion.curso_id)


@login_required
def editar_leccion(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    leccion = get_object_or_404(Leccion, id=id)

    if request.method == 'POST':
        leccion.titulo = request.POST.get('titulo')
        leccion.texto = request.POST.get('texto', '')
        leccion.orden = request.POST.get('orden') or 0
        leccion.save()

        return redirect('gestionar_contenido', curso_id=leccion.seccion.curso_id)

    return render(request, 'cursos/leccion_formulario.html', {
        'leccion': leccion
    })


@login_required
def eliminar_leccion(request, id):
    if request.user.role != 'ADMIN':
        return redirect('inicio')

    leccion = get_object_or_404(Leccion, id=id)
    curso_id = leccion.seccion.curso_id

    if request.method == 'POST':
        leccion.delete()

    return redirect('gestionar_contenido', curso_id=curso_id)


@login_required
def catalogo_cursos(request):
    if request.user.role != 'ESTUDIANTE':
        return redirect('inicio')

    q = request.GET.get('q', '').strip()
    cursos = Curso.objects.filter(activo=True)
    if q:
        cursos = cursos.filter(nombre__icontains=q)

    return render(request, 'cursos/catalogo.html', {
        'cursos': cursos.order_by('nombre'),
        'q': q
    })


@login_required
def detalle_curso(request, id):
    if request.user.role != 'ESTUDIANTE':
        return redirect('inicio')

    curso = get_object_or_404(Curso, id=id)
    estudiante = request.user.perfil_estudiante

    inscripcion = curso.grupos.filter(
        inscripciones__estudiante=estudiante,
        inscripciones__activa=True
    ).first()

    if inscripcion:
        secciones = curso.secciones.prefetch_related('lecciones')
        completadas_ids = set(
            Progreso.objects.filter(
                estudiante=estudiante, leccion__seccion__curso=curso, completado=True
            ).values_list('leccion_id', flat=True)
        )
        return render(request, 'cursos/detalle.html', {
            'curso': curso,
            'inscrito': True,
            'secciones': secciones,
            'completadas_ids': completadas_ids,
            'porcentaje': curso.progreso_para(estudiante)
        })

    grupos = curso.grupos.filter(activo=True).select_related('profesor__usuario').prefetch_related('horarios')
    return render(request, 'cursos/detalle.html', {
        'curso': curso,
        'inscrito': False,
        'grupos': grupos
    })


@login_required
def marcar_leccion(request, leccion_id):
    if request.user.role != 'ESTUDIANTE':
        return redirect('inicio')

    leccion = get_object_or_404(Leccion, id=leccion_id)
    estudiante = request.user.perfil_estudiante
    curso = leccion.seccion.curso

    inscrito = curso.grupos.filter(
        inscripciones__estudiante=estudiante,
        inscripciones__activa=True
    ).exists()

    if request.method == 'POST' and inscrito:
        progreso, _ = Progreso.objects.get_or_create(estudiante=estudiante, leccion=leccion)
        progreso.completado = not progreso.completado
        progreso.completado_en = timezone.now() if progreso.completado else None
        progreso.save()

    return redirect('detalle_curso', id=curso.id)
