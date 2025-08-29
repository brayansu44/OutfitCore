# ventas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lista_ventas/', views.lista_ventas, name='lista_ventas'),
    path("obtener-variantes/", views.obtener_variantes_por_local, name="obtener_variantes"),
    path('lista_ventas/agregar/', views.crear_venta, name='agregar_venta'),
    path('venta/<int:pk>/', views.venta_detalle, name='venta_detalle'),
    # Otras rutas como:
    # path('detalle/<int:id>/', views.detalle_venta, name='detalle_venta'),
]
