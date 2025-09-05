# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse

from .forms import VentaForm, DetalleVentasFormSet
from .models import Ventas, DetalleVentas
from locales.models import Local, InventarioLocal
from Producto.models import ProductoVariante

@login_required(login_url='login')
def lista_ventas(request):
    ventas = Ventas.objects.all().order_by('-fecha').prefetch_related('detalles')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

def obtener_variantes_por_local(request):
    local_id = request.GET.get("local_id")
    variantes = []

    if local_id:
        inventarios = InventarioLocal.objects.filter(local_id=local_id).select_related("variante", "variante__producto")
        for inv in inventarios:
            variantes.append({
                "id": inv.variante.id,
                "nombre": f"{inv.variante.producto.referencia} - {inv.variante.color} - {inv.variante.talla}",
                "stock": inv.stock_actual
            })

    return JsonResponse({"variantes": variantes})


@login_required(login_url='login')
def crear_venta(request):
    if request.method == 'POST':
        print(request.POST)
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            local = venta.local

            venta.save()  # 👈 guardamos primero la venta

            formset = DetalleVentasFormSet(
                request.POST,
                instance=venta,
                prefix="detalles",
                local=local
            )

            if formset.is_valid():
                formset.save()
                return redirect('lista_ventas')
            else:
                print("ERRORES EN FORMSET", formset.errors)
        else:
            print("ERRORES EN FORMULARIO PRINCIPAL", form.errors)
    else:
        form = VentaForm()
        formset = DetalleVentasFormSet(instance=None, prefix="detalles", local=None)


    return render(request, 'ventas/form_venta.html', {
        'form': form,
        'formset': formset,
        'accion': 'Crear',
    })


@login_required(login_url='login')
def venta_detalle(request, pk):
    venta = get_object_or_404(Ventas, pk=pk)
    detalles = venta.detalles.all()  # Todos los productos de la venta
    factura = venta.factura
    pagos = factura.pagorecibido_set.all() if factura else []

    context = {
        'venta': venta,
        'detalles': detalles,
        'factura': factura,
        'pagos': pagos,
    }
    return render(request, 'ventas/venta_detalle.html', context)


