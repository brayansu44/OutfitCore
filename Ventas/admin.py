from django.contrib import admin
from .models import Ventas, DetalleVentas

# Inline para manejar los detalles dentro de la venta
class DetalleVentasInline(admin.TabularInline):
    model = DetalleVentas
    extra = 1  # número de filas vacías para añadir
    fields = ("variante", "cantidad", "vr_unidad", "descuento_item", "vr_total", "iva_item", "ganancia_item")
    readonly_fields = ("vr_total", "iva_item", "ganancia_item")  # estos se calculan en el save

# Admin de Ventas
@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "fecha",
        "local",
        "cliente",
        "vendedor",
        "subtotal",
        "descuento_total",
        "iva",
        "ganancia",
        "estado",
    )
    list_filter = ("estado", "metodo_pago", "local", "fecha")
    search_fields = ("codigo", "cliente__nombre", "vendedor__user__username")
    inlines = [DetalleVentasInline]
    readonly_fields = ("subtotal", "descuento_total", "iva", "ganancia", "creado_en", "actualizado_en")

# Admin de DetalleVentas (opcional, si quieres verlo suelto)
@admin.register(DetalleVentas)
class DetalleVentasAdmin(admin.ModelAdmin):
    list_display = ("venta", "variante", "cantidad", "vr_unidad", "vr_total", "iva_item", "ganancia_item")
    search_fields = ("venta__codigo", "variante__producto__nombre")
    list_filter = ("venta__local",)
    readonly_fields = ("vr_total", "iva_item", "ganancia_item")
