from django.urls import path
from . import views

urlpatterns = [
    path('', views.empresas, name='empresas'),
    path('set_empresa_id/<int:empresa_id>/', views.set_empresa_id, name='set_empresa_id'),
]    
