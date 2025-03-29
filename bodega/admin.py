from django.contrib import admin
from .models import (
    EntregaCorte, Stock, SalidaProducto, ConfirmacionRecepcion, 
    UnidadMedida, TipoInsumo, Insumo, IngresoInsumo, UsoInsumo, EntradaProducto
)
from .forms import SalidaProductoForm

@admin.register(EntregaCorte)
class EntregaCorteAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'producto', 'get_cantidad', 'user_responsable')
    list_filter = ('fecha', 'user_responsable')
    search_fields = ('producto__producto__nombre',) 
    date_hierarchy = 'fecha'

    def get_cantidad(self, obj):
        return obj.cantidad  
    get_cantidad.short_description = 'Cantidad'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('producto_variante', 'cantidad')
    search_fields = ('producto_variante__producto__nombre',)

@admin.register(SalidaProducto)
class SalidaProductoAdmin(admin.ModelAdmin):
    form = SalidaProductoForm
    list_display = ('fecha', 'producto', 'cantidad', 'user_responsable', 'local', 'estado', 'es_lavado')
    search_fields = ('producto__producto_variante__nombre', 'user_responsable__usuario__username')
    list_filter = ('estado', 'es_lavado')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)  # Obtener el formulario base
        class CustomForm(form):
            def __init__(self, *args, **inner_kwargs):
                inner_kwargs['request'] = request  # Pasar request correctamente
                super().__init__(*args, **inner_kwargs)
        return CustomForm
    
@admin.register(EntradaProducto)
class EntradaProductoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'salida', 'cantidad', 'user_responsable')
    search_fields = ('salida__producto_variante__nombre', 'user_responsable__usuario__username')
    list_filter = ('fecha',)
    autocomplete_fields = ["salida"]    
    
@admin.register(ConfirmacionRecepcion)
class ConfirmacionRecepcionAdmin(admin.ModelAdmin):
    list_display = ("salida", "user_encargado", "confirmado", "fecha_confirmacion")
    list_filter = ("confirmado",)
    actions = ["confirmar_recepcion"]

    def has_add_permission(self, request):
        """Evita que los usuarios puedan agregar nuevas confirmaciones."""
        return False

    def save_model(self, request, obj, form, change):
        if obj.confirmado and not obj.user_encargado:
            obj.user_encargado = request.user.perfilusuario  # Asigna el usuario logueado
        super().save_model(request, obj, form, change)

    @admin.action(description="Confirmar recepción")
    def confirmar_recepcion(self, request, queryset):
        for recepcion in queryset:
            if not recepcion.confirmado:
                recepcion.confirmado = True
                recepcion.user_encargado = request.user.perfilusuario  # Asigna usuario autenticado
                recepcion.save()

    confirmar_recepcion.short_description = "Confirmar recepción de productos"


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "abrev")
    search_fields = ("nombre", "abrev")

@admin.register(TipoInsumo)
class TipoInsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo_insumo", "unidad_medida", "stock_actual")
    list_filter = ("tipo_insumo", "unidad_medida")
    search_fields = ("nombre",)
    
    def stock_actual(self, obj):
        return obj.stock_actual
    stock_actual.short_description = "Stock Actual"

@admin.register(IngresoInsumo)
class IngresoInsumoAdmin(admin.ModelAdmin):
    list_display = ('insumo', 'cantidad', 'fecha', 'cantidad', 'proveedor', 'user_responsable', 'estado')
    list_filter = ('estado', 'fecha', 'proveedor')
    search_fields = ('insumo__nombre', 'proveedor__nombre')
    actions = ['marcar_como_completado']

    @admin.action(description="Marcar como Completado")
    def marcar_como_completado(self, request, queryset):
        queryset.update(estado='Completado')

@admin.register(UsoInsumo)
class UsoInsumoAdmin(admin.ModelAdmin):
    list_display = ("insumo", "producto", "cantidad", "uso_destino", "fecha", "user_responsable")
    list_filter = ("uso_destino",)
    search_fields = ("insumo__nombre", "producto__nombre", "user_responsable__nombre_completo")
    date_hierarchy = "fecha"
