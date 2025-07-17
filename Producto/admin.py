from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Diseno, Genero, Color, Producto, Talla, ProductoVariante, ImagenDiseno

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

class ImagenDisenoInline(admin.TabularInline):
    model = ImagenDiseno
    extra = 1

@admin.register(Diseno)
class DisenoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ver_imagenes")
    inlines = [ImagenDisenoInline]

    def ver_imagenes(self, obj):
        imagenes = obj.imagenes.all()
        if not imagenes:
            return "(Sin imágenes)"
        return format_html("".join([
            f'<img src="{img.imagen.url}" width="60" height="60" style="margin:2px; border-radius:4px;" />'
            for img in imagenes
        ]))
    ver_imagenes.short_description = "Imágenes"

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    readonly_fields = ('nombre_en_ingles',)
    search_fields = ('nombre',)
    ordering = ('nombre',)
    fields = ('nombre',)

@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)         

class ProductoVarianteInline(admin.TabularInline):  
    """ Muestra las variantes dentro del producto, pero sin edición manual """
    model = ProductoVariante
    extra = 0
    readonly_fields = ('producto', 'color', 'talla', 'diseno')
    can_delete = False  # Evita eliminaciones manuales

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'referencia', 'categoria', 'estado', 'mostrar_tallas', 'mostrar_colores', 'mostrar_disenos', 'fecha_creacion')
    list_filter = ('estado', 'categoria', 'talla', 'genero', 'color')
    search_fields = ('codigo', 'referencia', 'color__nombre', 'categoria__nombre')
    ordering = ('-fecha_creacion',)
    filter_horizontal = ('diseno', 'color', 'talla')  
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    inlines = [ProductoVarianteInline]  # Muestra variantes dentro del producto

    def mostrar_tallas(self, obj):
        return ", ".join([talla.nombre for talla in obj.talla.all()])
    mostrar_tallas.short_description = "Tallas"

    def mostrar_colores(self, obj):
        return ", ".join([color.nombre for color in obj.color.all()])
    mostrar_colores.short_description = "Colores"

    def mostrar_disenos(self, obj):
        disenios_html = ""
        for diseno in obj.diseno.all():
            for img in diseno.imagenes.all():
                disenios_html += f'''
                    <div style="display: flex; align-items: center; gap: 8px; margin-top: 5px;">
                        <a href="{img.imagen.url}" target="_blank">
                            <img src="{img.imagen.url}" width="50" height="50" 
                            style="border-radius:5px; object-fit:cover; cursor:pointer;" />
                        </a>
                        <span style="font-size: 12px; color: #666;">{diseno.nombre}</span>
                    </div>
                '''
        return format_html(disenios_html) if disenios_html else "(Sin diseños)"


@admin.register(ProductoVariante)
class ProductoVarianteAdmin(admin.ModelAdmin):
    list_display = ('producto', 'color', 'talla', 'diseno')
    list_filter = ('producto', 'color', 'talla', 'diseno')
    search_fields = ('producto__referencia', 'color__nombre', 'talla__nombre', 'diseno__nombre')
    readonly_fields = ('producto', 'color', 'talla', 'diseno')

    def has_add_permission(self, request):  
        return False  # Evita creación manual

    def has_change_permission(self, request, obj=None):  
        return False  # Evita edición

    def has_delete_permission(self, request, obj=None):  
        return True  # Evita eliminación

