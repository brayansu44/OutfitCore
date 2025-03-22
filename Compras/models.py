from django.db import models
from empresas.models import Empresa
from usuarios.models import PerfilUsuario
from Cuentas.models import FacturaCompra
from proveedores.models import Proveedor

# Create your models here.
class Compras(models.Model):
    Fecha           = models.DateField(null=False, blank=False)
    ProveedorID     = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    UserResponsable = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    EmpresaID       = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    Factura         = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)

class Gastos_Operativos(models.Model):
    Fecha           = models.DateField(null=False, blank=False)
    Tipo_gasto      = models.CharField(max_length=50)
    Factura         = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)
    UserResponsable = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name="Solicitante")
    Aprobador       = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name="Autorizador")
    EmpresaID       = models.ForeignKey(Empresa, on_delete=models.CASCADE)