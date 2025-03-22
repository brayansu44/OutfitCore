from django.urls import path
from . import views

urlpatterns = [
    path('', views.telas, name='telas'),
    path('rollos_tela/', views.rollos_tela, name='rollos_tela'),
    path('ordenes_produccion/', views.ordenes_produccion, name='ordenes_produccion'),
    path('cortes_tela/', views.cortes_tela, name='cortes_tela'),
    path('tallas_corte/', views.tallas_corte, name='tallas_corte'),
    path('componentes_corte/', views.componentes_corte, name='componentes_corte'),
]    