from django.urls import path
from . import views

urlpatterns = [
    path('', views.nomina , name='nomina'),
    path('SeguridadSocial/<str:tab_id>/', views.SeguridadSocial , name='SeguridadSocial'),
    path('SeguridadSocial/', views.Register_EPS, name='Register_EPS'),
]
