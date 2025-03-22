from django.contrib import admin
from django.utils.html import format_html
from .models import Empresa, Area

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "nit", "telefono", "correo", "mostrar_logo")
    search_fields = ("razon_social", "nit", "correo")
    
    def mostrar_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.logo.url)
        return "(Sin logo)"
    
    mostrar_logo.short_description = "Logo"

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "empresa", "descripcion")
    search_fields = ("nombre", "empresa__razon_social")

