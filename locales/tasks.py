from celery import shared_task
from datetime import datetime, timedelta
from .models import InventarioLocal, InventarioSemanal

@shared_task
def registrar_inventario_semanal():
    hoy = datetime.today().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())

    for inventario in InventarioLocal.objects.all():
        InventarioSemanal.objects.create(
            local=inventario.local,
            variante=inventario.variante,
            semana=inicio_semana,
            entradas=inventario.entradas,
            salidas=inventario.salidas,
            stock_final=inventario.stock_actual,
        )
    return "Inventario Semanal Registrado"
