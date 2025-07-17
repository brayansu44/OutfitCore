from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from openpyxl import Workbook

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

from .forms import *

#codigo de barras
from barcode import Code128
from barcode.writer import ImageWriter
from django.utils.text import slugify
import io
import zipfile
import base64


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
    barcode_base64 = None

    for v in ProductoVariante.objects.select_related('producto', 'color', 'talla'):
        if v.get_codigo_barra().lower() == codigo.lower():
            variante = v
            barcode_base64 = generar_codigo_barra_base64(v.get_codigo_barra())
            break

    return render(request, 'productos/detalle_variante.html', {
        'variante': variante,
        'barcode_base64': barcode_base64
    })

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    variantes_list = ProductoVariante.objects.filter(producto=producto)

    paginator = Paginator(variantes_list, 10)  # Muestra 10 variantes por página
    page_number = request.GET.get('page')
    variantes = paginator.get_page(page_number)

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'variantes': variantes,
        'paginator': paginator,
    })

@login_required(login_url='login')
def detalle_variante(request, variante_id):
    variante = get_object_or_404(ProductoVariante, id=variante_id)
    return render(request, 'productos/detalle_variante.html', {'variante': variante})


@login_required(login_url='login')
def codigo_barras_variante(request, variante_id):
    variante = get_object_or_404(ProductoVariante, id=variante_id)
    codigo = variante.get_codigo_barra()
    
    buffer = io.BytesIO()
    Code128(codigo, writer=ImageWriter()).write(buffer)
    
    return HttpResponse(buffer.getvalue(), content_type='image/png')

@login_required(login_url='login')
def descargar_codigo_barras_variante(request, variante_id):
    variante = get_object_or_404(ProductoVariante, id=variante_id)
    codigo = variante.get_codigo_barra()

    buffer = io.BytesIO()
    Code128(codigo, writer=ImageWriter()).write(buffer, options={"write_text": True})
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{codigo}.png"'
    return response

def generar_codigo_barra_base64(codigo):
    buffer = io.BytesIO()
    Code128(codigo, writer=ImageWriter()).write(buffer)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

@login_required
def exportar_variantes_excel(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    variantes = ProductoVariante.objects.filter(producto=producto)

    wb = Workbook()
    ws = wb.active
    ws.title = "Variantes"

    ws.append(["Código de barras", "Color", "Talla", "Diseño"])

    for v in variantes:
        ws.append([
            v.get_codigo_barra(),
            v.color.nombre,
            v.talla.nombre,
            v.diseno.nombre if v.diseno else "Sin diseño"
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="variantes_{producto.referencia}.xlsx"'
    wb.save(response)
    return response

def exportar_variantes_pdf(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    variantes = ProductoVariante.objects.filter(producto=producto)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=60,
        bottomMargin=40,
        title=f"Variantes - {producto.referencia}",
    )

    elements = []
    styles = getSampleStyleSheet()

    # --- Logotipo (opcional) ---
    logo_path = os.path.join(settings.BASE_DIR, 'kiddes', 'static', 'images', 'logo-img.png') 
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=80, height=40)
        elements.append(logo)
        elements.append(Spacer(1, 12))

    # --- Título ---
    titulo = Paragraph(f"<b>Reporte de variantes del producto:</b> {producto.referencia}", styles['Title'])
    elements.append(titulo)
    elements.append(Spacer(1, 12))

    # --- Tabla de datos ---
    data = [['Código de Barras', 'Color', 'Talla', 'Diseño']]
    for variante in variantes:
        data.append([
            variante.get_codigo_barra(),
            variante.color.nombre,
            variante.talla.nombre,
            variante.diseno.nombre if variante.diseno else "Sin diseño"
        ])

    tabla = Table(data, repeatRows=1, hAlign='LEFT', colWidths=[150, 100, 80, 120])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(tabla)

    # --- Generar PDF ---
    doc.build(elements)

    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')