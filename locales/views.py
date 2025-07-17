from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Sum, Max
from django.contrib import messages

from locales.models import Local, InventarioLocal, InventarioSemanal
from Producto.models import Producto
from .forms import LocalForm, InventarioLocalForm

import io, os
from django.conf import settings
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import InventarioLocal

from django.utils.timezone import now
from django.utils.dateparse import parse_date

# Create your views here.

@login_required(login_url='login') 
def locales(request): 
    empresa_id = request.session.get('empresa_id')
    if empresa_id:
        locales_with_empresa = Local.objects.filter(empresa_id=empresa_id) 
        return render(request, 'locales/locales.html', {'locales': locales_with_empresa})
    else:
        locales = Local.objects.all()
        return render(request, 'locales/locales.html', {'locales': locales})
    
@login_required(login_url='login')
def agregar_local(request):
    if request.method == "POST":
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Local agregado correctamente.")
            return redirect('locales')
    else:
        form = LocalForm()

    return render(request, 'locales/form_local.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)

    if request.method == "POST":
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            messages.success(request, "Local actualizado correctamente.")
            return redirect('locales')
    else:
        form = LocalForm(instance=local)

    return render(request, 'locales/form_local.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
@require_POST
def eliminar_local(request, local_id):
    if request.method == "POST":
        local = get_object_or_404(Local, id=local_id)
        local.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url = 'login')
def inventario_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)
    inventario = InventarioLocal.objects.filter(local=local).select_related('variante__producto')

    context = {
        'local': local,
        'inventario': inventario,
    }

    return render(request, 'locales/inventario-local.html', context)

@login_required(login_url='login')
def agregar_movimiento_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)

    if request.method == 'POST':
        form = InventarioLocalForm(request.POST)
        if form.is_valid():
            variante = form.cleaned_data['variante']
            entradas = form.cleaned_data['entradas']
            salidas = form.cleaned_data['salidas']

            try:
                inventario = InventarioLocal.objects.get(local=local, variante=variante)
                # Actualiza entradas y salidas existentes
                inventario.entradas += entradas
                inventario.salidas += salidas
                inventario.stock_actual = inventario.entradas - inventario.salidas
                inventario.save()
                messages.success(request, 'Inventario actualizado correctamente.')
            except InventarioLocal.DoesNotExist:
                # Crea un nuevo registro
                inventario = form.save(commit=False)
                inventario.local = local
                inventario.stock_actual = inventario.entradas - inventario.salidas
                inventario.save()
                messages.success(request, 'Movimiento de inventario agregado correctamente.')

            return redirect('inventario_local', local_id=local.id)
    else:
        form = InventarioLocalForm()

    return render(request, 'locales/form_inventario_local.html', {
        'form': form,
        'accion': 'Agregar',
        'local': local
    })


@login_required(login_url='login')
def editar_movimiento_local(request, local_id, inventario_id):
    local = get_object_or_404(Local, id=local_id)
    inventario = get_object_or_404(InventarioLocal, id=inventario_id, local=local)

    if request.method == 'POST':
        form = InventarioLocalForm(request.POST, instance=inventario)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.local = local  
            movimiento.stock_actual = movimiento.entradas - movimiento.salidas
            movimiento.save()
            messages.success(request, 'Movimiento actualizado correctamente.')
            return redirect('inventario_local', local_id=local.id)
    else:
        form = InventarioLocalForm(instance=inventario)

    return render(request, 'locales/form_inventario_local.html', {
        'form': form,
        'accion': 'Editar',
        'local': local
    })

@login_required(login_url='login')
@require_POST
def eliminar_inventario(request, inventario_id):
    if request.method == "POST":
        inventario = get_object_or_404(InventarioLocal, id=inventario_id)
        inventario.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url = 'login')
def lista_referencias(request, local_id):
    referencias = InventarioLocal.objects.filter(local=local_id).select_related('variante__producto')

    referencias_unicas = {}
    for referencia in referencias:
        producto_referencia = referencia.variante.producto.referencia
        if producto_referencia not in referencias_unicas:
            referencias_unicas[producto_referencia] = referencia

    referencias_unicas = list(referencias_unicas.values())

    return render(request, 'locales/lista-referencias.html', {'referencias_unicas': referencias_unicas})

@login_required(login_url = 'login')
def resumen_inventario_producto(request, local_id, producto_id):
    producto = Producto.objects.get(id=producto_id)
    local = Local.objects.get(id=local_id)
    inventario = InventarioLocal.objects.filter(local=local_id, variante__producto=producto) \
        .values('variante__talla__nombre') \
        .annotate(stock_total=Sum('stock_actual'), salidas_total=Sum('salidas')) \
        .order_by('variante__talla__nombre')
    fecha_actualizacion = InventarioLocal.objects.filter(variante__producto=producto).aggregate(ultima_fecha=Max('fecha'))['ultima_fecha']
    total_stock = sum(item['stock_total'] for item in inventario)
    total_salidas = sum(item['salidas_total'] for item in inventario)

    context = {
        'producto': producto,
        'local': local,
        'inventario': inventario,
        'fecha': fecha_actualizacion,
        'total_stock': total_stock,
        'total_salidas': total_salidas
    }
    return render(request, 'locales/resumen-inventario.html', context)

