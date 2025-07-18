from django import forms
from django.forms import inlineformset_factory
from .models import Ventas, DetalleVentas
from django.utils.timezone import localtime

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
        fields = ['local', 'vendedor', 'fecha', 'estado']  # Agrega más si usas otros campos manuales

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

        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

         # Inicializa fecha si ya existe en la instancia
        if self.instance and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')

class DetalleVentasForm(forms.ModelForm):
    class Meta:
        model = DetalleVentas
        fields = ['variante', 'cantidad', 'vr_unidad']
        widgets = {
            'variante': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'vr_unidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['variante'].empty_label = "Seleccione una variante"

# Formset para DetalleVentas
DetalleVentasFormSet = inlineformset_factory(
    Ventas,
    DetalleVentas,
    form=DetalleVentasForm,  # Aquí se usa el formulario personalizado
    extra=1,
    can_delete=True
)
