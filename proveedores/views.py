from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#models
from .models import Proveedor

# Create your views here.
@login_required(login_url = 'login')
def proveedores(request):
    proveedores = Proveedor.objects.all()

    return render(request, 'proveedores/proveedores.html', {'proveedores': proveedores})