from django.db import models
from deep_translator import GoogleTranslator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Diseno(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    imagen = models.ImageField(upload_to='productos', blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name='Diseño'
        verbose_name_plural='Diseños'
    
class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Color(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    nombre_en_ingles = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.nombre_en_ingles:  # Solo traducir si el campo está vacío
            self.nombre_en_ingles = GoogleTranslator(source='es', target='en').translate(self.nombre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name='Color'
        verbose_name_plural='Colores'

    def __str__(self):
        return self.nombre
    
class Talla(models.Model):
    nombre = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre    

class Producto(models.Model):
    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('No disponible', 'No disponible'),
    ]
    codigo              = models.CharField(max_length=50, unique=True)
    referencia          = models.CharField(max_length=100)
    diseno              = models.ManyToManyField(Diseno, related_name="productos", blank=True)
    color               = models.ManyToManyField(Color, related_name="productos", blank=False)
    talla               = models.ManyToManyField(Talla, related_name="productos", blank=False)
    categoria           = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos")
    genero              = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos")
    descripcion         = models.TextField(blank=True)
    estado              = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Disponible')
    fecha_creacion      = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        colores = ", ".join([color.nombre for color in self.color.all()]) if self.color.exists() else "Sin colores"
        tallas = ", ".join([talla.nombre for talla in self.talla.all()]) if self.talla.exists() else "Sin tallas"
        return f"{self.codigo} - {self.referencia} (Colores: {colores} | Tallas: {tallas})"

class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="variantes")
    color    = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="variantes")
    talla    = models.ForeignKey(Talla, on_delete=models.CASCADE, related_name="variantes")
    diseno   = models.ForeignKey(Diseno, on_delete=models.CASCADE, null=True, blank=True, related_name="variantes")

    class Meta:
        unique_together = ('producto', 'color', 'talla', 'diseno')  

    def __str__(self):
        return f"{self.producto.referencia} - {self.color.nombre} - {self.talla.nombre} - {self.diseno.nombre if self.diseno else 'Sin diseño'}"
    
    def get_codigo_barra(self):
        return f"{self.producto.codigo}-{self.color.nombre}-{self.talla.nombre}"

