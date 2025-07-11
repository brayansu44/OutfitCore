from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from .forms import *

# Create your views here.
from .models import *

@login_required(login_url = 'login')
def Ventas(request):
    factura     = FacturaVenta.objects.all()
    pago        = PagoRecibido.objects.all()

    context = {
        'factura': factura,
        'pago': pago,
    }

    return render(request, 'cuentas/ventas/ventas.html', context)

@login_required(login_url = 'login')
def Compras(request):
    factura     = FacturaCompra.objects.all()
    pago        = Pago.objects.all()

    context = {
        'factura': factura,
        'pago': pago,
    }

    return render(request, 'cuentas/compras/compras.html', context)

#FACTURA DE VENTA
@login_required(login_url = 'login')
def Factura_venta(request):
    factura     = FacturaVenta.objects.all()

    return render(request, 'cuentas/ventas/factura_venta.html', {'factura':factura})

@login_required(login_url='login')
def agregar_factura_venta(request):
    if request.method == 'POST':
        form = FacturaVentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Factura agregada correctamente.")
            return redirect('factura_venta')
    else:
        form = FacturaVentaForm()
        
    return render(request, 'cuentas/ventas/form_factura_venta.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_factura_venta(request, factura_id):
    factura = get_object_or_404(FacturaVenta, id=factura_id)
    
    if request.method == "POST":
        form = FacturaVentaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            messages.success(request, "Factura actualizada correctamente.")
            return redirect('factura_venta')
    else:
        form = FacturaVentaForm(instance=factura)
    
    return render(request, 'cuentas/ventas/form_factura_venta.html', {'form': form, 'accion': 'Editar'})

# PAGO RECIBIDO DE VENTA
@login_required(login_url = 'login')
def Pago_venta(request):
    pago     = PagoRecibido.objects.all()

    return render(request, 'cuentas/ventas/pago_venta.html', {'pago':pago})
