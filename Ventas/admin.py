from django.contrib import admin
from .models import *

#@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('LocalID', 'FacturaID', 'Fecha')
    search_fields = ('LocalID', 'Factura')
    list_filter = ()

#@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('ventaID', 'productoID', 'cantidad', 'vr_unidad', 'vr_total', 'observacion')
    search_fields = ('ventaID', 'productoID')
    list_filter = ()

admin.site.register(Ventas, VentasAdmin)
admin.site.register(Item, ItemAdmin)