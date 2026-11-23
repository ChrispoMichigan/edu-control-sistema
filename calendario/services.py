import json
import urllib.request

from .models import Festivo

NAGER_URL = 'https://date.nager.at/api/v3/PublicHolidays/{anio}/MX'


def obtener_festivos(anio):
    cacheados = Festivo.objects.filter(fecha__year=anio)
    if cacheados.exists():
        return cacheados

    try:
        with urllib.request.urlopen(NAGER_URL.format(anio=anio), timeout=5) as resp:
            datos = json.loads(resp.read())
    except Exception:
        return Festivo.objects.none()

    Festivo.objects.bulk_create(
        [Festivo(fecha=d['date'], nombre=d['localName']) for d in datos],
        ignore_conflicts=True
    )
    return Festivo.objects.filter(fecha__year=anio)
