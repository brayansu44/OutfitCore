from django.db import models, transaction
from proveedores.models import Proveedor
from django.utils import timezone

# Create your models here.

# Modulo de cuentas por cobrar
class Cliente(models.Model):
    TIPOS_IDENTIFICACION = [
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cedula Ciudadania'),
        ('NIT', 'Número Identificación Tributaria'),
        ('PAS', 'Pasaporte')
    ]
    tipo_identificacion = models.CharField(max_length=50, choices=TIPOS_IDENTIFICACION, null=False, blank=False, default='CC')
    identificacion = models.IntegerField(unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=50, null=False)
    telefono = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_identificacion} {self.identificacion} - {self.nombre}"

class FacturaVenta(models.Model):
    numero_factura      = models.CharField(max_length=20, unique=True, blank=True)
    cliente             = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision       = models.DateField(auto_now_add=True)
    monto_total         = models.FloatField(blank=True)
    saldo_pendiente     = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            año = timezone.now().year
            with transaction.atomic():
                ultima_factura = FacturaVenta.objects.filter(
                    numero_factura__startswith=f"TKV-{año}-"
                ).order_by('-numero_factura').first()

                if ultima_factura:
                    ultimo_numero = int(ultima_factura.numero_factura.split("-")[-1])
                else:
                    ultimo_numero = 0

                nuevo_numero = ultimo_numero + 1
                self.numero_factura = f"TKV-{año}-{nuevo_numero:04d}"
                
        super().save(*args, **kwargs)

    def actualizar_saldo(self):
        pagos = self.pagorecibido_set.aggregate(models.Sum('monto_pagado'))['monto_pagado__sum'] or 0
        self.saldo_pendiente = self.monto_total - pagos
        self.save()

    def __str__(self):
        return f"{self.numero_factura} {self.cliente.tipo_identificacion} {self.cliente.identificacion}"

    class Meta:
        verbose_name = "Factura de Venta"
        verbose_name_plural = "Facturas de Venta"

class PagoRecibido(models.Model):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
    ]
    factura         = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)   
    monto_pagado    = models.FloatField(null=False)
    fecha_pago      = models.DateField(auto_now_add=True)
    metodo_pago     = models.CharField(max_length=50, choices=METODOS_PAGO, default='Efectivo')
    observaciones   = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.factura.actualizar_saldo()

    def __str__(self):
        return f"Pago {self.monto_pagado} - {self.factura.numero_factura}"

    class Meta:
        verbose_name = "Pago Recibido"
        verbose_name_plural = "Pagos Recibidos"

# Modulo de cuentas por pagar
class FacturaCompra(models.Model):
    numero_factura      = models.CharField(max_length=20, unique=True, blank=True)
    proveedor           = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_emision       = models.DateField(auto_now_add=True)
    monto_total         = models.FloatField(blank=True)
    saldo_pendiente     = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            año = timezone.now().year
            with transaction.atomic():
                ultima_factura = FacturaVenta.objects.filter(
                    numero_factura__startswith=f"TKC-{año}-"
                ).order_by('-numero_factura').first()

                if ultima_factura:
                    ultimo_numero = int(ultima_factura.numero_factura.split("-")[-1])
                else:
                    ultimo_numero = 0

                nuevo_numero = ultimo_numero + 1
                self.numero_factura = f"TKC-{año}-{nuevo_numero:04d}"
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_factura} {self.cliente.tipo_identificacion} {self.cliente.identificacion}"

    class Meta:
        verbose_name = "Factura de Compra"
        verbose_name_plural = "Facturas de Compra"   

class Pago(models.Model):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
    ]
    factura         = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)   
    monto_pagado    = models.FloatField()
    fecha_pago      = models.DateField(auto_now_add=True)
    metodo_pago     = models.CharField(max_length=50, choices=METODOS_PAGO, default='Efectivo')
    observaciones   = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.factura.actualizar_saldo()

    def __str__(self):
        return f"Pago {self.monto_pagado} - {self.factura.numero_factura}"

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"   
