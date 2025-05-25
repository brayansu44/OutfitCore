from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
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

    return render(request, 'nomina/SeguridadSocial.html', context)

@login_required(login_url='login')
def EPSadd(request):
    if request.method == "POST":
        form = EPSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "EPS agregada correctamente.")
            
        else:
            messages.success(request, "Registro Invalidado.")
    else:
        form = EPSForm()
        messages.error(request, "Validar el formato correctamente.") 

    return render(request, 'nomina/SeguridadSocial.html/step-1')

@login_required(login_url='login')
def EPSedit(request, eps_id):
    eps = get_object_or_404(EPS, id=eps_id)
    if request.method == "POST":
        form = EPSForm(request.POST, instance=eps)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de la EPS {eps.nombre} actualizada correctamente.")
            return render(request, 'nomina/SeguridadSocial.html/step-1')
        else:
            messages.success(request, "Actualización Invalidada.")
    else:
        form = EPSForm(instance=eps)
    
    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='login')
@require_POST
def EPSdelete(request, tela_id):
    if request.method == "POST":
        tela = get_object_or_404(EPS, id=tela_id)
        tela.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})
