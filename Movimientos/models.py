from django.db import models

# Create your models here.
class Cuenta(models.Model):
    TIPO = (
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto'),
    )
    nombre  = models.CharField(max_length=100)
    tipo    = models.CharField(max_length=50, choices=TIPO, default='Ingreso')

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class CategoriaMercaderia(models.Model):
    nombre  = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Ingreso(models.Model):
    fecha       = models.DateField()
    cuenta      = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    categoria   = models.ForeignKey(CategoriaMercaderia, on_delete=models.CASCADE, null=True, blank=True)
    cantidad    = models.PositiveIntegerField()
    monto       = models.FloatField()
    detalle     = models.TextField(blank=True, null=True)
    documento   = models.PositiveIntegerField()
    mes         = models.CharField(max_length=20)
    anio        = models.PositiveIntegerField()

    def __str__(self):
        return f"Ingreso {self.cantidad} unidades - {self.monto} $"

class Egreso(models.Model):
    fecha               = models.DateField()
    cuenta              = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    categoria           = models.ForeignKey(CategoriaMercaderia, on_delete=models.CASCADE, null=True, blank=True)
    cantidad            = models.PositiveIntegerField()
    monto               = models.FloatField()
    detalle             = models.TextField(blank=True, null=True)
    factura_remision    = models.CharField(max_length=50, null=True, blank=True)
    mes                 = models.CharField(max_length=20)
    anio                = models.PositiveIntegerField()

    def __str__(self):
        return f"Egreso {self.cantidad} unidades - {self.monto} $"

class RegistroContable(models.Model):
    cuenta          = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    anio            = models.PositiveIntegerField()
    mes             = models.CharField(max_length=20)
    ingresos        = models.PositiveIntegerField()
    gastos          = models.PositiveIntegerField()
    saldo_mensual   = models.FloatField()
    saldo_acumulado = models.FloatField()

    @property
    def ingresos(self):
        return Ingreso.objects.filter(cuenta=self.cuenta, anio=self.anio, mes=self.mes).aggregate(models.Sum('monto'))['monto__sum'] or 0

    @property
    def gastos(self):
        return Egreso.objects.filter(cuenta=self.cuenta, anio=self.anio, mes=self.mes).aggregate(models.Sum('monto'))['monto__sum'] or 0

    def __str__(self):
        return f"Registro {self.mes}/{self.anio} - Saldo: {self.saldo_mensual} $"