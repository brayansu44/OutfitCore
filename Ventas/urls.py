# ventas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lista_ventas/', views.lista_ventas, name='lista_ventas'),
    path('lista_ventas/agregar/', views.crear_venta, name='agregar_venta'),
    # Otras rutas como:
    # path('detalle/<int:id>/', views.detalle_venta, name='detalle_venta'),
]
