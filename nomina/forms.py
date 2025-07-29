from django import forms
from .models import *

class NominaForm(forms.ModelForm):

    periodo_pago = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'month'}
        ),
        required=True
    )

    class Meta:
        model = Nomina
        fields = [
            'periodo_pago', 'contrato', 'devengado', 'deducciones']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class EPSForm(forms.ModelForm):
    class Meta:
        model = EPS
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['estado'].empty_label = "Seleccione un estado"
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

class ARLForm(forms.ModelForm):
    class Meta:
        model = ARL
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['estado'].empty_label = "Seleccione un estado"
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

class PENSIONForm(forms.ModelForm):
    class Meta:
        model = Pension
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['estado'].empty_label = "Seleccione un estado"
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

class CAJAForm(forms.ModelForm):
    class Meta:
        model = CajaCompensacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['estado'].empty_label = "Seleccione un estado"
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})


class DevengadoForm(forms.ModelForm):
    class Meta:
        model = Devengado
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class DeduccionesForm(forms.ModelForm):
    class Meta:
        model = Deducciones
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ProvisionesForm(forms.ModelForm):
    class Meta:
        model = Provisiones
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AportesParafiscalForm(forms.ModelForm):
    class Meta:
        model = AportesParafiscal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})