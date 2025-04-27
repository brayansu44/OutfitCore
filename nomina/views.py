from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

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

    context = {
        'tab_id': tab_id,
        'eps': eps,
        'arl': arl,
        'pension': pension,
        'cajacompensacion': cajacompensacion,
    }

    return render(request, 'nomina/SeguridadSocial.html', context)

def Register_EPS(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_eps')
        direccion = request.POST.get('direccion_eps')
        telefono = request.POST.get('telefono_eps')
        estado = request.POST.get('estado_eps')
        correo = request.POST.get('correo_eps')

        if nombre and telefono and correo and estado and direccion:
            Register_EPS = EPS(
                nombre=nombre,
                telefono=telefono,
                correo=correo,
                estado=estado,
                direccion=direccion
            )
            Register_EPS.save()
            messages.success(request,"Registro exitoso.")
        else:
            messages.error(request, "Diligenciar los campos correctamente.")

    return render(request, 'SeguridadSocial.html')