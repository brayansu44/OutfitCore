from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from .forms import *

from .models import Producto

@login_required(login_url='login')
def productos(request):
    productos = Producto.objects.prefetch_related('talla', 'color').all()
    return render(request, 'productos/productos.html', {'productos': productos})

@login_required(login_url='login')
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto agregado correctamente.")
            return redirect('productos')
    else:
        form = ProductoForm()
    
    return render(request, 'productos/form_producto.html', {'form': form, 'accion': 'Agregar'})

'''@login_required(login_url='login')
def editar_tela(request, tela_id):
    tela = get_object_or_404(Tela, id=tela_id)
    
    if request.method == "POST":
        form = TelaForm(request.POST, instance=tela)
        if form.is_valid():
            form.save()
            messages.success(request, "Tela actualizada correctamente.")
            return redirect('telas')
    else:
        form = TelaForm(instance=tela)
    
    return render(request, 'trazabilidad/telas/form_tela.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def eliminar_tela(request, tela_id):
    if request.method == "POST":
        tela = get_object_or_404(Tela, id=tela_id)
        tela.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})'''
