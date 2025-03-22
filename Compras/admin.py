from django.contrib import admin
from .models import Compras, Gastos_Operativos
# Register your models here.

#@admin.register(ComprasAdmin)
class ComprasAdmin(admin.ModelAdmin):
    list_display = ('Fecha', 'ProveedorID', 'UserResponsable', 'EmpresaID', 'Factura')
    search_fields = ()
    list_filter = ()

#@admin.register(Gastos_OperativosAdmin)
class Gastos_OperativosAdmin(admin.ModelAdmin):
    list_display = ('Fecha', 'Tipo_gasto', 'Factura', 'UserResponsable', 'Aprobador', 'EmpresaID')
    search_fields = ('EmpresaID', 'UserResponsable')
    list_filter = ()


admin.site.register(Compras, ComprasAdmin)  
admin.site.register(Gastos_Operativos, Gastos_OperativosAdmin)
