from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.template.loader import render_to_string
from .forms import *

# Create your views here.
from .models import *

@login_required(login_url = 'login')
def Ventas(request):
    return render(request, 'cuentas/ventas/ventas.html')

@login_required(login_url = 'login')
def Compras(request):
    return render(request, 'cuentas/compras/compras.html')

#MODAL CONTENT
@login_required(login_url='login')
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({'success': True, 'id': cliente.id, 'nombre': str(cliente)})
        else:
            return JsonResponse({'success': False, 'form_html': render_to_string('cuentas/form_cliente.html', {'form': form}, request)})
    else:
        form = ClienteForm()
        return render(request, 'cuentas/form_cliente.html', {'form': form, 'accion':'Cliente'})
    
@login_required(login_url='login')
def addFacturaVenta(request):
    if request.method == 'POST':
        form = FacturaVentaForm(request.POST)
        if form.is_valid():
            factura = form.save()
            return JsonResponse({'success': True, 'id': factura.id, 'nombre': str(factura)})
        else:
            return JsonResponse({'success': False, 'form_html': render_to_string('cuentas/form_cliente.html', {'form': form}, request)})
    else:
        form = ClienteForm()
    
    context = {
        'form': form, 
        'accion': 'Factura',
        'now': timezone.now()
    }
    return render(request, 'cuentas/form_cliente.html', context)

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

    context = {
        'form': form, 
        'accion': 'Agregar',
        'now': timezone.now()
    }
        
    return render(request, 'cuentas/ventas/form_factura_venta.html', context)

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

@login_required(login_url='login')
@require_POST
def delete_factura_venta(request, factura_id):
    if request.method == "POST":
        factura = get_object_or_404(FacturaVenta, id=factura_id)
        factura.delete()
        msj = f"Factura {factura.numero_factura} eliminada correctamente."
        return JsonResponse({"success": True, "message": msj})

    return JsonResponse({"success": False, "error": "Método no permitido"})

# PAGO RECIBIDO DE VENTA
@login_required(login_url = 'login')
def Pago_venta(request):
    pago     = PagoRecibido.objects.all()

    return render(request, 'cuentas/ventas/pago_venta.html', {'pago':pago})

@login_required(login_url='login')
def agregar_pago_venta(request):
    if request.method == 'POST':
        form = PagoVentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pago recibido añadido correctamente.")
            return redirect('pago_venta')
    else:
        form = PagoVentaForm()

    context = {
        'form': form, 
        'accion': 'Agregar',
        'now': timezone.now()
    }
        
    return render(request, 'cuentas/ventas/form_pago_venta.html', context)

@login_required(login_url='login')
def editar_pago_venta(request, pago_id):
    pago = get_object_or_404(PagoRecibido, id=pago_id)
    
    if request.method == "POST":
        form = PagoVentaForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request, "Pago actualizado correctamente.")
            return redirect('pago_venta')
    else:
        form = PagoVentaForm(instance=pago)
    
    return render(request, 'cuentas/ventas/form_factura_venta.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def delete_pago_venta(request, pago_id):
    if request.method == "POST":
        pago = get_object_or_404(PagoRecibido, id=pago_id)
        pago.delete()
        msj = f"Factura {pago.numero_factura} eliminada correctamente."
        return JsonResponse({"success": True, "message": msj})

    return JsonResponse({"success": False, "error": "Método no permitido"})
