from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from locales.models import Local

from .models import Empresa

@login_required(login_url = 'login')
def empresas(request):
    empresas        = Empresa.objects.annotate(locales_count=Count('Empresa_relacionada'), 
                                               usuarios_count=Count('Empresa_usuario__perfil'))
    context = {
        'empresas': empresas,
    }

    return render(request, 'empresas/empresas.html', context)

@login_required(login_url='login')
def set_empresa_id(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    request.session['empresa_id'] = empresa.id
    return redirect('locales')

