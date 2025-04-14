from django.db import models, transaction
from proveedores.models import Proveedor
from Producto.models import ProductoVariante
from locales.models import InventarioLocal
from notificaciones.models import Notificacion
from django.core.exceptions import ValidationError

class EstadoChoices(models.TextChoices):
    PENDIENTE = 'Pendiente', 'Pendiente'
    CONFIRMADO = 'Confirmado', 'Confirmado'
    CANCELADO = 'Cancelado', 'Cancelado'
    COMPLETADO = 'Completado', 'Completado'

class EntregaCorte(models.Model):
    fecha = models.DateField(auto_now_add=True)
    producto = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE, related_name="ingresos")
    cantidad = models.PositiveIntegerField()  
    cantidad_lavado = models.PositiveIntegerField(default=0) 
    user_responsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)

    def clean(self):
        """Validar que la cantidad a lavar no sea mayor que la cantidad total"""
        if self.cantidad_lavado > self.cantidad:
            raise ValidationError("La cantidad a lavar no puede ser mayor que la cantidad total entregada.")

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

        with transaction.atomic():
            # Stock que realmente entra en bodega
            cantidad_a_bodega = self.cantidad - self.cantidad_lavado

            producto_bodega, created = Stock.objects.select_for_update().get_or_create(
                producto_variante=self.producto,
                defaults={'cantidad': cantidad_a_bodega}
            )
            
            if not created:
                producto_bodega.cantidad += cantidad_a_bodega
                producto_bodega.save()

            if self.cantidad_lavado > 0:
                SalidaProducto.objects.create(
                    producto=producto_bodega,  
                    cantidad=self.cantidad_lavado,
                    user_responsable=self.user_responsable,
                    local=None,  
                    estado=EstadoChoices.PENDIENTE,
                    es_lavado=True  
                )

    def __str__(self):
        return f"Entrega Corte {self.cantidad} - {self.producto} (Lavado: {self.cantidad_lavado})"

class Stock(models.Model):
    producto_variante = models.OneToOneField(ProductoVariante, on_delete=models.CASCADE, related_name="bodega_stock")
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.producto_variante} - Stock: {self.cantidad}"

class SalidaProducto(models.Model):
    fecha = models.DateField(auto_now_add=True)
    producto = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="salidas")
    cantidad = models.PositiveIntegerField()
    user_responsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)
    local = models.ForeignKey(InventarioLocal, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=50, choices=EstadoChoices.choices, default=EstadoChoices.PENDIENTE)
    es_lavado = models.BooleanField(default=False)  # Indica si es una salida a lavado

    def save(self, *args, **kwargs):
        es_nueva = self.pk is None  

        if es_nueva:
            if not self.producto:  
                raise ValueError("El producto no puede ser None en una salida.")

            stock, created = Stock.objects.get_or_create(producto_variante=self.producto.producto_variante)

            if stock.cantidad < self.cantidad:
                raise ValueError(f"No hay suficiente stock para la salida de {self.producto}. Stock disponible: {stock.cantidad}")

            # Solo restar del stock si NO es una salida a lavado
            if not self.es_lavado:
                stock.cantidad -= self.cantidad
                stock.save()

            super().save(*args, **kwargs)

            # Crear confirmación de recepción si no es lavado
            if not self.es_lavado:
                ConfirmacionRecepcion.objects.create(salida=self, confirmado=False)

            # Notificación si es una salida normal a un local
            if not self.es_lavado and self.local and self.local.local.encargado:
                Notificacion.objects.create(
                    user=self.local.local.encargado.usuario,
                    mensaje=f"Se ha realizado la salida de {self.cantidad} unidades de {self.producto} hacia {self.local.local}.",
                    tipo="salida",
                    salida=self 
                )

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        tipo = "Lavado" if self.es_lavado else "Salida"
        destino = self.local.local if self.local else "Proceso de Lavado"
        return f"{tipo} {self.cantidad} - {self.producto} -> {destino}"


class EntradaProducto(models.Model):
    fecha = models.DateField(auto_now_add=True)
    salida = models.OneToOneField(SalidaProducto, on_delete=models.CASCADE, related_name="entrada")  
    cantidad = models.PositiveIntegerField(editable=False)  # Se establecerá automáticamente
    user_responsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.salida:
            self.cantidad = self.salida.cantidad 

            
            self.salida.estado = "Completado"
            self.salida.save()

            
            if isinstance(self.salida.producto, Stock):
                stock = self.salida.producto  
            else:
                stock = Stock.objects.filter(producto=self.salida.producto).first()  

            if stock:
                stock.cantidad += self.cantidad
                stock.save()

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Entrada {self.cantidad} - {self.salida.producto} - {self.fecha}"


