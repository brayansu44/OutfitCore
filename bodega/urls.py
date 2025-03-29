from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario_bodega, name='inventario_bodega'),
    path('entradas_producto/', views.entradas_producto, name='entradas'),
    path('salidas_producto/', views.salidas_producto, name='salidas'),
    path('inventario-insumos/', views.inventario_insumos, name='inventario_insumos'),
]    