from django import forms
from .models import *

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
