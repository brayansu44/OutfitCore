from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.db import models
from .models import Ventas, DetalleVentas
from Cuentas.models import FacturaVenta, PagoRecibido

@receiver(post_save, sender=DetalleVentas)
def crear_factura_y_pago(sender, instance, created, **kwargs):
    venta = instance.venta

    # solo si la venta no tiene factura
    if venta.factura is None:
        def _create():
            # 1. Calcular total sumando todos los detalles
            total = venta.detalles.aggregate(total=models.Sum('vr_total'))['total'] or 0

            # 2. Crear la factura
            factura = FacturaVenta.objects.create(
                cliente=venta.cliente,
                monto_total=total,
            )

            # 3. Asociar la factura a la venta
            Ventas.objects.filter(pk=venta.pk).update(factura=factura)

            # 4. Crear PagoRecibido si la venta tiene metodo_pago
            if hasattr(venta, 'metodo_pago') and venta.metodo_pago:
                PagoRecibido.objects.create(
                    factura=factura,
                    monto_pagado=total,
                    metodo_pago=venta.metodo_pago
                )
                # 5. Actualizar estado de la venta a PAGADA
                Ventas.objects.filter(pk=venta.pk).update(estado='PAGADA')

        transaction.on_commit(_create)
