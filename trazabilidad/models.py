from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import PerfilUsuario
from proveedores.models import Proveedor
from Producto.models import Producto

class Tela(models.Model):
    nombre      = models.CharField(max_length=100, unique=True, null=False, blank=False)
    proveedor   = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre}"

class RolloTela(models.Model):
    ESTADO = (
        ('Completo', 'Completo'),
        ('Incompleto', 'Incompleto'),
        ('Agotado', 'Agotado'),
    )
    numero_rollo        = models.CharField(max_length=50, db_index=True)
    referencia          = models.CharField(max_length=100, db_index=True)
    numero_referencia   = models.CharField(max_length=50, unique=True)
    tela                = models.ForeignKey(Tela, on_delete=models.CASCADE)
    color               = models.CharField(max_length=50, null=False, blank=False)
    metros_solicitados  = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    largo_inicial       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    largo_restante      = models.DecimalField(max_digits=6, decimal_places=2)
    kilos               = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    estado              = models.CharField(max_length=50, choices=ESTADO, default='Completo')
    fecha_registro      = models.DateTimeField(null=False, blank=False)

    def actualizar_estado(self):
        if self.largo_restante <= 0:
            self.estado = 'Agotado'
        elif self.largo_inicial and self.largo_restante < self.largo_inicial:
            self.estado = 'Incompleto'
        else:
            self.estado = 'Completo'

    def consumir_metros(self, metros):
        if metros <= 0:
            raise ValidationError("Los metros consumidos deben ser mayores a cero.")
        if metros > self.largo_restante:
            raise ValidationError("No hay suficiente tela disponible en el rollo.")
        self.largo_restante -= metros
        self.actualizar_estado()
        self.save()

    def save(self, *args, **kwargs):
        if self.largo_restante is None or self.largo_restante == 0:
            self.largo_restante = self.largo_inicial

        if self.largo_inicial and self.largo_restante > self.largo_inicial:
            raise ValidationError("El largo restante no puede ser mayor al inicial.")
        
        if self.kilos < 0:
            raise ValidationError("El peso no puede ser negativo.")
        self.actualizar_estado()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Rollo {self.numero_rollo} - {self.tela.nombre} - {self.color} - {self.largo_restante}m restantes - Estado: {self.estado}"

class OrdenProduccion(models.Model):
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    )
    fecha = models.DateField(auto_now_add=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="referencia_producto")
    cortador = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name="ordenes_produccion")
    total_unidades = models.PositiveIntegerField()
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    class Meta:
        verbose_name='Orden Producción'
        verbose_name_plural='Ordenes Producción'

    def save(self, *args, **kwargs):
        if self.pk:
            original = OrdenProduccion.objects.get(pk=self.pk)
            if original.estado == "Completada" and self.estado != "Completada":
                raise ValidationError("No se puede modificar una orden ya completada.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Orden: {self.producto.referencia} - {self.total_unidades} unidades - Estado: {self.estado}"

class CorteTela(models.Model):
    CATEGORIA = (
        ('Adulto', 'Adulto'),
        ('Niño', 'Niño'),
    )
    numero_corte = models.CharField(max_length=50, unique=True)
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name="cortes")
    rollo = models.ForeignKey(RolloTela, on_delete=models.CASCADE)
    largo_utilizado = models.DecimalField(max_digits=6, decimal_places=2)
    capas_cortadas = models.PositiveIntegerField()
    metros_tendidos = models.DecimalField(max_digits=6, decimal_places=2)
    medida_tendido_mesa = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    colas = models.DecimalField(max_digits=6, decimal_places=2)
    metros_dft_gastados = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rendimiento_rollo = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_corte = models.DateField()
    categoria = models.CharField(max_length=10, choices=CATEGORIA, default='Adulto')
    responsable = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)

    def calcular_rendimiento(self):
        metros_previos = self.largo_utilizado + self.rollo.largo_restante
        if metros_previos > 0:
            return (self.largo_utilizado / metros_previos) * 100
        return 0

    def calcular_medida_tendido_mesa(self):
        if self.capas_cortadas > 0:
            return self.metros_tendidos / self.capas_cortadas
        return 0

    def save(self, *args, **kwargs):
        self.rendimiento_rollo = self.calcular_rendimiento()
        self.medida_tendido_mesa = self.calcular_medida_tendido_mesa()

        if self.pk is None: 
            if self.largo_utilizado > self.rollo.largo_restante:
                raise ValidationError("No hay suficiente tela en el rollo para realizar este corte.")
            self.rollo.consumir_metros(self.largo_utilizado)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Corte {self.numero_corte} - Orden: {self.orden.producto} - {self.largo_utilizado}m ({self.rollo.tela.nombre})"

class TallaCorte(models.Model):
    TALLA = (
        ('4', '4'),
        ('6', '6'),
        ('8', '8'),
        ('10', '10'),
        ('12', '12'),
        ('14', '14'),
        ('16', '16'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    )
    corte = models.ForeignKey(CorteTela, on_delete=models.CASCADE, related_name="tallas_cortes")
    talla = models.CharField(max_length=2, choices=TALLA, default='S')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"Corte {self.corte.numero_corte} - Talla {self.talla} - {self.cantidad} unidades"
