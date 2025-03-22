from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Empresa

@login_required(login_url = 'login')
def empresas(request):
    empresas        = Empresa.objects.annotate(locales_count=Count('Empresa_relacionada'), 
                                               usuarios_count=Count('Empresa_usuario__perfil'))
    context = {
        'empresas': empresas,
    }

    return render(request, 'empresas/empresas.html', context)