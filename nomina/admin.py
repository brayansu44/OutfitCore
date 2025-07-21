from django.contrib import admin
from .models import EPS, ARL, Pension, CajaCompensacion, Contrato, Devengado, Deducciones, Provisiones, AportesParafiscal, Nomina

@admin.register(EPS, ARL, Pension, CajaCompensacion)
class SeguridadSocialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'correo')
    search_fields = ('nombre',)

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'empresa', 'local', 'eps', 'pension', 'arl', 'caja_compensacion', 'fecha_inicio', 'fecha_fin', 'salario')
    list_filter = ('empresa', 'eps', 'pension', 'arl')
    search_fields = ('perfil__nombre', 'empresa__nombre')

@admin.register(Devengado)
class DevengadoAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'total', 'auxilio_transporte', 'exonerado_aportes', 'dias_liquidados', 'horas_extras_diurna', 'horas_extras_nocturna', 'horas_extras_diurna_dominical', 'horas_extras_nocturna_dominical', 'recargos_nocturnos', 'recargos_dominical', 'recargos_nocturnos_dominical')
    list_filter = ('contrato',)

@admin.register(Deducciones)
class DeduccionesAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'salud', 'pension', 'fondo', 'retencion', 'otros')
    list_filter = ('contrato',)

@admin.register(Provisiones)
class ProvisionesAdmin(admin.ModelAdmin):
    list_display = ('nomina', 'total', 'pension', 'salud', 'prima', 'cesantias')
    list_filter = ('nomina',)

@admin.register(AportesParafiscal)
class AportesParafiscalAdmin(admin.ModelAdmin):
    list_display = ('nomina', 'sena', 'icbf', 'ccf', 'aporte_salud')
    list_filter = ('nomina',)

@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'fecha_liquidacion', 'contrato')
    list_filter = ('fecha_inicio', 'fecha_fin', 'contrato',)