@login_required(login_url='login')
def resumen_inventario_semanal(request, local_id, producto_id):
    local = get_object_or_404(Local, id=local_id)
    producto = get_object_or_404(Producto, id=producto_id)

    fecha_inicio = parse_date(request.GET.get('fecha_inicio', ''))
    fecha_fin = parse_date(request.GET.get('fecha_fin', ''))

    inventario_qs = InventarioSemanal.objects.filter(local=local, variante__producto=producto)

    if fecha_inicio and fecha_fin:
        inventario_qs = inventario_qs.filter(semana__range=(fecha_inicio, fecha_fin))

    inventario_qs = inventario_qs.order_by('-semana')

    data_por_semana = {}
    for item in inventario_qs:
        semana = item.semana
        if semana not in data_por_semana:
            data_por_semana[semana] = {'entradas': 0, 'salidas': 0, 'stock_final': 0}
        data_por_semana[semana]['entradas'] += item.entradas
        data_por_semana[semana]['salidas'] += item.salidas
        data_por_semana[semana]['stock_final'] += item.stock_final

    inventario_list = [
        {'semana': semana, **val}
        for semana, val in sorted(data_por_semana.items(), reverse=True)
    ]

    total_entradas = sum(i['entradas'] for i in inventario_list)
    total_salidas = sum(i['salidas'] for i in inventario_list)
    stock_final_total = sum(i['stock_final'] for i in inventario_list)

    context = {
        'local': local,
        'producto': producto,
        'inventario_semanal': inventario_list,
        'total_entradas': total_entradas,
        'total_salidas': total_salidas,
        'stock_final_total': stock_final_total,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }

    return render(request, 'locales/resumen-semanal.html', context)

@login_required(login_url='login')
def exportar_inventario_pdf(request, local_id):
    inventario = InventarioLocal.objects.filter(local_id=local_id).select_related(
        'variante__producto', 'variante__talla', 'variante__color', 'variante__diseno'
    )

    context = {
        'inventario': inventario,
        'local': inventario.first().local if inventario.exists() else None
    }

    html_string = render_to_string('locales/reportes/exportar_inventario_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventario_local.pdf"'
    pisa.CreatePDF(io.StringIO(html_string), dest=response)
    return response

@login_required(login_url='login')
def exportar_inventario_excel(request, local_id):
    inventario = InventarioLocal.objects.filter(local_id=local_id).select_related(
        'variante__producto', 'variante__talla', 'variante__color', 'variante__diseno'
    )

    data = []
    for item in inventario:
        data.append({
            'Producto': item.variante.producto.referencia,
            'Talla': item.variante.talla.nombre,
            'Color': item.variante.color.nombre,
            'Diseño': item.variante.diseno.nombre if item.variante.diseno else 'Sin diseño',
            'Entradas': item.entradas,
            'Salidas': item.salidas,
            'Stock Actual': item.stock_actual,
            'Fecha': item.fecha.strftime('%d/%m/%Y')
        })

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventario')

    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="inventario_local.xlsx"'
    return response

@login_required(login_url='login')
def exportar_resumen_excel(request, local_id, producto_id):
    inventario = (
        InventarioLocal.objects
        .filter(local_id=local_id, variante__producto_id=producto_id)
        .values('variante__talla__nombre')
        .annotate(
            stock_total=Sum('stock_actual'),
            salidas_total=Sum('salidas')
        )
    )

    data = [
        {
            'Talla': item['variante__talla__nombre'],
            'Stock Total': item['stock_total'],
            'Salidas Totales': item['salidas_total'],
        }
        for item in inventario
    ]

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Resumen_Inventario_Local{local_id}_Producto{producto_id}.xlsx'
    df.to_excel(response, index=False, engine='xlsxwriter')
    return response

@login_required(login_url='login')
def exportar_resumen_pdf(request, local_id, producto_id):
    local = Local.objects.get(pk=local_id)
    producto = Producto.objects.get(pk=producto_id)

    inventario = (
        InventarioLocal.objects
        .filter(local=local, variante__producto=producto)
        .values('variante__talla__nombre')
        .annotate(
            stock_total=Sum('stock_actual'),
            salidas_total=Sum('salidas')
        )
    )

    total_stock = sum(item['stock_total'] for item in inventario)
    total_salidas = sum(item['salidas_total'] for item in inventario)

    logo_path = ''
    if local.empresa.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, local.empresa.logo.name)

    context = {
        'local': local,
        'producto': producto,
        'inventario': inventario,
        'total_stock': total_stock,
        'total_salidas': total_salidas,
        'now': now(),
        'logo_path': logo_path,
    }

    html = render_to_string('locales/reportes/resumen_inventario_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Resumen_Inventario_Local{local_id}_Producto{producto_id}.pdf"'

    pisa_status = pisa.CreatePDF(src=html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

@login_required(login_url='login')
def exportar_resumen_semanal_pdf(request, local_id, producto_id):
    local = get_object_or_404(Local, pk=local_id)
    producto = get_object_or_404(Producto, pk=producto_id)
    inventario_semanal = (
        InventarioSemanal.objects
        .filter(local=local, variante__producto=producto)
        .order_by('-semana')
    )

    context = {
        'local': local,
        'producto': producto,
        'inventario_semanal': inventario_semanal,
        'now': now()
    }

    html = render_to_string('locales/reportes/resumen_semanal_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Resumen_Semanal_{producto.referencia}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Hubo un error al generar el PDF", status=500)

    return response

@login_required(login_url='login')
def exportar_resumen_semanal_excel(request, local_id, producto_id):
    local = Local.objects.get(pk=local_id)
    producto = Producto.objects.get(pk=producto_id)
    inventario = InventarioSemanal.objects.filter(local=local, variante__producto=producto).order_by('-semana')

    data = [
        {
            'Semana': item.semana.strftime('%Y-%m-%d'),
            'Entradas': item.entradas,
            'Salidas': item.salidas,
            'Stock Final': item.stock_final
        }
        for item in inventario
    ]

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Resumen_Semanal_{producto.referencia}.xlsx"'

    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='ResumenSemanal')

    return response