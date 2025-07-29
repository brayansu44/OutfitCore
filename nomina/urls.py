from django.urls import path
from . import views

urlpatterns = [
    path('', views.nomina , name='nomina'),
    path('Contratos/', views.Contratos , name='Contratos'),
    path('Parametrizacion/', views.Parametrizacion , name='Parametrizacion'),

    #NOMINA PERSONAL
    path('Nomina_personal/', views.Nomina_personal , name='Nomina_personal'),
    path('Nomina_personal/add', views.agregar_nomina_personal , name='agregar_nomina_personal'),
    path('Nomina_personal/edit/<int:nomina_id>/', views.editar_nomina_personal , name='editar_nomina_personal'),

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
