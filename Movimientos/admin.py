from django.contrib import admin
from .models import Cuenta, CategoriaMercaderia, Ingreso, Egreso, RegistroContable

# Register your models here.
@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)

@admin.register(CategoriaMercaderia)
class CategoriaMercaderiaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'cuenta', 'categoria', 'cantidad', 'monto', 'mes', 'anio')
    list_filter = ('mes', 'anio', 'cuenta', 'categoria')
    search_fields = ('detalle', 'documento')
    date_hierarchy = 'fecha'

@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'cuenta', 'categoria', 'cantidad', 'monto', 'mes', 'anio')
    list_filter = ('mes', 'anio', 'cuenta', 'categoria')
    search_fields = ('detalle', 'factura_remision')
    date_hierarchy = 'fecha'

@admin.register(RegistroContable)
class RegistroContableAdmin(admin.ModelAdmin):
    list_display = ('cuenta', 'anio', 'mes', 'ingresos', 'gastos', 'saldo_mensual', 'saldo_acumulado')
    list_filter = ('anio', 'mes', 'cuenta')
    search_fields = ('cuenta__nombre',)
