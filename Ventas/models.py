from django.db import models

from Cuentas.models import FacturaVenta
from locales.models import Local
from Producto.models import ProductoVariante
from Cuentas.models import Cliente

# Create your models here.

class Ventas(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ]

    local               = models.ForeignKey(Local, on_delete=models.CASCADE)
    #factura             = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    vendedor            = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)
    cliente             = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha               = models.DateField(null=False, blank=False)
    estado              = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    creado_en           = models.DateTimeField(auto_now_add=True)
    actualizado_en      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha} - {self.estado}"
    
    
class DetalleVentas(models.Model):
    venta     = models.ForeignKey(Ventas, on_delete=models.CASCADE, related_name="detalles")
    variante  = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    cantidad    = models.PositiveIntegerField(null=False)
    vr_unidad   = models.FloatField()
    vr_total    = models.FloatField()
    observacion = models.CharField(max_length=200, blank=True)

    def get_codigo_barra(self):
        return self.varianteID.get_codigo_barra()

    def __str__(self):
        return f"{self.variante} x {self.cantidad}"
