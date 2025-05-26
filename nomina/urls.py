from django.urls import path
from . import views

urlpatterns = [
    path('', views.nomina , name='nomina'),
    path('SeguridadSocial/<str:tab_id>/', views.SeguridadSocial , name='SeguridadSocial'),

    #EPS
    path('SeguridadSocial/step-1/add/', views.EPSadd, name='EPSadd')
]
