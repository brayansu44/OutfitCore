from celery import shared_task
from datetime import datetime, timedelta
from .models import InventarioLocal, InventarioSemanal

@shared_task
def registrar_inventario_semanal():
    hoy = datetime.today().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())

    registros_creados = 0

    for inventario in InventarioLocal.objects.all():
        ya_existe = InventarioSemanal.objects.filter(
            local=inventario.local,
            variante=inventario.variante,
            semana=inicio_semana
        ).exists()

        if not ya_existe:
            InventarioSemanal.objects.create(
                local=inventario.local,
                variante=inventario.variante,
                semana=inicio_semana,
                entradas=inventario.entradas,
                salidas=inventario.salidas,
                stock_final=inventario.stock_actual,
            )
            registros_creados += 1

    return f"Inventario semanal registrado. Total: {registros_creados}"
