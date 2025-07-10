from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse

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

@login_required(login_url = 'login')
def Factura_venta(request):
    factura     = FacturaVenta.objects.all()

    return render(request, 'cuentas/ventas/factura_venta.html', {'factura':factura})

@login_required(login_url = 'login')
def Pago_venta(request):
    pago     = PagoRecibido.objects.all()

    return render(request, 'cuentas/ventas/pago_venta.html', {'pago':pago})