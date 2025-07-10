"""
URL configuration for kiddes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('home/<int:empresa_id>/', views.home_with_empresa, name='home_with_empresa'),
    path('set_empresa/<int:empresa_id>/', views.set_empresa_id, name='set_empresa_id'),
    path('', include('usuarios.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('trazabilidad/', include('trazabilidad.urls')),
    path('productos/', include('Producto.urls')),
    path('empresas/', include('empresas.urls')),
    path('locales/', include('locales.urls')),
    path('bodega/', include('bodega.urls')),
    path('notificaiones/', include('notificaciones.urls')),
    path('nomina/', include('nomina.urls')),
    path('cuentas/', include('Cuentas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
