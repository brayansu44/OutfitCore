from django.db import models
from django.core.exceptions import ValidationError
from Producto.models import ProductoVariante

class Empresa(models.Model):
    razon_social            = models.CharField(max_length=100)
    nit                     = models.CharField(max_length=20, unique=True)
    telefono                = models.CharField(max_length=20, unique=True)
    correo                  = models.EmailField(max_length=100, unique=True)
    logo                    = models.ImageField(upload_to='empresas', blank=False, null=False)

    def __str__(self):
        return self.razon_social

class Area(models.Model):
    nombre      = models.CharField(max_length=100, unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=100)
    empresa     = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre



