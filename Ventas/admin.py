from django.contrib import admin
from .models import Ventas
# Register your models here.

#@admin.register(VentasAdmin)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('LocalID', 'Factura', 'Fecha', 'ClienteID')
    search_fields = ('LocalID', 'ClienteID')
    list_filter = ()


admin.site.register(Ventas, VentasAdmin)  