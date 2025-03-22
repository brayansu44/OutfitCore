from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Producto

def productos(request):
    productos = Producto.objects.prefetch_related('talla', 'color').all()
    return render(request, 'productos/productos.html', {'productos': productos})
