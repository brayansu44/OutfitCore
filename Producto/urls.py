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

]    