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
    list_display = ('tela', 'metros_solicitados', 'largo_inicial', 'largo_restante', 'kilos', 'estado', 'fecha_registro')
    search_fields = ('tela__nombre', 'estado')
    list_filter = ('tela__nombre', 'estado', 'fecha_registro')
    ordering = ('-fecha_registro',) 
    readonly_fields = ('estado',) 


@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'referencia', 'cortador', 'total_unidades', 'estado')
    search_fields = ('referencia', 'cortador__full_name')
    list_filter = ('fecha', 'estado')

@admin.register(CorteTela)
class CorteTelaAdmin(admin.ModelAdmin):
    readonly_fields = ('faltante_tela', 'rendimiento_rollo')
    list_display = ('orden', 'rollo', 'largo_utilizado', 'capas_cortadas', 'fecha_corte', 'responsable')
    search_fields = ('orden__referencia', 'rollo__tela__nombre', 'responsable__full_name')
    list_filter = ('fecha_corte',)
    readonly_fields = ('fecha_corte', 'faltante_tela', 'rendimiento_rollo')

@admin.register(TallaCorte)
class TallaCorteAdmin(admin.ModelAdmin):
    list_display = ('corte', 'talla', 'cantidad')
    search_fields = ('corte__orden__referencia', 'talla')
    list_filter = ('talla',)

@admin.register(ComponenteCorte)
class ComponenteCorteAdmin(admin.ModelAdmin):
    list_display = ('talla_corte', 'tipo_pieza', 'cantidad')
    search_fields = ('talla_corte__corte__orden__referencia', 'talla_corte__talla', 'tipo_pieza')
    list_filter = ('tipo_pieza',)