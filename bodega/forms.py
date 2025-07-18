from django import forms
from django.forms import modelformset_factory
from .models import SalidaProducto, InventarioLocal, Stock, EntregaCorte, Insumo, IngresoInsumo, DetalleIngresoInsumo, UsoInsumo
from usuarios.models import PerfilUsuario

class SalidaProductoForm(forms.ModelForm):
    class Meta:
        model = SalidaProducto
        fields = ['producto', 'cantidad', 'local', 'estado']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Aplicar clase 'form-control' a todos los widgets visibles
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Filtrar locales únicos por ID
        locales_unicos = {}
        for inventario in InventarioLocal.objects.select_related("local", "local__empresa").all():
            locales_unicos[inventario.local.id] = inventario

        self.fields['local'].queryset = InventarioLocal.objects.filter(id__in=[inv.id for inv in locales_unicos.values()])
        self.fields['local'].label_from_instance = lambda obj: f"{obj.local.nombre} - {obj.local.empresa.razon_social}"

        self.fields['producto'].empty_label = "Seleccione un producto"
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})

        self.fields['local'].empty_label = "Seleccione un local"
        self.fields['local'].widget.attrs.update({'class': 'form-select'})

        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        try:
            perfil_usuario = PerfilUsuario.objects.get(usuario=self.request.user)
        except PerfilUsuario.DoesNotExist:
            raise forms.ValidationError("El usuario logueado no tiene un perfil asociado.")
        instance.user_responsable = perfil_usuario
        if commit:
            instance.save()
        return instance
    
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['producto_variante', 'cantidad']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['producto_variante'].empty_label = "Seleccione una variante"
        self.fields['producto_variante'].widget.attrs.update({'class': 'form-select'})

class EntregaCorteForm(forms.ModelForm):
    class Meta:
        model = EntregaCorte
        fields = ['producto', 'cantidad', 'cantidad_lavado']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['producto'].empty_label = "Seleccione una variante"
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'tipo_insumo', 'unidad_medida']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['tipo_insumo'].empty_label = "Seleccione un tipo de insumo"
        self.fields['tipo_insumo'].widget.attrs.update({'class': 'form-select'})

        self.fields['unidad_medida'].empty_label = "Seleccione una unidad de medida"
        self.fields['unidad_medida'].widget.attrs.update({'class': 'form-select'})

class IngresoInsumoForm(forms.ModelForm):
    class Meta:
        model = IngresoInsumo
        fields = ['insumo', 'cantidad', 'proveedor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['insumo'].empty_label = "Seleccione un insumo"
        self.fields['insumo'].widget.attrs.update({'class': 'form-select'})

        self.fields['proveedor'].empty_label = "Seleccione un proveedor"
        self.fields['proveedor'].widget.attrs.update({'class': 'form-select'})


class UsoInsumoForm(forms.ModelForm):
    class Meta:
        model = UsoInsumo
        fields = ['insumo', 'producto', 'cantidad', 'uso_destino', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['insumo'].empty_label = "Seleccione un insumo"
        self.fields['insumo'].widget.attrs.update({'class': 'form-select'})

        self.fields['producto'].empty_label = "Seleccione un producto"
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})
