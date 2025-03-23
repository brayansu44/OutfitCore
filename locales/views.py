from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max

from locales.models import Local, InventarioLocal, InventarioSemanal
from Producto.models import Producto

# Create your views here.
@login_required(login_url = 'login')
def locales(request):
    locales = Local.objects.all()
    return render(request, 'locales/locales.html', {'locales': locales})

@login_required(login_url='login') 
def locales_with_empresa(request): 
    empresa_id = request.session.get('empresa_id') 
    locales = Local.objects.filter(empresa_id=empresa_id) 
    return render(request, 'locales/locales.html', {'locales': locales})

@login_required(login_url = 'login')
def inventario_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)
    inventario = InventarioLocal.objects.filter(local=local).select_related('variante__producto')

    context = {
        'local': local,
        'inventario': inventario,
    }

    return render(request, 'locales/inventario-local.html', context)

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

@login_required(login_url = 'login')
def resumen_inventario_semanal(request, local_id, producto_id):
    local = get_object_or_404(Local, id=local_id)
    producto = get_object_or_404(Producto, id=producto_id)

    inventario_semanal = (
        InventarioSemanal.objects
        .filter(local=local, variante__producto=producto)
        .order_by('-semana') 
    )

    context = {
        'local': local,
        'producto': producto,
        'inventario_semanal': inventario_semanal,
    }
    
    return render(request, 'locales/resumen-semanal.html', context)
