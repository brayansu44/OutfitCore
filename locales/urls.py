from django.urls import path
from . import views

urlpatterns = [
    path('', views.locales, name='locales'),
    path('locales-empresa/<int:empresa_id>/', views.locales_por_empresa, name='locales_por_empresa'),
    path('inventario-local/<int:local_id>/', views.inventario_local, name='inventario_local'),
    path('lista-referencias/<int:local_id>/', views.lista_referencias, name='lista_referencias'),
    path('resumen-inventario-producto/<int:local_id>/<int:producto_id>/', views.resumen_inventario_producto, name='resumen_inventario_producto'),
    path('resumen-inventario-semanal/<int:local_id>/<int:producto_id>/', views.resumen_inventario_semanal, name='resumen_inventario_semanal'),
]    