# EduControl — sistema de diseño

Fuente de verdad para color, tipografía, espaciado y componentes. Implementado en CSS
plano (sin Tailwind) para que cualquier plantilla de Django lo reuse sin duplicar reglas.

```
static/css/tokens.css   → variables (la paleta, tipografía, espaciado, sombras, motion)
static/css/app.css      → reset + componentes (botones, tabla, formulario, badge, nav...)
templates/base.html     → layout compartido (sidebar + topbar) que todas las páginas extienden
templates/_icons.html   → sprite de iconos SVG (<use href="#icon-x">), un solo set reusable
static/js/app.js        → único script: abre/cierra el menú lateral en móvil
```

Cualquier plantilla nueva hereda de `base.html` y usa estas clases — no se escriben
colores o fuentes sueltos en una plantilla.

## 1. Paleta

Los cuatro colores del brief son la base; el resto son tintes/sombras de **esos mismos
tres tonos** (no colores inventados), para que la paleta se sienta de una sola pieza.

| Token | Hex | Uso |
|---|---|---|
| `--violet-400` | `#7f56d9` | Acento, foco de inputs, enlaces en sidebar oscuro |
| `--violet-500` | `#4e4294` | Primario — botones, estado activo de navegación |
| `--violet-900` | `#1d2939` | Ink del brief — sidebar, texto más oscuro, ancla de los grises |
| `--slate-50…900` | — | Escala neutra con el mismo subtono frío de `#1d2939` (no gris puro) |

Violeta completo: `50 #f7f5fd · 100 #f0ebfa · 200 #dfd5f6 · 300 #c5b3ee · 400 #7f56d9 ·
500 #4e4294 · 600 #43397f · 700 #372e68 · 800 #333462 · 900 #1d2939`.

**Estados semánticos** (texto en tono 700 sobre fondo claro → ≥4.5:1 de contraste):
`--color-success #15803d`, `--color-warning #b45309`, `--color-danger #b91c1c`, cada uno
con su `-bg` y `-border` a juego. Se usan para: Activo/Inactivo, confirmaciones y errores
de formulario. El verde activo lleva un punto animado (`.badge-dot`) con pulso suave.

**Un mismo sistema, dos temperaturas**: administración y profesor usan `--slate-50` como
fondo de página (sobrio); el portal del estudiante usa `--surface-estudiante`
(`#fbf9fd`, violeta casi imperceptible) — mismo set de componentes, variable distinta.

## 2. Tipografía

- **Poppins** (500/600/700) para títulos — geométrica, amigable, con algo de carácter sin
  perder seriedad administrativa.
- **Open Sans** (400/600) para cuerpo de texto, tablas y formularios — alta legibilidad en
  bloques largos de datos.
- Base 16px, interlineado 1.5 en cuerpo / 1.25 en títulos. Nunca texto de body bajo 14px.

## 3. Espaciado, forma y elevación

Escala de 8px (`--space-1` 4px … `--space-8` 64px). Radios: `sm` 6px (inputs pequeños),
`md` 10px (botones, inputs), `lg` 16px (tarjetas). Sombras muy sutiles (`--shadow-sm/md`):
la jerarquía la da el borde + el espaciado, no sombras pesadas — así se mantiene sobrio en
modo "Operate".

## 4. Microinteracciones

Todo hover/focus transiciona en 150–200ms (`--duration-fast/base`), y se anula bajo
`prefers-reduced-motion`. Reglas fijas, no decoración suelta:

- Botones: fondo más oscuro al hover, `translateY(1px)` al presionar.
- Filas de tabla: fondo violeta muy claro al pasar el mouse (`--color-primary-soft`).
- Inputs: anillo de foco violeta (`--shadow-focus`) — visible también en navegación por
  teclado (`:focus-visible`).
- Badge "Activo": punto que pulsa — comunica "vivo" sin texto adicional.
- Tarjetas y tablas entran con `fade-up` (200ms) al cargar la página.
- Menú lateral en móvil: se desliza (`transform`), con scrim y cierre por `Esc`.

## 5. Iconos

Un solo sprite (`templates/_icons.html`) con `<symbol>` outline (trazo, sin relleno,
20–24px) en el estilo Heroicons/Phosphor. Se usan con `<svg class="icon"><use href="#icon-nombre"/></svg>`
— nunca emoji como icono. Todo icono junto a texto visible lleva `aria-hidden="true"` (el
texto ya lo describe); un icono solo en un botón necesita además una etiqueta accesible.

## 6. Componentes clave

- **`.btn`** — `btn-primary` (acción principal), `btn-outline` (secundaria), `btn-danger-ghost`
  (eliminar). Alto mínimo 44px (objetivo táctil).
- **`.table-card`** — tabla con cabecera sticky visual, fila con hover, y en <768px se
  convierte en tarjetas (`data-label` en cada `<td>`) en vez de scroll horizontal forzado.
- **`.badge`** — estado Activo/Inactivo; mismo patrón para futuros estados de asistencia
  (Presente/Retardo/Falta/Justificada) cuando se construya ese módulo.
- **`.card` / `.form-grid` / `.field`** — formularios con label siempre visible (nunca solo
  placeholder) y `.hint` para ayuda contextual (p. ej. "cupo máximo del grupo").
- **`.alert-danger`** — errores de formulario y de login, con icono + texto, nunca solo
  color.
- **Sidebar + topbar (`base.html`)** — navegación por rol: administración ve Cursos /
  Grupos / Estudiantes; profesor y estudiante ven su panel de inicio (sus módulos de
  navegación propia se añaden aquí cuando existan esas vistas).

## 7. Accesibilidad (no negociable)

Contraste ≥4.5:1 en texto, foco visible en todo elemento interactivo, objetivos táctiles
≥44px, `aria-hidden` en iconos decorativos, estados comunicados con texto + color (no solo
color), y diseño responsive probado en 375 / 768 / 1024 / 1440px.

## 8. Lo que falta a propósito

Asistencias, inscripciones, calendario y el resto del panel de profesor/estudiante no
tienen vistas en el código todavía — este rediseño no inventa esas pantallas, solo deja el
sistema (`tokens.css` + `app.css` + `base.html`) listo para que, cuando se construyan, se
vean consistentes desde el primer commit.
