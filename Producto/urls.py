from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('generar-todos-codigos/', views.generar_codigos_todos_productos, name='generar_codigos_todos_productos'),
    path('generar-codigo-por-producto/<int:producto_id>/', views.generar_codigos_por_producto, name='generar_codigos_por_producto'),
    path("buscar-por-codigo/", views.buscar_por_codigo, name="buscar_por_codigo"),
    path('productos/detalle-producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('variante/<int:variante_id>/codigo-barras/', views.codigo_barras_variante, name='codigo_barras_variante'),
    path('variante/<int:variante_id>/descargar-codigo/', views.descargar_codigo_barras_variante, name='descargar_codigo_barras_variante'),
    path('productos/variante/<int:variante_id>/', views.detalle_variante, name='detalle_variante'),
    path('productos/<int:producto_id>/exportar-excel/', views.exportar_variantes_excel, name='exportar_variantes_excel'),
    path('productos/<int:producto_id>/exportar-pdf/', views.exportar_variantes_pdf, name='exportar_variantes_pdf'),
]    