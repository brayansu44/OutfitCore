from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('Razon_Social', 'Tipo_documento', 'Identificacion', 'Telefono', 'Correo', 'Ciudad', 'Fecha_Inicio_Actividad')
    search_fields = ('Razon_Social', 'Identificacion', 'Correo')
    list_filter = ('Ciudad', 'Tipo_documento')
    ordering = ('Razon_Social',)