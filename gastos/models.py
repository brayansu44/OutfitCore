from django.db import models
from usuarios.models import PerfilUsuario

# Create your models here.

class Proveedor(models.Model):
    TIPO = [
        ('Tela', 'Tela'),
        ('Insumo', 'Insumo'),
        ('Otros', 'Otros'),
    ]
    nombre          = models.CharField(max_length=100)
    contacto        = models.CharField(max_length=100)
    tipo_proveedor  = models.CharField(max_length=50, choices=TIPO)
    direccion       = models.CharField(max_length=200)
    ciudad          = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.tipo_proveedor}"

class Compra(models.Model):
    fecha_compra    = models.DateField()
    proveedor       = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total_compra    = models.DecimalField(max_digits=10, decimal_places=2)
    responsable     = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compra {self.id} - {self.proveedor.nombre}"

class DetalleCompra(models.Model):
    TIPO = [
        ('Tela', 'Tela'),
        ('Insumo', 'Insumo'),
        ('Otros', 'Otros'),
    ]
    compra              = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="detalles")
    tipo                = models.CharField(max_length=50, choices=TIPO)
    cantidad_comprada   = models.PositiveIntegerField()
    precio_unitario     = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def sub_total(self):
        return self.cantidad_comprada * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad_comprada} x {self.tipo} - {self.compra.proveedor.nombre}"

class GastosOperativos(models.Model):
    TIPO = [
        ('Servicios', 'Servicios'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Transporte', 'Transporte'),
        ('Otros', 'Otros'),
    ]
    fecha       = models.DateField()
    tipo        = models.CharField(max_length=50, choices=TIPO)
    monto       = models.DecimalField(max_digits=10, decimal_places=2)
    responsable = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Gasto Operativo'
        verbose_name_plural = 'Gastos Operativos'

    def __str__(self):
        return f"Gasto {self.tipo} - {self.monto} $"
