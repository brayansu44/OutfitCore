from django.urls import path, include
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
    path('ventas/pagos/edit/<int:pago_id>/', views.editar_pago_venta, name='editar_pago_venta'),
    path('ventas/pagos/delete/<int:pago_id>/', views.delete_pago_venta, name='delete_pago_venta'),

    #FACTURA DE COMPRA
    path('compras/facturas', views.Factura_compra, name='factura_compra'),
    path('compras/facturas/add', views.agregar_factura_compra, name='agregar_factura_compra'),
    path('compras/facturas/edit/<int:factura_id>/', views.editar_factura_compra, name='editar_factura_compra'),
    path('compras/facturas/delete/<int:factura_id>/', views.delete_factura_compra, name='delete_factura_compra'),

    # PAGO DE COMPRA
    path('compras/pagos', views.Pago_compra, name='pago_compra'),
    path('compras/pagos/add', views.agregar_pago_compra, name='agregar_pago_compra'),
    path('compras/pagos/edit/<int:pago_id>/', views.editar_pago_compra, name='editar_pago_compra'),
    path('compras/pagos/delete/<int:pago_id>/', views.delete_pago_compra, name='delete_pago_compra'),
]   
