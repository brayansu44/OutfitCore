from django.urls import path
from . import views

urlpatterns = [
    path('ventas/', views.Ventas, name='ventas'),
    path('compras/', views.Compras, name='compras'),

    #MODAL CONTENT
    path('clientes/', views.agregar_cliente, name='agregar_cliente'),
    path('facturaVenta/', views.addFacturaVenta, name='addFacturaVenta'),

    #FACTURA DE VENTA
    path('ventas/facturas', views.Factura_venta, name='factura_venta'),
    path('ventas/facturas/add', views.agregar_factura_venta, name='agregar_factura_venta'),
    path('ventas/facturas/edit/<int:factura_id>/', views.editar_factura_venta, name='editar_factura_venta'),
    path('ventas/facturas/delete/<int:factura_id>/', views.delete_factura_venta, name='delete_factura_venta'),

    # PAGO RECIBIDO DE VENTA
    path('ventas/pagos', views.Pago_venta, name='pago_venta'),


    path('ventas/pagos/add', views.agregar_pago_venta, name='agregar_pago_venta'),
    path('ventas/pagos/edit/<int:factura_id>/', views.editar_pago_venta, name='editar_pago_venta'),
    path('ventas/pagos/delete/<int:factura_id>/', views.delete_pago_venta, name='delete_pago_venta'),
]   
