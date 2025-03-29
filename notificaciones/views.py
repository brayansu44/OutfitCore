from django.shortcuts import redirect, get_object_or_404, render
from .models import Notificacion
from django.contrib.auth.decorators import login_required
from bodega.models import ConfirmacionRecepcion
from .forms import ConfirmacionRecepcionForm 
from django.contrib import messages
from django.http import JsonResponse

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

@login_required
def contar_notificaciones_no_leidas(request):
    count = Notificacion.objects.filter(user=request.user, leida=False).count()
    return JsonResponse({"count": count})

@login_required
def lista_notificaciones(request):

    Notificacion.objects.filter(user=request.user, leida=False).update(leida=True)

    notificaciones = Notificacion.objects.filter(user=request.user)

    return render(request, "notificaciones/lista_notificaciones.html", {"notificaciones": notificaciones})

@login_required
def gestionar_notificacion(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, user=request.user)
    
    salida = notificacion.salida  

    if not salida:
        messages.error(request, "No se encontró una salida asociada.")
        return redirect("notificaciones")
    
    confirmacion, created = ConfirmacionRecepcion.objects.get_or_create(salida=salida)

    if request.method == "POST":
        form = ConfirmacionRecepcionForm(request.POST, instance=confirmacion)
        if form.is_valid():
            confirmacion = form.save(commit=False)
            confirmacion.salida = salida
            confirmacion.user_encargado = request.user.perfilusuario
            confirmacion.confirmado = True
            confirmacion.save(request=request)

            notificacion.delete()

            return redirect("notificaciones")
    else:
        form = ConfirmacionRecepcionForm()

    return render(request, "notificaciones/gestionar_notificacion.html", {
        "notificacion": notificacion,
        "form": form
    })


