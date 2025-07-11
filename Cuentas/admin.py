from django.contrib import admin
from .models import Cliente, FacturaVenta, PagoRecibido, FacturaCompra, Pago

# Register your models here.
# ---- Módulo de Cuentas por Cobrar ----
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'identificacion', 'nombre', 'telefono', 'direccion')
    search_fields = ('identificacion', 'nombre',)

@admin.register(FacturaVenta)
class FacturaVentaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'saldo_pendiente')
    list_filter = ('fecha_emision', 'fecha_vencimiento')
    search_fields = ('numero_factura', 'cliente__nombre')
    ordering = ('-fecha_emision',)

@admin.register(PagoRecibido)
class PagoRecibidoAdmin(admin.ModelAdmin):
    list_display = ('factura', 'monto_pagado', 'fecha_pago', 'metodo_pago')
    list_filter = ('fecha_pago', 'metodo_pago')
    search_fields = ('factura__numero_factura', 'factura__cliente__nombre')

# ---- Módulo de Cuentas por Pagar ----
@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'proveedor', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'saldo_pendiente')
    list_filter = ('fecha_emision', 'fecha_vencimiento')
    search_fields = ('numero_factura', 'proveedor__nombre')
    ordering = ('-fecha_emision',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('factura', 'monto_pagado', 'fecha_pago', 'metodo_pago')
    list_filter = ('fecha_pago', 'metodo_pago')
    search_fields = ('factura__numero_factura', 'factura__proveedor__nombre')