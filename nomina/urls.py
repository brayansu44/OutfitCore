from django.urls import path
from . import views


urlpatterns = [
    path('', views.nomina , name='nomina'),
    path('SeguridadSocial/<str:tab_id>/', views.SeguridadSocial , name='SeguridadSocial'),

    #EPS
    path('nomina/SeguridadSocial/step-1/', views.EPSadd, name='EPSadd'),
    path('nomina/SeguridadSocial/step-1/<int:eps_id>/', views.EPSedit, name='EPSedit'),
    path('nomina/SeguridadSocial/step-1/<int:eps_id>/', views.EPSdelete, name='EPSdelete'),
]
