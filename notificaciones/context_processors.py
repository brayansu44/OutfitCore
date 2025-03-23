from .models import Notificacion

def notificaciones_context(request):
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(user=request.user, leida=False).order_by('-fecha_creacion')
    else:
        notificaciones = []
    return {'notificaciones': notificaciones}
