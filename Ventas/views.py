# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .forms import VentaForm, DetalleVentasFormSet
from .models import Ventas, DetalleVentas

@login_required(login_url='login')
def lista_ventas(request):
    ventas = Ventas.objects.all().order_by('-fecha')  # Ordenar por fecha descendente
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})


@login_required(login_url='login')
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = DetalleVentasFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            venta = form.save()
            formset.instance = venta  # Asocia los detalles a la venta
            formset.save()

            return redirect('lista_ventas')
        else:
            print("ERRORES EN FORMULARIOS")
            print(form.errors)
            print(formset.errors)
    else:
        form = VentaForm()
        formset = DetalleVentasFormSet()

    return render(request, 'ventas/form_venta.html', {
        'form': form,
        'formset': formset,
        'accion': 'Crear',
    })
