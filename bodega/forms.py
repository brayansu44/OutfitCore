from django import forms
from .models import SalidaProducto, InventarioLocal
from usuarios.models import PerfilUsuario

class SalidaProductoForm(forms.ModelForm):
    class Meta:
        model = SalidaProducto
        fields = ['producto', 'cantidad', 'local', 'estado']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Capturar la request
        super().__init__(*args, **kwargs)

        # Filtrar locales únicos por ID
        locales_unicos = {}
        for inventario in InventarioLocal.objects.select_related("local", "local__empresa").all():
            locales_unicos[inventario.local.id] = inventario  # Guarda solo un inventario por local

        self.fields['local'].queryset = InventarioLocal.objects.filter(id__in=[inv.id for inv in locales_unicos.values()])
        self.fields['local'].label_from_instance = lambda obj: f"{obj.local.nombre} - {obj.local.empresa.razon_social}"

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Obtener el perfil del usuario logueado
        try:
            perfil_usuario = PerfilUsuario.objects.get(usuario=self.request.user)
        except PerfilUsuario.DoesNotExist:
            raise forms.ValidationError("El usuario logueado no tiene un perfil asociado. Asegúrate de que el usuario tenga un perfil en PerfilUsuario.")

        instance.user_responsable = perfil_usuario  # Asignar el perfil al responsable

        if commit:
            instance.save()
        return instance
