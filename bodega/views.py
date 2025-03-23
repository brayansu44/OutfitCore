from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

# Vista del inventario de bodega
@login_required(login_url='login')
def inventario_bodega(request):
    stock = Stock.objects.all()
    return render(request, 'bodega/inventario-bodega.html', {'stock': stock})

# Vista de entradas de productos
@login_required(login_url='login')
def entradas_producto(request):
    entrega_corte = EntregaCorte.objects.all()
    return render(request, 'bodega/entradas-productos.html', {'entrega_corte': entrega_corte})

# Vista de salidas de productos
@login_required(login_url='login')
def salidas_producto(request):
    salida_producto = SalidaProducto.objects.all() 
    return render(request, 'bodega/salidas-productos.html', {'salida_producto': salida_producto}) 
