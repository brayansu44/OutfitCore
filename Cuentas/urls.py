from django.urls import path
from . import views

urlpatterns = [
    path('ventas/', views.Ventas, name='ventas'),
    path('compras/', views.Compras, name='compras'),

    #CLIENTE
    path('clientes/', views.agregar_cliente, name='agregar_cliente'),

    #FACTURA DE VENTA
    path('ventas/facturas', views.Factura_venta, name='factura_venta'),
    path('ventas/facturas/agregar', views.agregar_factura_venta, name='agregar_factura_venta'),
    path('ventas/facturas/editar', views.editar_factura_venta, name='editar_factura_venta'),

    # PAGO RECIBIDO DE VENTA
    path('ventas/pagos', views.Pago_venta, name='pago_venta'),
]    