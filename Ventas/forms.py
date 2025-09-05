from django import forms
from django.forms import inlineformset_factory
from .models import Ventas, DetalleVentas
from django.utils.timezone import localtime
from Producto.models import ProductoVariante
from django.forms import BaseInlineFormSet

class VentaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        required=True
    )

    class Meta:
        model = Ventas
        fields = ['local', 'vendedor', 'cliente', 'fecha', 'metodo_pago', 'estado']  # Agrega más si usas otros campos manuales

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        self.fields['local'].empty_label = "Seleccione un local"
        self.fields['local'].widget.attrs.update({'class': 'form-select'})

        self.fields['vendedor'].empty_label = "Seleccione un vendedor"
        self.fields['vendedor'].widget.attrs.update({'class': 'form-select'})

        self.fields['metodo_pago'].widget.attrs.update({'class': 'form-select'})

        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

        self.fields['cliente'].empty_label = "Seleccione un cliente"
        self.fields['cliente'].widget.attrs.update({'class': 'form-select'})

        # Inicializa fecha si ya existe en la instancia
        if self.instance and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')

class DetalleVentasForm(forms.ModelForm):
    class Meta:
        model = DetalleVentas
        fields = ['variante', 'cantidad', 'vr_unidad', 'descuento_item']
        widgets = {
            'variante': forms.Select(attrs={'class': 'form-select detalle-variante'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'vr_unidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descuento_item': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        local = kwargs.pop('local', None)
        super().__init__(*args, **kwargs)

        placeholder = "Seleccione un producto"

        if local:
            qs = ProductoVariante.objects.filter(
                stock_locales__local=local,
                stock_locales__stock_actual__gt=0
            )
            # construimos choices (primera opción deshabilitada)
            choices = [(None, placeholder)] + [(v.pk, str(v)) for v in qs]
            self.fields['variante'].choices = choices
        else:
            self.fields['variante'].choices = [(None, placeholder)]

        # marcamos el placeholder como deshabilitado
        self.fields['variante'].widget.choices = self.fields['variante'].choices
        self.fields['variante'].widget.attrs.update({'required': True})
        if self.fields['variante'].choices:
            self.fields['variante'].widget.choices = [
                (k, v) if k else (k, {'label': v, 'attrs': {'disabled': True, 'selected': True}})
                for k, v in self.fields['variante'].choices
            ]

class BaseDetalleVentasFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.local = kwargs.pop('local', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['local'] = self.local  # pasamos el local a cada form
        return super()._construct_form(i, **kwargs)

# Formset para DetalleVentas
DetalleVentasFormSet = inlineformset_factory(
    Ventas,
    DetalleVentas,
    form=DetalleVentasForm,
    formset=BaseDetalleVentasFormSet, 
    extra=1,
    can_delete=True
)
