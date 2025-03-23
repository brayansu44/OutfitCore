from django.urls import path
from .views import marcar_leida, marcar_todas_leidas

urlpatterns = [
    path('notificacion/leida/<int:notificacion_id>/', marcar_leida, name='marcar_leida'),
    path('notificaciones/leidas/', marcar_todas_leidas, name='marcar_todas_leidas'),
]
