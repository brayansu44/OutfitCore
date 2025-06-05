from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import *

# Create your views here.
from .models import Nomina, EPS, ARL, Pension, CajaCompensacion

@login_required(login_url = 'login')
def nomina(request):
    nomina        = Nomina.objects.all()

    return render(request, 'nomina/nomina.html', {'nomina': nomina})

@login_required(login_url = 'login')
def SeguridadSocial(request, tab_id):
    eps     = EPS.objects.all()
    arl     = ARL.objects.all()
    pension = Pension.objects.all()
    cajacompensacion = CajaCompensacion.objects.all()

    EPSform = EPSForm()

    context = {
        'tab_id': tab_id,
        'eps': eps,
        'arl': arl,
        'pension': pension,
        'cajacompensacion': cajacompensacion,
        'form': EPSform,

    }

    return render(request, 'nomina/SeguridadSocial.html', context )

@login_required(login_url='login')
def EPSadd(request):
    if request.method == "POST":
        form = EPSForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "EPS agregada correctamente."})
        else:
            return JsonResponse({"success": False, "message": "Registro invalidado."})
    return JsonResponse({"success": False, "message": "Validar el formato correctamente."})

@login_required(login_url='login')
def EPSedit(request, eps_id):
    eps = get_object_or_404(EPS, id=eps_id)

    if request.method == "POST":
        form = EPSForm(request.POST, instance=eps)
        if form.is_valid():
            form.save()
            msj = f"Datos de la EPS {eps.nombre} actualizada correctamente."
            return JsonResponse({"success": True, "message": msj})
        else:
            return JsonResponse({"success": False, "message": "Actualización invalida."})
        
    # En caso de GET, devolver datos del registro
    data = {field.name: getattr(eps, field.name) for field in eps._meta.get_fields() if hasattr(eps, field.name)}
    return JsonResponse({"success": True, "data": data})

@login_required(login_url='login')
@require_POST
def EPSdelete(request, tela_id):
    if request.method == "POST":
        tela = get_object_or_404(EPS, id=tela_id)
        tela.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})
