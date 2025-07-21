from django.contrib import admin
from .models import *

#@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('local', 'fecha', 'estado', 'vendedor')
    search_fields = ('local', 'estado')
    list_filter = ()

#@admin.register(Item)
class DetalleVentasAdmin(admin.ModelAdmin):
    list_display = ('venta', 'variante', 'cantidad', 'vr_unidad', 'vr_total', 'observacion')
    search_fields = ('venta', 'variante')
    list_filter = ()

admin.site.register(Ventas, VentasAdmin)
admin.site.register(DetalleVentas, DetalleVentasAdmin)