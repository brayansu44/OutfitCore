from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#models
from .models import *

# Create your views here.
@login_required(login_url='login')
def telas(request):
    telas = Tela.objects.all()
    return render(request, 'telas/telas.html', {'telas': telas})

@login_required(login_url='login')
def rollos_tela(request):
    rollos_tela = RolloTela.objects.all()
    return render(request, 'telas/rollos-tela.html', {'rollos_tela': rollos_tela})

@login_required(login_url='login')
def ordenes_produccion(request):
    orden_produccion = OrdenProduccion.objects.all()
    return render(request, 'telas/ordenes-produccion.html', {'orden_produccion': orden_produccion})

@login_required(login_url='login')
def cortes_tela(request):
    cortes_tela = CorteTela.objects.all()
    return render(request, 'telas/cortes-tela.html', {'cortes_tela': cortes_tela})

@login_required(login_url='login')
def tallas_corte(request):
    tallas_corte = TallaCorte.objects.all()
    return render(request, 'telas/tallas-corte.html', {'tallas_corte': tallas_corte})

@login_required(login_url='login')
def componentes_corte(request):
    componentes_corte = ComponenteCorte.objects.all()
    return render(request, 'telas/componentes-corte.html', {'componentes_corte': componentes_corte})