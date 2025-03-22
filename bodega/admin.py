from django.contrib import admin
from .models import Ingresos_Producto, Salidas_Producto, Unidad_Medida, Tipo_insumo, Insumo, Ingresos_insumo, Uso_Insumo
# Register your models here.

#@admin.register(Ingresos_ProductoAdmin)
class Ingresos_ProductoAdmin(admin.ModelAdmin):
    list_display = ('Fecha', 'ProductoID', 'ProveedorID', 'Cantidad', 'UserResponsable', 'Estado')
    search_fields = ('ProductoID', 'UserResponsable')
    list_filter = ()

    #@admin.register(Salidas_ProductoAdmin)
class Salidas_ProductoAdmin(admin.ModelAdmin):
    list_display = ('Fecha', 'ProductoID', 'ProveedorID', 'Cantidad', 'UserResponsable', 'Estado', 'LocalID')
    search_fields = ('ProductoID', 'UserResponsable', 'LocalID')
    list_filter = ()

    #@admin.register(Unidad_MedidaAdmin)
class Unidad_MedidaAdmin(admin.ModelAdmin):
    list_display = ('Nombre',)
    search_fields = ()
    list_filter = ()

    #@admin.register(Tipo_insumoAdmin)
class Tipo_insumoAdmin(admin.ModelAdmin):
    list_display = ('Nombre',)
    search_fields = ()
    list_filter = ()

    #@admin.register(InsumoAdmin)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'Tipo_insumoID', 'Unidad_MedidaID', 'Cantidad', 'Estado')
    search_fields = ()
    list_filter = ()

    #@admin.register(Ingresos_insumoAdmin)
class Ingresos_insumoAdmin(admin.ModelAdmin):
    list_display = ("InsumoID", "Fecha", "Cantidad", "ProveedorID", "UserResponsable")
    search_fields = ('InsumoID', 'UserResponsable')
    list_filter = ()

    #@admin.register(Uso_InsumoAdmin)
class Uso_InsumoAdmin(admin.ModelAdmin):
    list_display = ('InsumoID', 'ProductoID', 'Fecha', 'Cantidad', 'Observaciones_Destino', 'UserResponsable')
    search_fields = ('InsumoID', 'UserResponsable')
    list_filter = ()

admin.site.register(Ingresos_Producto, Ingresos_ProductoAdmin)  
admin.site.register(Salidas_Producto, Salidas_ProductoAdmin)
admin.site.register(Unidad_Medida, Unidad_MedidaAdmin)
admin.site.register(Tipo_insumo, Tipo_insumoAdmin)
admin.site.register(Insumo, InsumoAdmin)
admin.site.register(Ingresos_insumo, Ingresos_insumoAdmin)
admin.site.register(Uso_Insumo, Uso_InsumoAdmin)