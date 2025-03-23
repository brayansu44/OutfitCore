from django.db import models
from django.contrib.auth import get_user_model
from usuarios.models import Usuario

User = get_user_model()

class Notificacion(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    mensaje = models.TextField()  # Cambio de CharField a TextField para evitar recortes
    tipo = models.CharField(
        max_length=20,
        choices=[
            ("salida", "Salida de Producto"),
            ("confirmacion", "Confirmación de Recepción"),
            ("otro", "Otro")
        ],
        default="otro"
    )
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.mensaje[:50]}..."

