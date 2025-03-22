from django.db import models

from Cuentas.models import Cliente, FacturaVenta
from locales.models import Local

# Create your models here.

class Ventas(models.Model):
    LocalID     = models.ForeignKey(Local, on_delete=models.CASCADE)
    Factura     = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    Fecha       = models.DateField(null=False, blank=False)
    ClienteID   = models.ForeignKey(Cliente, on_delete=models.CASCADE)
