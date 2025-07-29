from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Nomina, Provisiones, AportesParafiscal

@receiver(post_save, sender=Nomina)
def actualizar_aportes_y_provisiones(sender, instance, **kwargs):
    contrato = instance.contrato

    # Aportes
    aportes, _ = AportesParafiscal.objects.get_or_create(nomina=instance)
    aportes.save()  # recalcula el total usando .save() y calcular_total()

    # Provisiones
    provisiones, _ = Provisiones.objects.get_or_create(
        nmoina=contrato,
        aportes_parafiscal=aportes
    )
    provisiones.save()  # recalcula el total
