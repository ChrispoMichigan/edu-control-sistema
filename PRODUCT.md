# EduControl — contexto de producto

> Generado a partir del brief que acompaña este avance de proyecto. Donde el brief no
> especifica un detalle, se marca como **Supuesto**.

## Qué es

Plataforma web para un centro de capacitación: administra cursos, grupos (aperturas de
un curso con profesor, cupo y fechas), inscripciones de estudiantes y asistencia por clase.

## Para quién

Tres roles, cada uno con su propia vista:

- **Administración** — crea cursos y grupos, da de alta estudiantes, inscribe/da de baja.
- **Profesor** — pasa lista (asistencia) y consulta su calendario de clases. *(Módulo aún
  no implementado en código; el panel de inicio ya reserva su espacio.)*
- **Estudiante** — consulta su calendario, asistencia y resultados. *(Idem: pendiente de
  implementar.)*

## Objetivo

Que cada rol pueda hacer su parte sin fricción: administración ve ocupación y estado de
un vistazo, el profesor marca asistencia rápido, el estudiante entiende su progreso sin
vocabulario técnico.

## Stack

- Django 6.1 + SQLite (desarrollo). Plantillas server-rendered, sin framework de frontend.
- CSS propio con variables (sin Tailwind todavía — el plan original lo menciona, pero el
  código aún no lo integra). **Supuesto:** se mantiene así por ahora; migrar a Tailwind
  es un cambio aparte, no parte de este rediseño.
- API externa de festivos (API Ninjas) — **Supuesto:** no implementada aún, no afecta al
  sistema de diseño.

## Alcance ya construido (lo que este rediseño cubre)

Login, panel de inicio por rol, y CRUD de cursos / grupos / estudiantes (administración).
Asistencias, inscripciones y calendario existen como modelos/apps pero sin pantallas: el
rediseño no inventa pantallas para módulos que no existen todavía.

## Identidad visual

- Paleta fija dada por el brief: `#4e4294` `#7f56d9` `#1d2939` `#ffffff` — administración y
  profesorado en tono sobrio, portal del estudiante con el mismo sistema en un tono más
  cálido (fondo violeta muy suave en vez de gris neutro).
- Heurísticas de Nielsen ya señaladas en el brief (visibilidad de estado, lenguaje del
  usuario, control y libertad, consistencia, prevención de errores) gobiernan las
  decisiones de `DESIGN.md`.

## Modo de superficie

Operate (precisión y consistencia sobre expresión): es software de gestión de uso diario,
no una landing de conversión.
