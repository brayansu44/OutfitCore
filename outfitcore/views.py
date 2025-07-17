from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from empresas.models import Empresa

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html', {'mensaje': 'Bienvenido a la página principal'})

@login_required(login_url = 'login')
def home_with_empresa(request, empresa_id=None):
    empresa = None
    if empresa_id:
        empresa = get_object_or_404(Empresa, id=empresa_id)
        request.session['empresa_id'] = empresa.id
    return render(request, 'home.html', {'empresa': empresa})

@login_required(login_url = 'login')
def set_empresa_id(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    request.session['empresa_id'] = empresa.id
    return redirect('home')