from django.urls import path
from . import views

urlpatterns = [
    path('', views.nomina , name='nomina'),
    path('SeguridadSocial/<str:tab_id>/', views.SeguridadSocial , name='SeguridadSocial'),

    #EPS
    path('SeguridadSocial/EPS/add/', views.EPSadd, name='EPSadd'),
    path('SeguridadSocial/EPS/edit/<int:eps_id>/', views.EPSedit, name='EPSedit'),
]
