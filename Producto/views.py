from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import *

#codigo de barras
from barcode import Code128
from barcode.writer import ImageWriter
from django.utils.text import slugify
import io
import zipfile

@login_required(login_url='login')
def productos(request):
    productos = Producto.objects.prefetch_related('talla', 'color').all()
    diseno_id = request.GET.get("diseno_id")

    if diseno_id:
        productos = productos.filter(diseno__id=diseno_id).distinct()

    disenos = Diseno.objects.all()

    context = {
        'productos': productos,
        'disenos': disenos,
    }

    return render(request, 'productos/productos.html', context)

@login_required(login_url='login')
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            form.save_m2m()
            messages.success(request, "Producto agregado correctamente.")
            return redirect('productos')
    else:
        form = ProductoForm()
    
    return render(request, 'productos/form_producto.html', {'form': form, 'accion': 'Agregar'})

@login_required(login_url='login')
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            form.save_m2m()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('productos') 
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/form_producto.html', {
        'form': form,
        'accion': 'Editar'
    })

@login_required(login_url='login')
@require_POST
def eliminar_producto(request, producto_id):
    if request.method == "POST":
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='login')
def generar_codigos_todos_productos(request):
    productos = Producto.objects.all().prefetch_related('variantes', 'variantes__color', 'variantes__talla')
    
    if not productos.exists():
        messages.warning(request, "No hay productos registrados.")
        return redirect('productos')

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for producto in productos:
            variantes = producto.variantes.all()
            for variante in variantes:
                codigo = f"{producto.codigo}-{variante.color.nombre}-{variante.talla.nombre}"
                codigo_slug = slugify(codigo)
                buffer = io.BytesIO()
                Code128(codigo, writer=ImageWriter()).write(buffer)
                zip_file.writestr(f"{producto.codigo}/{codigo_slug}.png", buffer.getvalue())  # se agrupan por carpeta del producto

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="codigos_todos_productos.zip"'
    return response

@login_required(login_url='login')
def generar_codigos_todos_productos(request):
    productos = Producto.objects.all().prefetch_related('variantes', 'variantes__color', 'variantes__talla')
    
    if not productos.exists():
        messages.warning(request, "No hay productos registrados.")
        return redirect('productos')

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for producto in productos:
            variantes = producto.variantes.all()
            for variante in variantes:
                codigo = f"{producto.codigo}-{variante.color.nombre}-{variante.talla.nombre}"
                codigo_slug = slugify(codigo)
                buffer = io.BytesIO()
                Code128(codigo, writer=ImageWriter()).write(buffer)
                zip_file.writestr(f"{producto.codigo}/{codigo_slug}.png", buffer.getvalue())  # se agrupan por carpeta del producto

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="codigos_todos_productos.zip"'
    return response

@login_required(login_url='login')
def generar_codigos_por_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    variantes = ProductoVariante.objects.filter(producto=producto)

    if not variantes.exists():
        messages.warning(request, "Este producto no tiene variantes para generar códigos de barras.")
        return redirect('productos')

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for variante in variantes:
            codigo = f"{producto.codigo}-{variante.color.nombre}-{variante.talla.nombre}"
            codigo_slug = slugify(codigo)  # Asegura nombres válidos
            buffer = io.BytesIO()
            Code128(codigo, writer=ImageWriter()).write(buffer)
            zip_file.writestr(f"{codigo_slug}.png", buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="codigos_producto_{producto.codigo}.zip"'
    return response

@login_required(login_url='login')
def buscar_por_codigo(request):
    codigo = request.GET.get('codigo', '')
    variante = None

    for v in ProductoVariante.objects.select_related('producto', 'color', 'talla'):
        if v.get_codigo_barra().lower() == codigo.lower():
            variante = v
            break

    return render(request, 'productos/detalle_variante.html', {'variante': variante})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    variantes = ProductoVariante.objects.filter(producto=producto)
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'variantes': variantes
    })



