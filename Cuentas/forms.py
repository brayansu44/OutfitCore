from django import forms
from django.utils.timezone import localtime
from .models import *

class FacturaVentaForm(forms.ModelForm):
    fecha_vencimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        required=True
    )

    class Meta:
        model = FacturaVenta
        fields = [
            'numero_factura', 'cliente', 'fecha_vencimiento', 'monto_total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"
        
        if self.instance and self.instance.fecha_vencimiento:
            self.initial['fecha_vencimiento'] = self.instance.fecha_vencimiento.strftime('%Y-%m-%d')