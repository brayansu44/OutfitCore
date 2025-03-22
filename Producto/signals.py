from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Producto, ProductoVariante

@receiver(m2m_changed, sender=Producto.color.through)
@receiver(m2m_changed, sender=Producto.talla.through)
@receiver(m2m_changed, sender=Producto.diseno.through)
def crear_variantes_producto(sender, instance, action, **kwargs):
    """
    Cada vez que se agregan o eliminan colores, tallas o diseños, 
    se generan automáticamente las combinaciones en ProductoVariante.
    """
    if action in ["post_add", "post_remove", "post_clear"]: 
        # Borrar variantes existentes para evitar duplicados
        ProductoVariante.objects.filter(producto=instance).delete()

        # Obtener las combinaciones de colores, tallas y diseños
        colores = list(instance.color.all())
        tallas = list(instance.talla.all())
        disenos = list(instance.diseno.all()) or [None]  # Puede no haber diseño

        # Crear nuevas variantes
        variantes_creadas = []
        for color in colores:
            for talla in tallas:
                for diseno in disenos:
                    variante, creada = ProductoVariante.objects.get_or_create(
                        producto=instance,
                        color=color,
                        talla=talla,
                        diseno=diseno
                    )
                    variantes_creadas.append(variante)

        print(f"📌 {len(variantes_creadas)} variantes creadas para {instance.referencia}")
