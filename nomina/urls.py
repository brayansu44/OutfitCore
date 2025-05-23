from django.urls import path
from . import views


urlpatterns = [
    path('', views.nomina , name='nomina'),
    path('SeguridadSocial/<str:tab_id>/', views.SeguridadSocial , name='SeguridadSocial'),

    #EPS
    path('SeguridadSocial/', views.EPSadd, name='EPSadd'),
    path('SeguridadSocial/<int:eps_id>/', views.EPSedit, name='EPSedit'),
    path('SeguridadSocial/EPSdelete/<int:eps_id>/', views.EPSdelete, name='EPSdelete'),
]
