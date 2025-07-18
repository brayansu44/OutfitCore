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
         
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
            })

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"
                
        
        self.fields['tipo_identificacion'].widget.attrs.update({'class': 'form-select'})


class FacturaVentaForm(forms.ModelForm):
    
    class Meta:
        model = FacturaVenta
        fields = [
            'cliente', 'monto_total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
                })

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        self.fields['cliente'].empty_label = "Seleccione Cliente"
        self.fields['cliente'].widget.attrs.update({'class': 'form-select'})

class PagoVentaForm(forms.ModelForm):

    class Meta:
        model = PagoRecibido
        fields = [
            'factura', 'metodo_pago', 'monto_pagado', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
                })

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"
        
        self.fields['metodo_pago'].widget.attrs.update({'class': 'form-select'})
        self.fields['factura'].empty_label = "Seleccione Factura"
        self.fields['factura'].widget.attrs.update({'class': 'form-select'})

class FacturaCompraForm(forms.ModelForm):

    class Meta:
        model = FacturaCompra
        fields = [
            'proveedor', 'monto_total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
                })

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        self.fields['proveedor'].empty_label = "Seleccione proveedor"
        self.fields['proveedor'].widget.attrs.update({'class': 'form-select'})
        

class PagoForm(forms.ModelForm):

    class Meta:
        model = Pago
        fields = [
            'factura', 'metodo_pago', 'monto_pagado', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
                })

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"
        
        self.fields['metodo_pago'].widget.attrs.update({'class': 'form-select'})
        self.fields['factura'].empty_label = "Seleccione Factura"
        self.fields['factura'].widget.attrs.update({'class': 'form-select'})
