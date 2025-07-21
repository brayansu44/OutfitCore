from django.contrib import admin
from .models import Cliente, FacturaVenta, PagoRecibido, FacturaCompra, Pago

# Register your models here.
# ---- Módulo de Cuentas por Cobrar ----
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_identificacion', 'identificacion', 'nombre', 'telefono', 'direccion')
    search_fields = ('identificacion', 'nombre',)

@admin.register(FacturaVenta)
class FacturaVentaAdmin(admin.ModelAdmin):
    readonly_fields = ('numero_factura', 'fecha_emision')
    list_display = ('numero_factura', 'cliente', 'fecha_emision', 'monto_total', 'saldo_pendiente')
    list_filter = ('fecha_emision', 'numero_factura')
    search_fields = ('numero_factura', 'cliente__tipo_identificacion', 'cliente__identificacion')
    ordering = ('-fecha_emision',)

@admin.register(PagoRecibido)
class PagoRecibidoAdmin(admin.ModelAdmin):
    list_display = ('factura', 'monto_pagado', 'fecha_pago', 'metodo_pago')
    list_filter = ('fecha_pago', 'metodo_pago')
    search_fields = ('factura__numero_factura', 'factura__cliente__nombre')

# ---- Módulo de Cuentas por Pagar ----
@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):
    readonly_fields = ('numero_factura', 'fecha_emision')
    list_display = ('numero_factura', 'proveedor', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'saldo_pendiente', 'estado')
    list_filter = ('fecha_emision', 'fecha_vencimiento', 'numero_factura')
    search_fields = ('numero_factura', 'proveedor__nombre')
    ordering = ('-fecha_emision',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('factura', 'monto_pagado', 'fecha_pago', 'metodo_pago')
    list_filter = ('fecha_pago', 'metodo_pago')
    search_fields = ('factura__numero_factura', 'factura__proveedor__nombre')
