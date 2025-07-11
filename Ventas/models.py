from django.db import models

from Cuentas.models import FacturaVenta
from locales.models import Local
from Producto.models import Producto

# Create your models here.

class Ventas(models.Model):
    LocalID     = models.ForeignKey(Local, on_delete=models.CASCADE)
    FacturaID   = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    Fecha       = models.DateField(null=False, blank=False)
    
    
class Item(models.Model):
    ventaID     = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    productoID  = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad    = models.IntegerField(null=False)
    vr_unidad   = models.FloatField(null=False)
    vr_total    = models.FloatField(null=False)
    observacion = models.CharField(max_length=200, blank=True)


