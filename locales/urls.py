from django.urls import path
from . import views

urlpatterns = [
    path('', views.locales, name='locales'),
    path('locales/<int:empresa_id>', views.locales, name='locales'),
    path('agregar/', views.agregar_local, name='agregar_local'),
    path('editar/<int:local_id>/', views.editar_local, name='editar_local'),
    path('eliminar/<int:local_id>/', views.eliminar_local, name='eliminar_local'),
    path('inventario-local/<int:local_id>/', views.inventario_local, name='inventario_local'),
    path('local/<int:local_id>/agregar-movimiento/', views.agregar_movimiento_local, name='agregar_movimiento_local'),
    path('local/<int:local_id>/editar-movimiento/<int:inventario_id>/', views.editar_movimiento_local, name='editar_movimiento_local'),
    path('inventario/eliminar/<int:inventario_id>/', views.eliminar_inventario, name='eliminar_inventario'),
    path('lista-referencias/<int:local_id>/', views.lista_referencias, name='lista_referencias'),
    path('resumen-inventario-producto/<int:local_id>/<int:producto_id>/', views.resumen_inventario_producto, name='resumen_inventario_producto'),
    path('resumen-inventario-semanal/<int:local_id>/<int:producto_id>/', views.resumen_inventario_semanal, name='resumen_inventario_semanal'),
    path('inventario/exportar/excel/<int:local_id>/', views.exportar_inventario_excel, name='exportar_inventario_excel'),
    path('inventario/exportar/pdf/<int:local_id>/', views.exportar_inventario_pdf, name='exportar_inventario_pdf'),
    path('resumen-inventario/excel/<int:local_id>/<int:producto_id>/', views.exportar_resumen_excel, name='exportar_resumen_excel'),
    path('resumen-inventario/pdf/<int:local_id>/<int:producto_id>/', views.exportar_resumen_pdf, name='exportar_resumen_pdf'),
    path('resumen-inventario/semanal/pdf/<int:local_id>/<int:producto_id>/', views.exportar_resumen_semanal_pdf, name='exportar_resumen_semanal_pdf'),
    path('resumen-inventario/semanal/excel/<int:local_id>/<int:producto_id>/', views.exportar_resumen_semanal_excel, name='exportar_resumen_semanal_excel'),
]    