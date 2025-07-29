from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from .forms import *

# Create your views here.
from .models import *

@login_required(login_url = 'login')
def nomina(request):
    return render(request, 'nomina/nomina.html')

@login_required(login_url = 'login')
def Contratos(request):
    contrato     = Contrato.objects.all()

    context = {
        'contrato': contrato,
    }

    return render(request, 'nomina/contratos.html', context )

#NOMINA PERSONAL
@login_required(login_url = 'login')
def Nomina_personal(request):
    nomina     = Nomina.objects.all()
    # Filtrar perfil usando los contratos de la nómina
    perfil_contrato = Contrato.objects.filter(perfil__contrato__in=[nomina.contrato for nomina in nomina]) 

    context = {
        'nomina': nomina,
        'perfil': perfil_contrato,
    }

    return render(request, 'nomina/nomina_personal.html', context )

@login_required(login_url='login')
def agregar_nomina_personal(request):
    if request.method == 'POST':
        form = NominaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nomina agregada correctamente.")
            return redirect('Nomina_personal')
    else:
        form = NominaForm()

    context = {
        'form': form, 
        'accion': 'Agregar'
    }
        
    return render(request, 'nomina/form_nomina_personal.html', context)

@login_required(login_url='login')
def editar_nomina_personal(request, nomina_id):
    nomina = get_object_or_404(Nomina, id=nomina_id)
    
    if request.method == "POST":
        form = NominaForm(request.POST, instance=nomina)
        if form.is_valid():
            form.save()
            messages.success(request, "Nomina actualizada correctamente.")
            return redirect('Nomina_personal')
    else:
        form = NominaForm(instance=nomina)
    
    return render(request, 'nomina/form_nomina_personal.html', {'form': form, 'accion': 'Editar'})


@login_required(login_url = 'login')
def Parametrizacion(request):
    contrato = Contrato.objects.all()
    devengado = Devengado.objects.all()
    deducciones = Deducciones.objects.all()
    provisiones = Provisiones.objects.all()
    aportes = AportesParafiscal.objects.all() 
 
    context = {
        'contrato': contrato,
        'devengado': devengado,
        'deducciones': deducciones,
        'provisiones': provisiones,
        'aportes': aportes,
    }

    return render(request, 'nomina/Parametrizacion.html', context )

@login_required(login_url='login')
def devengado(request, user_id):
    contrato = Contrato.objects.filter(perfil=user_id) 
    devengado = get_object_or_404(Devengado)

    if request.method == "POST":
        form = DevengadoForm(request.POST, instance=devengado)
        if form.is_valid():
            form.save()
            msj = f"Datos devengado del usuario {devengado.nombre} actualizada correctamente."
            return JsonResponse({"success": True, "message": msj})
        else:
            return JsonResponse({"success": False, "message": "Actualización invalida."})
        
    # En caso de GET, devolver datos del registro
    data = {field.name: getattr(devengado, field.name) for field in devengado._meta.get_fields() if hasattr(devengado, field.name)}
    return JsonResponse({"success": True, "data": data})

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

#EPS
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
def EPSdelete(request, eps_id):
    if request.method == "POST":
        eps = get_object_or_404(EPS, id=eps_id)
        eps.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})

#ARL
@login_required(login_url='login')
def ARLadd(request):
    if request.method == "POST":
        form = ARLForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "ARL agregada correctamente."})
        else:
            return JsonResponse({"success": False, "message": "Registro invalidado."})
    return JsonResponse({"success": False, "message": "Validar el formato correctamente."})

@login_required(login_url='login')
def ARLedit(request, arl_id):
    arl = get_object_or_404(ARL, id=arl_id)

    if request.method == "POST":
        form = ARLForm(request.POST, instance=arl)
        if form.is_valid():
            form.save()
            msj = f"Datos de la EPS {arl.nombre} actualizada correctamente."
            return JsonResponse({"success": True, "message": msj})
        else:
            return JsonResponse({"success": False, "message": "Actualización invalida."})
        
    # En caso de GET, devolver datos del registro
    data = {field.name: getattr(arl, field.name) for field in arl._meta.get_fields() if hasattr(arl, field.name)}
    return JsonResponse({"success": True, "data": data})

@login_required(login_url='login')
@require_POST
def ARLdelete(request, arl_id):
    if request.method == "POST":
        arl = get_object_or_404(ARL, id=arl_id)
        arl.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})

#PENSION
@login_required(login_url='login')
def PENSIONadd(request):
    if request.method == "POST":
        form = PENSIONForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "PENSION agregada correctamente."})
        else:
            return JsonResponse({"success": False, "message": "Registro invalidado."})
    return JsonResponse({"success": False, "message": "Validar el formato correctamente."})

@login_required(login_url='login')
def PENSIONedit(request, pension_id):
    pension = get_object_or_404(Pension, id=pension_id)

    if request.method == "POST":
        form = PENSIONForm(request.POST, instance=pension)
        if form.is_valid():
            form.save()
            msj = f"Datos de la PENSION {pension.nombre} actualizada correctamente."
            return JsonResponse({"success": True, "message": msj})
        else:
            return JsonResponse({"success": False, "message": "Actualización invalida."})
        
    # En caso de GET, devolver datos del registro
    data = {field.name: getattr(pension, field.name) for field in pension._meta.get_fields() if hasattr(pension, field.name)}
    return JsonResponse({"success": True, "data": data})

@login_required(login_url='login')
@require_POST
def PENSIONdelete(request, pension_id):
    if request.method == "POST":
        pension = get_object_or_404(Pension, id=pension_id)
        pension.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})

#CAJA
@login_required(login_url='login')
def CAJAadd(request):
    if request.method == "POST":
        form = CAJAForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "CAJA agregada correctamente."})
        else:
            return JsonResponse({"success": False, "message": "Registro invalidado."})
    return JsonResponse({"success": False, "message": "Validar el formato correctamente."})

@login_required(login_url='login')
def CAJAedit(request, caja_id):
    caja = get_object_or_404(CajaCompensacion, id=caja_id)

    if request.method == "POST":
        form = CAJAForm(request.POST, instance=caja)
        if form.is_valid():
            form.save()
            msj = f"Datos de la CAJA {caja.nombre} actualizada correctamente."
            return JsonResponse({"success": True, "message": msj})
        else:
            return JsonResponse({"success": False, "message": "Actualización invalida."})
        
    # En caso de GET, devolver datos del registro
    data = {field.name: getattr(caja, field.name) for field in caja._meta.get_fields() if hasattr(caja, field.name)}
    return JsonResponse({"success": True, "data": data})

@login_required(login_url='login')
@require_POST
def CAJAdelete(request, caja_id):
    if request.method == "POST":
        caja = get_object_or_404(CajaCompensacion, id=caja_id)
        caja.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})

