from django.urls import path
from . import views

urlpatterns = [
    path('Cuentas/ventas/', views.Ventas, name='ventas'),
    path('Cuentas/compras/', views.Compras, name='compras'),
    path('Cuentas/ventas/facturas', views.Factura_venta, name='factura_venta'),
    path('Cuentas/ventas/pagos', views.Pago_venta, name='pago_venta'),
]    