from django.db import models
from proveedores.models import Proveedor
# Create your models here.


# Modelos locales
class Ingresos_Producto(models.Model):
    Fecha           = models.DateField(null=False, blank=False)
    ProductoID = models.ForeignKey("Producto.Producto", on_delete=models.CASCADE)
    ProveedorID     = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    Cantidad        = models.IntegerField(null=False, blank=False)
    UserResponsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)
    Estados = (
        ('Activo', 'Active'),
        ('Inactivo', 'Inactive'),
    )
    Estado          = models.CharField(max_length=50, choices=Estados, default='Activo')

class Salidas_Producto(models.Model):
    Fecha           = models.DateField(null=False, blank=False)
    ProductoID = models.ForeignKey("Producto.Producto", on_delete=models.CASCADE)
    ProveedorID     = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    Cantidad        = models.IntegerField(null=False, blank=False)
    UserResponsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)
    Estados = (
        ('Activo', 'Active'),
        ('Inactivo', 'Inactive'),
    )
    Estado          = models.CharField(max_length=50, choices=Estados, default='Activo')
    LocalID         = models.ForeignKey("locales.InventarioLocal", on_delete=models.CASCADE)

class Unidad_Medida(models.Model):
    Nombre    = models.CharField(max_length=100, unique=True, null=False, blank=False)

class Tipo_insumo(models.Model):
    Nombre    = models.CharField(max_length=100, unique=True, null=False, blank=False)

class Insumo(models.Model):
    Nombre          = models.CharField(max_length=100, unique=True, null=False, blank=False)
    Tipo_insumoID   = models.ForeignKey(Tipo_insumo, on_delete=models.CASCADE)
    Unidad_MedidaID = models.ForeignKey(Unidad_Medida, on_delete=models.CASCADE)
    Cantidad        = models.IntegerField(null=False, blank=False)
    Estados = (
        ('Activo', 'Active'),
        ('Inactivo', 'Inactive'),
    )
    Estado          = models.CharField(max_length=50, choices=Estados, default='Activo')

class Ingresos_insumo(models.Model):
    InsumoID        = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    Fecha           = models.DateField(null=False, blank=False)
    Cantidad        = models.IntegerField(null=False, blank=False)
    ProveedorID     = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    UserResponsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)

class Uso_Insumo(models.Model):
    InsumoID        = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    ProductoID      = models.ForeignKey("Producto.Producto", on_delete=models.CASCADE)
    Fecha           = models.DateField(null=False, blank=False)
    Cantidad        = models.IntegerField(null=False, blank=False)
    Observaciones_Destino = models.CharField(max_length=100)
    UserResponsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)