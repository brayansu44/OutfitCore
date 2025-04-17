from django import forms
from django.utils.timezone import localtime
from .models import *

class TelaForm(forms.ModelForm):
    class Meta:
        model = Tela
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['proveedor'].empty_label = "Seleccione un proveedor"
        self.fields['proveedor'].widget.attrs.update({'class': 'form-select'}) 

class RolloTelaForm(forms.ModelForm):
    fecha_registro = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        required=True 
    )

    class Meta:
        model = RolloTela
        fields = [
            'numero_rollo', 'numero_referencia', 'referencia', 
            'tela', 'color', 'metros_solicitados', 'largo_inicial', 
            'kilos', 'fecha_registro'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        self.fields['tela'].empty_label = "Seleccione una tela"
        self.fields['tela'].widget.attrs.update({'class': 'form-select'})

        if self.instance and self.instance.fecha_registro:
            self.initial['fecha_registro'] = localtime(self.instance.fecha_registro).strftime('%Y-%m-%dT%H:%M')

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        self.fields['producto'].label_from_instance = lambda obj: obj.referencia
        self.fields['producto'].empty_label = "Seleccione una referencia"
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})

        self.fields['cortador'].empty_label = "Seleccione un cortador"
        self.fields['cortador'].widget.attrs.update({'class': 'form-select'})            

        if 'observaciones' in self.fields:
            observaciones_field = self.fields.pop('observaciones')  
            self.fields['observaciones'] = observaciones_field

class CorteTelaForm(forms.ModelForm):
    fecha_corte = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        required=True
    )

    class Meta:
        model = CorteTela
        fields = [
            'numero_corte', 'orden', 'rollo', 'largo_utilizado',
            'capas_cortadas', 'metros_tendidos',
            'colas', 'metros_dft_gastados',
            'fecha_corte', 'categoria', 'responsable'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        
        self.fields['orden'].empty_label = "Seleccione una orden"
        self.fields['orden'].widget.attrs.update({'class': 'form-select'})   

        self.fields['rollo'].empty_label = "Seleccione un rollo"
        self.fields['rollo'].widget.attrs.update({'class': 'form-select'})  
        
        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})
        self.fields['responsable'].empty_label = "Seleccione un responsable"

        if self.instance and self.instance.fecha_corte:
            self.initial['fecha_corte'] = self.instance.fecha_corte.strftime('%Y-%m-%d')

class TallaCorteForm(forms.ModelForm):

    class Meta:
        model = TallaCorte
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        self.fields['corte'].empty_label = "Seleccione un corte"
        self.fields['corte'].widget.attrs.update({'class': 'form-select'})   

        self.fields['talla'].widget.attrs.update({'class': 'form-select'})          

class RetazoTelaForm(forms.ModelForm):

    fecha_registro = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        required=True
    )

    class Meta:
        model = RetazoTela
        fields = [
            'rollo', 'orden', 'capas_cortadas',
            'metros_tendidos', 'colas', 'faltante', 
            'fecha_registro', 'responsable','observaciones',
        ]
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.label = f"<strong>{field.label if field.label else field_name}</strong>"

        self.fields['rollo'].empty_label = "Seleccione un rollo"
        self.fields['rollo'].widget.attrs.update({'class': 'form-select'})

        self.fields['orden'].empty_label = "Seleccione una orden"
        self.fields['orden'].widget.attrs.update({'class': 'form-select'})

        self.fields['responsable'].empty_label = "Seleccione un cortador"
        self.fields['responsable'].widget.attrs.update({'class': 'form-select'})

        if 'observaciones' in self.fields:
            observaciones_field = self.fields.pop('observaciones')  
            self.fields['observaciones'] = observaciones_field