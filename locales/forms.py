from django import forms
from .models import Local, InventarioLocal

from django import forms
from django.utils.safestring import mark_safe
from .models import Local

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['empresa', 'nombre', 'telefono', 'direccion', 'encargado', 'Horario_habil']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Aplicar clases de estilo
            if field_name in ['empresa', 'encargado']:
                field.widget.attrs.update({'class': 'form-select'})
            elif field_name == 'Horario_habil':
                field.widget.attrs.update({'class': 'dual-listbox'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

            # Etiqueta en negrita con asterisco si es requerido
            if field.required:
                field.label = mark_safe(f"<strong>{field.label} <span style='color:red;'>*</span></strong>")

        # Etiquetas vacías en campos tipo ForeignKey
        self.fields['empresa'].empty_label = "Seleccione una empresa"
        self.fields['encargado'].empty_label = "Seleccione un encargado"

        self.fields['encargado'].empty_label = "Seleccione un encargado"
        self.fields['encargado'].widget.attrs.update({'class': 'form-select'})

        self.fields['Horario_habil'].widget.attrs.update({'class': 'dual-listbox'})


class InventarioLocalForm(forms.ModelForm):
    class Meta:
        model = InventarioLocal
        fields = ['variante', 'entradas', 'salidas', 'stock_actual'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

            # Etiqueta en negrita con asterisco si es requerido
            if field.required:
                field.label = mark_safe(f"<strong>{field.label} <span style='color:red;'>*</span></strong>")

        self.fields['variante'].empty_label = "Seleccione una variante"
        self.fields['variante'].widget.attrs.update({'class': 'form-select'})
        self.fields['stock_actual'].widget.attrs.update({'readonly': 'readonly'})
