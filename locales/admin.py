from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(DiasFuncionamiento)
class DiasFuncionamientoAdmin(admin.ModelAdmin):
    list_display = ("dia", "get_dia_display")
    ordering = ("dia",)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "empresa", "telefono", "direccion", "mostrar_horario")
    search_fields = ("nombre", "empresa__razon_social", "direccion")
    filter_horizontal = ("Horario_habil",)

    def mostrar_horario(self, obj):
        return ", ".join([dia.get_dia_display() for dia in obj.Horario_habil.all()])
    
    mostrar_horario.short_description = "Días de funcionamiento"

@admin.register(InventarioLocal)
class InventarioLocalAdmin(admin.ModelAdmin):
    list_display = ('local', 'variante', 'entradas', 'salidas', 'stock_actual')
    list_filter = ('local', 'variante__producto', 'fecha')  
    search_fields = ('local__nombre', 'variante__producto__referencia', 'variante__color__nombre', 'variante__talla__nombre')
    ordering = ('-fecha',)
    readonly_fields = ('stock_actual', 'fecha') 

    fieldsets = (
        ('Información del Local', {
            'fields': ('local', 'variante')
        }),
        ('Movimientos de Stock', {
            'fields': ('entradas', 'salidas', 'stock_actual')
        }),
        ('Fecha de Registro', {
            'fields': ('fecha',)
        }),
    )


@admin.register(InventarioSemanal)
class InventarioSemanalAdmin(admin.ModelAdmin):
    list_display = ('local', 'variante', 'semana', 'entradas', 'salidas', 'stock_final')
    list_filter = ('local', 'semana')
    search_fields = ('local__nombre', 'variante__producto__referencia')
    ordering = ('-semana', 'local')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('local', 'variante', 'variante__producto')