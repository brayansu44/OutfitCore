from django.db import models
from django.core.exceptions import ValidationError

from Producto.models import ProductoVariante
from empresas.models import Empresa

# Create your models here.
class DiasFuncionamiento(models.Model):
    DIAS_CHOICES = [
        (1, "Lunes"),
        (2, "Martes"),
        (3, "Miércoles"),
        (4, "Jueves"),
        (5, "Viernes"),
        (6, "Sábado"),
        (7, "Domingo"),
    ]
    dia = models.IntegerField(choices=DIAS_CHOICES, unique=True)
 
    def __str__(self):
        return f"{self.get_dia_display()}" 

class Local(models.Model):
    empresa         = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="Empresa_relacionada")
    nombre          = models.CharField(max_length=100)
    telefono        = models.IntegerField()
    direccion       = models.CharField(max_length=255)
    Horario_habil   = models.ManyToManyField(DiasFuncionamiento, related_name="locales")

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locales'

    def __str__(self):
        return f"{self.nombre} - {self.empresa.razon_social}"
    
class InventarioLocal(models.Model):
    local               = models.ForeignKey(Local, on_delete=models.CASCADE, related_name="inventario")
    variante            = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE, related_name="stock_locales")
    entradas            = models.PositiveIntegerField(default=0)
    salidas             = models.PositiveIntegerField(default=0)
    stock_actual        = models.PositiveIntegerField(default=0)
    fecha               = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('local', 'variante')
        verbose_name = 'Inventario Local'
        verbose_name_plural = 'Inventario Local'  

    def clean(self):
        if self.salidas > self.entradas:
            raise ValidationError({'salidas': 'Las salidas no pueden ser mayores que las entradas.'})

    def save(self, *args, **kwargs):
        self.stock_actual = self.entradas - self.salidas
        self.clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.local.nombre} - {self.variante} - Stock: {self.stock_actual} uds"
    
class InventarioSemanal(models.Model):
    local       = models.ForeignKey(Local, on_delete=models.CASCADE)
    variante    = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    semana      = models.DateField()  
    entradas    = models.PositiveIntegerField(default=0)
    salidas     = models.PositiveIntegerField(default=0)
    stock_final = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.local.nombre} - {self.variante.producto.referencia} - {self.semana}"
