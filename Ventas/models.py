from django.db import models

from Cuentas.models import FacturaVenta
from locales.models import Local
from Producto.models import ProductoVariante
from Cuentas.models import Cliente

import secrets
import string

# Create your models here.

class Ventas(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ]

    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
    ]

    codigo                  = models.CharField(max_length=20, unique=True, blank=False, null=False)
    local                   = models.ForeignKey(Local, on_delete=models.CASCADE)
    vendedor                = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE, null=False, blank=False)
    cliente                 = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
    fecha                   = models.DateField(null=False, blank=False)
    subtotal                = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento_porcentaje    = models.FloatField(default=0, help_text="Porcentaje de descuento aplicado a la venta")
    descuento_total         = models.FloatField(default=0, help_text="Valor absoluto de descuento aplicado")
    metodo_pago             = models.CharField(max_length=20, choices=METODOS_PAGO, default='Efectivo', null=False, blank=False)
    cambio                  = models.FloatField(default=0, help_text="Cambio que se le debe dar al cliente")
    iva                     = models.FloatField(default=0.0)
    ganancia                = models.FloatField(default=0.0)
    tiene_devolucion        = models.BooleanField(default=False)  
    estado                  = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    creado_en               = models.DateTimeField(auto_now_add=True)
    actualizado_en          = models.DateTimeField(auto_now=True)
    factura                 = models.OneToOneField(FacturaVenta, on_delete=models.SET_NULL, null=True, blank=True, related_name='venta')

    def save(self, *args, **kwargs):
        if not self.pk:  
            # Guardar primero para tener PK
            super().save(*args, **kwargs)

        # Solo calcular si ya está guardada
        subtotal = sum(det.vr_total for det in self.detalles.all())
        self.subtotal = subtotal
        self.descuento_total = subtotal * (self.descuento_porcentaje / 100)
        base = subtotal - self.descuento_total
        self.iva = base * 0.19
        self.ganancia = sum(det.ganancia_item for det in self.detalles.all())

        super().save(update_fields=["subtotal", "descuento_total", "iva", "ganancia"])

    @property
    def subtotal_calculado(self):
        return sum(det.vr_total for det in self.detalles.all())

    @property
    def total_iva_calculado(self):
        return sum(det.iva_item for det in self.detalles.all())

    @property
    def ganancia_calculada(self):
        return sum(det.ganancia_item for det in self.detalles.all())

    @property
    def total_pagado(self):
        return sum(pago.monto for pago in self.pagos.all())

    @property
    def cambio_calculado(self):
        return max(self.total_pagado - self.subtotal, 0)

    @property
    def saldo_pendiente(self):
        return max(self.subtotal - self.total_pagado, 0)



    def generar_codigo_unico(self, length=12):
        # caracteres que se pueden usar: letras mayúsculas + números
        chars = string.ascii_uppercase + string.digits
        while True:
            codigo = ''.join(secrets.choice(chars) for _ in range(length))
            if not Ventas.objects.filter(codigo=codigo).exists():
                return codigo
    
    def __str__(self):
        return f"Venta {self.id} - {self.fecha} - {self.estado}"

class DetalleVentas(models.Model):
    venta           = models.ForeignKey(Ventas, on_delete=models.CASCADE, related_name="detalles")
    variante        = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE)
    cantidad        = models.PositiveIntegerField(null=False)
    vr_unidad       = models.FloatField()
    vr_total        = models.FloatField()
    iva_item        = models.FloatField(default=0.0)
    ganancia_item   = models.FloatField(default=0.0)
    descuento_item  = models.FloatField(default=0.0)
    observacion = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # calcular el total automáticamente
        self.vr_total = (self.vr_unidad * self.cantidad) - self.descuento_item
        self.iva_item = self.vr_total * 0.19  # ejemplo 19% de IVA
        self.ganancia_item = (self.vr_unidad - self.variante.costo) * self.cantidad
        super().save(*args, **kwargs)


    def get_codigo_barra(self):
        return self.variante.get_codigo_barra()

    def __str__(self):
        return f"{self.variante} x {self.cantidad}"
