from django.urls import path
from . import views

urlpatterns = [
    path('inventario/', views.inventario_bodega, name='inventario_bodega'),
    path('inventario/agregar/', views.crear_stock, name='crear_stock'),
    path('inventario/editar/<int:stock_id>/', views.editar_stock, name='editar_stock'),
    path('inventario/eliminar/<int:stock_id>/', views.eliminar_stock, name='eliminar_stock'),

    path('entradas_producto/', views.entradas_producto, name='entradas'),
    path('entradas/crear/', views.crear_entrada, name='crear_entrada'),
    path('entradas/editar/<int:entrada_id>/', views.editar_entrada, name='editar_entrada'),
    path('entradas/eliminar/<int:entrada_id>/', views.eliminar_entrada, name='eliminar_entrada'),

    path('salidas_producto/', views.salidas_producto, name='salidas_producto'),
    path('salidas/crear/', views.crear_salida_producto, name='crear_salida_producto'),
    path('salidas/<int:salida_id>/editar/', views.editar_salida_producto, name='editar_salida_producto'),
    path('salidas/eliminar/<int:salida_id>/', views.eliminar_salida_producto, name='eliminar_salida_producto'),

    path('historial/<int:variante_id>/', views.historial_movimientos_producto, name='historial_movimientos'),
    path('historial/<int:variante_id>/exportar-excel/', views.exportar_historial_excel, name='exportar_historial_excel'),
    path('bodega/historial/<int:variante_id>/exportar-pdf/', views.exportar_historial_pdf, name='exportar_historial_pdf'),

    path('inventario-insumos/', views.inventario_insumos, name='inventario_insumos'),
    path('insumos/agregar/', views.agregar_insumo, name='agregar_insumo'),
    path('insumos/editar/<int:insumo_id>/', views.editar_insumo, name='editar_insumo'),
    path('insumos/eliminar/<int:insumo_id>/', views.eliminar_insumo, name='eliminar_insumo'),

    path('ingresos/', views.listar_ingresos_insumo, name='ingresos_insumos'),
    path('insumos/ingreso/nuevo/', views.agregar_ingreso_insumo, name='agregar_ingreso_insumo'),
    path('ingresos-insumos/<int:ingreso_id>/editar/', views.editar_ingreso_insumo, name='editar_ingreso_insumo'),
    path('ingresos-insumos/eliminar/<int:ingreso_id>/', views.eliminar_ingreso_insumo, name='eliminar_ingreso_insumo'),
    path('ingresos-insumos/<int:ingreso_id>/detalle/', views.detalle_ingreso_insumo, name='detalle_ingreso_insumo'),
    path('ingresos/exportar/excel/<int:ingreso_id>/', views.exportar_detalle_ingreso_excel, name='exportar_detalle_ingreso_excel'),
    path('ingresos/exportar/pdf/<int:ingreso_id>/', views.exportar_detalle_ingreso_pdf, name='exportar_detalle_ingreso_pdf'),

    path('uso-insumos/', views.lista_uso_insumos, name='lista_uso_insumos'),
    path('uso-insumos/crear/', views.crear_uso_insumo, name='crear_uso_insumo'),
    path('obtener-stock/<int:insumo_id>/', views.obtener_stock_insumo, name='obtener_stock_insumo'),
    path('uso-insumos/<int:uso_id>/editar/', views.editar_uso_insumo, name='editar_uso_insumo'),
    path('uso-insumos/eliminar/<int:uso_id>/', views.eliminar_uso_insumo, name='eliminar_uso_insumo'),
]    
