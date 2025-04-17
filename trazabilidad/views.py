from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from .forms import *

#models
from .models import *

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

# Cortes
@login_required(login_url='login')
def cortes(request):
    cortes = CorteTela.objects.all()
    return render(request, 'trazabilidad/cortes/cortes.html', {'cortes': cortes})

@login_required(login_url='login')
def agregar_corte(request):
    if request.method == 'POST':
        form = CorteTelaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Corte agregado correctamente.")
            return redirect('cortes')
    else:
        form = CorteTelaForm()
        
    return render(request, 'trazabilidad/cortes/form_corte.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_corte(request, corte_id):
    corte = get_object_or_404(CorteTela, id=corte_id)
    
    if request.method == "POST":
        form = CorteTelaForm(request.POST, instance=corte)
        if form.is_valid():
            form.save()
            messages.success(request, "Corte actualizado correctamente.")
            return redirect('cortes')
    else:
        form = CorteTelaForm(instance=corte)
    
    return render(request, 'trazabilidad/cortes/form_corte.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def eliminar_corte(request, corte_id):
    if request.method == 'POST':
        corte = get_object_or_404(CorteTela, id=corte_id)
        corte.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# Tallas
@login_required(login_url='login')
def tallas(request):
    tallas = TallaCorte.objects.all()
    return render(request, 'trazabilidad/tallas/tallas.html', {'tallas': tallas})

@login_required(login_url='login')
def agregar_talla(request):
    if request.method == 'POST':
        form = TallaCorteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Talla agregada correctamente.")
            return redirect('tallas')
    else:
        form = TallaCorteForm()
        
    return render(request, 'trazabilidad/tallas/form_talla.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_talla(request, talla_id):
    talla = get_object_or_404(TallaCorte, id=talla_id)
    
    if request.method == "POST":
        form = TallaCorteForm(request.POST, instance=talla)
        if form.is_valid():
            form.save()
            messages.success(request, "Talla actualizada correctamente.")
            return redirect('tallas')
    else:
        form = TallaCorteForm(instance=talla)
    
    return render(request, 'trazabilidad/tallas/form_talla.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def eliminar_talla(request, talla_id):
    if request.method == 'POST':
        talla = get_object_or_404(TallaCorte, id=talla_id)
        talla.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# Retazos
@login_required(login_url='login')
def retazos(request):
    retazos = RetazoTela.objects.all()
    return render(request, 'trazabilidad/retazos/retazos.html', {'retazos': retazos})

@login_required(login_url='login')
def agregar_retazo(request):
    if request.method == 'POST':
        form = RetazoTelaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Retazo agregado correctamente.")
            return redirect('retazos')
    else:
        form = RetazoTelaForm()
        
    return render(request, 'trazabilidad/retazos/form_retazo.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_retazo(request, retazo_id):
    retazo = get_object_or_404(RetazoTela, id=retazo_id)
    
    if request.method == "POST":
        form = RetazoTelaForm(request.POST, instance=retazo)
        if form.is_valid():
            form.save()
            messages.success(request, "retazo actualizado correctamente.")
            return redirect('retazos')
    else:
        form = RetazoTelaForm(instance=retazo)
    
    return render(request, 'trazabilidad/retazos/form_retazo.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def eliminar_retazo(request, retazo_id):
    if request.method == 'POST':
        retazo = get_object_or_404(RetazoTela, id=retazo_id)
        retazo.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required(login_url='login')
def informe_cortes(request):
    cortes = CorteTela.objects.select_related(
        'rollo__tela',
        'orden',
    ).prefetch_related('tallas_cortes')

    data = []
    total_metros = 0
    total_capas = 0 
    total_tallas = 0

    for corte in cortes:
        tallas = corte.tallas_cortes.all()
        tallas_detalle = [f"{t.talla}: {t.cantidad}" for t in tallas]
        total_tallas_corte = sum(t.cantidad for t in tallas)
        total_tallas += total_tallas_corte

        capas = corte.capas_cortadas

        retazos_qs = RetazoTela.objects.filter(
            rollo=corte.rollo,
            orden=corte.orden
        )
        retazos_generados = [f"{r.metros_tendidos} m" for r in retazos_qs]

        total_metros += corte.largo_utilizado
        total_capas += capas  

        data.append({
            'numero_corte': corte.numero_corte,
            'fecha_corte': corte.fecha_corte,
            'rollo_numero': corte.rollo.numero_rollo,
            'tela_nombre': corte.rollo.tela.nombre,
            'rollo_color': corte.rollo.color,
            'largo_utilizado': corte.largo_utilizado,
            'tallas_detalle': tallas_detalle,
            'total_tallas': total_tallas_corte,
            'retazos_generados': retazos_generados,
            'capas': capas
        })

    return render(request, 'trazabilidad/informe_cortes.html', {
        'data': data,
        'total_metros': total_metros,
        'total_capas': total_capas,
        'total_tallas': total_tallas 
    })




