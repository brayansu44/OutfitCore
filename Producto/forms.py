from django import forms
from .models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'referencia', 'diseno',
            'color', 'talla', 'categoria',
            'genero', 'estado', 'descripcion'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['categoria'].empty_label = "Seleccione una categoria"
        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})

        self.fields['genero'].empty_label = "Seleccione un genero"
        self.fields['genero'].widget.attrs.update({'class': 'form-select'})

        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

        # Agrega la clase necesaria para el dual-listbox
        self.fields['color'].widget.attrs.update({'class': 'dual-listbox'})
        self.fields['talla'].widget.attrs.update({'class': 'dual-listbox'})
        self.fields['diseno'].widget.attrs.update({'class': 'dual-listbox'})
