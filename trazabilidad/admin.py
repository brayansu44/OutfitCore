from django.contrib import admin
from .models import Tela, RolloTela, OrdenProduccion, CorteTela, TallaCorte, RetazoTela

@admin.register(Tela)
class TelaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'proveedor')
    search_fields = ('nombre', 'proveedor__Razon_Social')
    list_filter = ('proveedor',)

@admin.register(RolloTela)
class RolloTelaAdmin(admin.ModelAdmin):
    list_display = ('numero_rollo', 'tela', 'color', 'metros_solicitados', 'largo_inicial', 'largo_restante', 'kilos', 'estado', 'fecha_registro')
    search_fields = ('numero_rollo', 'tela__nombre')
    list_filter = ('estado', 'fecha_registro')
    ordering = ('-fecha_registro',)
    readonly_fields = ('estado',)

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'producto', 'cortador', 'total_unidades', 'estado')
    search_fields = ('producto__referencia', 'cortador__usuario__full_name')
    list_filter = ('fecha', 'estado')
    autocomplete_fields = ['producto', 'cortador']

@admin.register(CorteTela)
class CorteTelaAdmin(admin.ModelAdmin):
    list_display = ('numero_corte', 'orden', 'rollo', 'largo_utilizado', 'capas_cortadas', 'fecha_corte', 'responsable')
    search_fields = ('numero_corte', 'orden__producto__referencia', 'rollo__tela__nombre', 'responsable__usuario__full_name')
    list_filter = ('fecha_corte',)
    autocomplete_fields = ['orden', 'rollo', 'responsable']
    readonly_fields = ('rendimiento_rollo', 'medida_tendido_mesa')

@admin.register(TallaCorte)
class TallaCorteAdmin(admin.ModelAdmin):
    list_display = ('corte', 'talla', 'cantidad')
    search_fields = ('corte__numero_corte', 'talla')
    list_filter = ('talla',)
    autocomplete_fields = ['corte']

@admin.register(RetazoTela)
class RetazoTelaAdmin(admin.ModelAdmin):
    list_display = (
        'rollo','orden','capas_cortadas',
        'metros_tendidos','colas','faltante',
        'medida_tendido_mesa','fecha_registro','responsable'
    )
    search_fields = (
        'rollo__numero_rollo',
        'orden__producto__referencia',
        'responsable__full_name'
    )
    list_filter = ('fecha_registro','responsable')
    readonly_fields = ('medida_tendido_mesa','faltante')
    autocomplete_fields = ('rollo','orden','responsable')
    ordering = ('-fecha_registro',)
