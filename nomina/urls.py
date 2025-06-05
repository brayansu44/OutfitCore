from django.urls import path
from . import views

urlpatterns = [
    path('', views.nomina , name='nomina'),
    path('SeguridadSocial/<str:tab_id>/', views.SeguridadSocial , name='SeguridadSocial'),

    #EPS
    path('SeguridadSocial/EPS/add/', views.EPSadd, name='EPSadd'),
    path('SeguridadSocial/EPS/edit/<int:eps_id>/', views.EPSedit, name='EPSedit'),
    path('SeguridadSocial/EPS/delete/<int:eps_id>/', views.EPSdelete, name='EPSdelete'),
    #ARL
    path('SeguridadSocial/ARL/add/', views.ARLadd, name='ARLadd'),
    path('SeguridadSocial/ARL/edit/<int:arl_id>/', views.ARLedit, name='ARLedit'),
    path('SeguridadSocial/ARL/delete/<int:arl_id>/', views.ARLdelete, name='ARLdelete'),
    #PENSION
    path('SeguridadSocial/PENSION/add/', views.PENSIONadd, name='PENSIONadd'),
    path('SeguridadSocial/PENSION/edit/<int:pension_id>/', views.PENSIONedit, name='PENSIONedit'),
    path('SeguridadSocial/PENSION/delete/<int:pension_id>/', views.PENSIONdelete, name='PENSIONdelete'),
    #CAJA
    path('SeguridadSocial/CAJA/add/', views.CAJAadd, name='CAJAadd'),
    path('SeguridadSocial/CAJA/edit/<int:caja_id>/', views.CAJAedit, name='CAJAedit'),
    path('SeguridadSocial/CAJA/delete/<int:caja_id>/', views.CAJAdelete, name='CAJAdelete'),
]
