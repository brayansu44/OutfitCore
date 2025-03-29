from django.urls import path
from .views import marcar_leida, marcar_todas_leidas, lista_notificaciones, gestionar_notificacion, contar_notificaciones_no_leidas

urlpatterns = [
    path('leida/<int:notificacion_id>/', marcar_leida, name='marcar_leida'),
    path('leidas/', marcar_todas_leidas, name='marcar_todas_leidas'),
    path("", lista_notificaciones, name="notificaciones"),
    path("gestionar/<int:notificacion_id>/", gestionar_notificacion, name="gestionar_notificacion"),
    path("contar_notificaciones/", contar_notificaciones_no_leidas, name="contar_notificaciones"),
]
