from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from .forms import *

#models
from .models import *

# Create your views here.

#telas
@login_required(login_url='login')
def telas(request):
    telas = Tela.objects.all()
    return render(request, 'trazabilidad/telas/telas.html', {'telas': telas})

@login_required(login_url='login')
def agregar_tela(request):
    if request.method == "POST":
        form = TelaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tela agregada correctamente.")
            return redirect('telas')
    else:
        form = TelaForm()
    
    return render(request, 'trazabilidad/telas/form_tela.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
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

    return JsonResponse({"success": False, "error": "Método no permitido"})

#rollos
@login_required(login_url='login')
def rollos(request):
    rollos = RolloTela.objects.all()
    return render(request, 'trazabilidad/rollos/rollos.html', {'rollos': rollos})

@login_required(login_url='login')
def agregar_rollo(request):
    if request.method == 'POST':
        form = RolloTelaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rollo agregado correctamente.")
            return redirect('rollos')
    else:
        form = RolloTelaForm()
        
    return render(request, 'trazabilidad/rollos/form_rollo.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_rollo(request, rollo_id):
    rollo = get_object_or_404(RolloTela, id=rollo_id)
    
    if request.method == "POST":
        form = RolloTelaForm(request.POST, instance=rollo)
        if form.is_valid():
            form.save()
            messages.success(request, "Rollo actualizado correctamente.")
            return redirect('rollos')
    else:
        form = RolloTelaForm(instance=rollo)
    
    return render(request, 'trazabilidad/rollos/form_rollo.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def eliminar_rollo(request, rollo_id):
    if request.method == 'POST':
        rollo = get_object_or_404(RolloTela, id=rollo_id)
        rollo.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#Orden Producción
@login_required(login_url='login')
def ordenes_produccion(request):
    ordenes = OrdenProduccion.objects.all()
    return render(request, 'trazabilidad/ordenes_produccion/ordenes.html', {'ordenes': ordenes})

@login_required(login_url='login')
def agregar_orden(request):
    if request.method == 'POST':
        form = OrdenProduccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Orden de producción agregada correctamente.")
            return redirect('ordenes_produccion')
    else:
        form = OrdenProduccionForm()
        
    return render(request, 'trazabilidad/ordenes_produccion/form_orden.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_orden(request, orden_id):
    orden = get_object_or_404(OrdenProduccion, id=orden_id)
    
    if request.method == "POST":
        form = OrdenProduccionForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, "Orden de producción actualizada correctamente.")
            return redirect('ordenes_produccion')
    else:
        form = OrdenProduccionForm(instance=orden)
    
    return render(request, 'trazabilidad/ordenes_produccion/form_orden.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def eliminar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(OrdenProduccion, id=orden_id)
        orden.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

