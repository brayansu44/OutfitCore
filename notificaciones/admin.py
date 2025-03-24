from django.contrib import admin
from .models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("user", "mensaje_resumido", "tipo", "leida", "fecha_creacion")
    list_filter = ("tipo", "leida", "fecha_creacion")
    search_fields = ("user__username", "mensaje")
    list_editable = ("leida",)
    readonly_fields = ("fecha_creacion",)

    def mensaje_resumido(self, obj):
        return obj.mensaje[:50] + "..." if len(obj.mensaje) > 50 else obj.mensaje

    mensaje_resumido.short_description = "Mensaje"

    def has_add_permission(self, request):
        """Evita que los usuarios agreguen notificaciones manualmente desde el admin."""
        return False
