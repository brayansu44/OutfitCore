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
    path('cortes/editar/<int:corte_id>/', views.editar_corte, name='editar_corte'),
    path('cortes/eliminar/<int:corte_id>/', views.eliminar_corte, name='eliminar_corte'),

    #tallas
    path('tallas_corte/', views.tallas, name='tallas'),
    path('tallas_corte/agregar/', views.agregar_talla, name='agregar_talla'),
    path('tallas_corte/editar/<int:talla_id>/', views.editar_talla, name='editar_talla'),
    path('tallas_corte/eliminar/<int:talla_id>/', views.eliminar_talla, name='eliminar_talla'),

    #Retazos
    path('retazos_tela/', views.retazos, name='retazos'),
    path('retazos_tela/agregar', views.agregar_retazo, name='agregar_retazo'),
    path('retazos_tela/editar/<int:retazo_id>/', views.editar_retazo, name='editar_retazo'),
    path('retazos_tela/eliminar/<int:retazo_id>/', views.eliminar_retazo, name='eliminar_retazo'),

    path('informe_cortes/', views.informe_cortes, name='informe_cortes'),
]    