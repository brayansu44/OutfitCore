from django import forms
from bodega.models import ConfirmacionRecepcion

class ConfirmacionRecepcionForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea, required=False, label="Observaciones (opcional)")

    class Meta:
        model = ConfirmacionRecepcion
        fields = ["confirmado", "observaciones"]