class ConfirmacionRecepcion(models.Model):
    salida              = models.OneToOneField(SalidaProducto, on_delete=models.CASCADE, related_name="confirmacion")
    fecha_confirmacion  = models.DateTimeField(auto_now_add=True)
    user_encargado      = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE, related_name="confirmaciones", null=True, blank=True)
    confirmado          = models.BooleanField(default=False)
    observaciones       = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)  

        if self.confirmado:
            if not self.salida:
                raise ValueError("La salida asociada no puede ser None.")

            # Asignar el usuario que confirma si no está asignado
            if request and not self.user_encargado:
                if hasattr(request.user, 'perfilusuario'):
                    self.user_encargado = request.user.perfilusuario  

            # Marcar la salida como confirmada
            self.salida.estado = EstadoChoices.CONFIRMADO
            self.salida.save()

            # Si la salida es a lavado, no se actualiza el inventario del local
            if not self.salida.es_lavado:
                # Notificar al usuario responsable
                if self.user_encargado:
                    Notificacion.objects.create(
                        user=self.salida.user_responsable.usuario,
                        mensaje=f"Se confirmó la recepción de {self.salida.cantidad} unidades de {self.salida.producto} en {self.salida.local.local}.",
                        tipo="confirmacion"
                    )

                # Actualizar inventario del local
                inventario_local, created = InventarioLocal.objects.get_or_create(
                    local=self.salida.local.local,  
                    variante=self.salida.producto.producto_variante,
                    defaults={'entradas': 0, 'stock_actual': 0}
                )
                inventario_local.entradas += self.salida.cantidad
                inventario_local.stock_actual += self.salida.cantidad
                inventario_local.save()

        super().save(*args, **kwargs)

    def __str__(self):
        estado = "Confirmado" if self.confirmado else "Pendiente"
        destino = self.salida.local.local if self.salida.local else "Lavado"
        observaciones = self.observaciones[:30] + "..." if self.observaciones else "Sin observaciones"
        return f"Recepción {estado} - {self.salida.producto} -> {destino} ({observaciones})"


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    abrev = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Ejemplo: kg, m, l

    def __str__(self):
        return self.nombre

class TipoInsumo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)  # Permite desactivar tipos en lugar de eliminarlos

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tipo_insumo = models.ForeignKey(TipoInsumo, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_insumo})"

    @property
    def stock_actual(self):
        """Calcula el stock en tiempo real basado en ingresos y usos registrados."""
        ingresos = self.ingresos.aggregate(total=models.Sum('cantidad'))['total'] or 0
        usos = self.usos.aggregate(total=models.Sum('cantidad'))['total'] or 0
        return ingresos - usos
    

class IngresoInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name="ingresos")
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.PositiveIntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    user_responsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=EstadoChoices.choices, default=EstadoChoices.COMPLETADO)

    def save(self, *args, **kwargs):
        """Si el ingreso está completado, actualiza el stock del insumo."""
        super().save(*args, **kwargs)

class UsoInsumo(models.Model):
    DESTINO_CHOICES = [
        ('Costura', 'Costura'),
        ('Otros', 'Otros'),
    ]
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name="usos")
    producto = models.ForeignKey(ProductoVariante, on_delete=models.CASCADE, related_name="insumos_usados")
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.PositiveIntegerField()
    uso_destino = models.CharField(max_length=50, choices=DESTINO_CHOICES, default='Lavado')
    observaciones = models.TextField(null=True, blank=True) 
    user_responsable = models.ForeignKey("usuarios.PerfilUsuario", on_delete=models.CASCADE)

    def clean(self):
        """Valida que haya stock suficiente antes de descontar insumos."""
        if self.cantidad > self.insumo.stock_actual:
            raise ValidationError(f"No hay suficiente stock de {self.insumo.nombre}.")

    def save(self, *args, **kwargs):
        """Descuenta el stock automáticamente al guardar un uso de insumo."""
        self.clean()  # Llama la validación antes de guardar
        super().save(*args, **kwargs)
