from django.contrib import admin
from .models import Tela, RolloTela, OrdenProduccion, CorteTela, TallaCorte, ComponenteCorte

# Register your models here.

@admin.register(Tela)
class TelaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'tipo', 'proveedor', 'ancho')
    search_fields = ('nombre', 'color', 'tipo', 'proveedor')
    list_filter = ('color', 'tipo', 'proveedor')

@admin.register(RolloTela)
class RolloTelaAdmin(admin.ModelAdmin):
    list_display = ('tela', 'largo_inicial', 'largo_restante', 'estado', 'fecha_registro')
    search_fields = ('tela__nombre',)
    list_filter = ('estado', 'fecha_registro')
    ordering = ('-fecha_registro',)  


@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'referencia', 'cortador', 'total_unidades', 'estado')
    search_fields = ('referencia', 'cortador__nombre')
    list_filter = ('fecha', 'estado')

@admin.register(CorteTela)
class CorteTelaAdmin(admin.ModelAdmin):
    readonly_fields = ('faltante_tela', 'rendimiento_rollo')
    list_display = ('orden', 'rollo', 'largo_utilizado', 'capas_cortadas', 'fecha_corte', 'responsable')
    search_fields = ('orden__referencia', 'rollo__tela__nombre', 'responsable__nombre')
    list_filter = ('fecha_corte',)

@admin.register(TallaCorte)
class TallaCorteAdmin(admin.ModelAdmin):
    list_display = ('corte', 'talla', 'cantidad')
    search_fields = ('corte__id', 'talla')
    list_filter = ('talla',)

@admin.register(ComponenteCorte)
class ComponenteCorteAdmin(admin.ModelAdmin):
    list_display = ('talla_corte', 'tipo_pieza', 'cantidad')
    search_fields = ('talla_corte__talla', 'tipo_pieza')
    list_filter = ('tipo_pieza',)