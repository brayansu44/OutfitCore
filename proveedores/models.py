from django.db import models
from usuarios.models import PerfilUsuario

# Create your models here.
class Proveedor(models.Model):
    UserResponsable       = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    Razon_Social          = models.CharField(max_length=100, null=False, blank=False)
    Tipo_documentos=(
        ('C.C.','C.C'),
        ('NIT.','NIT.'),
        ('PAS','PAS'),
    )
    Tipo_documento          = models.CharField(max_length=50, choices=Tipo_documentos, default='NIT')
    Identificacion          = models.IntegerField(unique=True, null=False, blank=False)
    Telefono                = models.IntegerField()
    Correo                  = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    Ciudad                  = models.CharField(max_length=100)
    Direccion               = models.CharField(max_length=100)
    Fecha_Inicio_Actividad  = models.DateField(null=False, blank=False)
    
    class Meta:
        verbose_name='Proveedor'
        verbose_name_plural='Proveedores'

    def __str__(self):
        return f"{self.Razon_Social} ({self.Tipo_documento} {self.Identificacion})"    