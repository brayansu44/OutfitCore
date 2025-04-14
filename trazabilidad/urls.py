from django.urls import path
from . import views

urlpatterns = [
    #telas
    path('telas/', views.telas, name='telas'),
    path('telas/agregar/', views.agregar_tela, name='agregar_tela'),
    path('telas/editar/<int:tela_id>/', views.editar_tela, name='editar_tela'),
    path('telas/eliminar/<int:tela_id>/', views.eliminar_tela, name='eliminar_tela'),

    # Rollos de tela
    path('rollos/', views.rollos, name='rollos'),
    path('rollos/agregar/', views.agregar_rollo, name='agregar_rollo'),
    path('rollos/editar/<int:rollo_id>/', views.editar_rollo, name='editar_rollo'),
    path('rollos/eliminar/<int:rollo_id>/', views.eliminar_rollo, name='eliminar_rollo'),

    # Ordenes de produccion
    path('ordenes_produccion/', views.ordenes_produccion, name='ordenes_produccion'),
    path('ordenes_produccion/agregar/', views.agregar_orden, name='agregar_orden'),
    path('ordenes_produccion/editar/<int:orden_id>/', views.editar_orden, name='editar_orden'),
    path('ordenes_produccion/eliminar/<int:orden_id>/', views.eliminar_orden, name='eliminar_orden'),

    # Cortes
    path('cortes_tela/', views.cortes, name='cortes'),
    path('cortes/agregar/', views.agregar_corte, name='agregar_corte'),
    #path('tallas_corte/', views.tallas_corte, name='tallas_corte'),
]    