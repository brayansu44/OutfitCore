from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
]    