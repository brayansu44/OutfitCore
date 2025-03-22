from django.contrib import admin
from .models import Proveedor, Compra, DetalleCompra, GastosOperativos

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha_compra", "proveedor", "total_compra", "responsable")
    search_fields = ("proveedor__nombre", "responsable__username")
    list_filter = ("fecha_compra",)
    date_hierarchy = "fecha_compra"

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ("compra", "tipo", "cantidad_comprada", "precio_unitario", "sub_total")
    search_fields = ("compra__proveedor__nombre", "tipo")
    list_filter = ("tipo",)
    
    def sub_total(self, obj):
        return obj.sub_total  # Propiedad calculada
    sub_total.short_description = "Subtotal"

@admin.register(GastosOperativos)
class GastosOperativosAdmin(admin.ModelAdmin):
    list_display = ("fecha", "tipo", "monto", "responsable")
    search_fields = ("tipo", "responsable__username")
    list_filter = ("tipo", "fecha")
    date_hierarchy = "fecha"
