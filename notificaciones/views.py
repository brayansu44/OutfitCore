from django.shortcuts import redirect, get_object_or_404
from .models import Notificacion
from django.contrib.auth.decorators import login_required

@login_required
def marcar_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, user=request.user)
    notificacion.leida = True
    notificacion.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def marcar_todas_leidas(request):
    Notificacion.objects.filter(user=request.user, leida=False).update(leida=True)
    return redirect(request.META.get("HTTP_REFERER", "/"))
