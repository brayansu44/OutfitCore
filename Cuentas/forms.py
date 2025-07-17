from django import forms
from django.utils.timezone import localtime
from .models import *


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['direccion'].required = False
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field}</strong>"


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
            'cliente', 'fecha_vencimiento', 'monto_total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"
        
        if self.instance and self.instance.fecha_vencimiento:
            self.initial['fecha_vencimiento'] = self.instance.fecha_vencimiento.strftime('%Y-%m-%d')

class PagoVentaForm(forms.ModelForm):

    class Meta:
        model = PagoRecibido
        fields = [
            'factura', 'metodo_pago', 'monto_pagado', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"
        self.fields['metodo_pago'].empty_label = "Seleccione un metodo de pago"
        self.fields['metodo_pago'].widget.attrs.update({'class': 'form-select'})
        