from django.db import models
from usuarios.models import PerfilUsuario
from empresas.models import Empresa
from locales.models import Local
from django.core.exceptions import ValidationError

# 📌 Modelo EPS
class EPS(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'EPS'
        verbose_name_plural = 'EPS'

    def __str__(self):
        return self.nombre

# 📌 Modelo ARL
class ARL(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'ARL'
        verbose_name_plural = 'ARL'

    def __str__(self):
        return self.nombre

# 📌 Modelo Pension
class Pension(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Pensión'
        verbose_name_plural = 'Pensiones'

    def __str__(self):
        return self.nombre

# 📌 Modelo Caja de Compensación
class CajaCompensacion(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Caja de Compensación'
        verbose_name_plural = 'Cajas de Compensación'

    def __str__(self):
        return self.nombre

# 📌 Modelo Contrato
class Contrato(models.Model):
    perfil                = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    empresa               = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="Empresa_usuario")
    local                 = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True, related_name="Local_relacionado")
    eps                   = models.ForeignKey(EPS, on_delete=models.SET_NULL, null=True, blank=True)
    pension               = models.ForeignKey(Pension, on_delete=models.SET_NULL, null=True, blank=True)
    arl                   = models.ForeignKey(ARL, on_delete=models.SET_NULL, null=True, blank=True)
    caja_compensacion     = models.ForeignKey(CajaCompensacion, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio          = models.DateField()
    fecha_fin             = models.DateField(null=True, blank=True)
    salario               = models.FloatField()

    def __str__(self):
        return f"Contrato de {self.perfil.full_name} en {self.empresa.razon_social} ({self.local.nombre if self.local else 'Sin local'})"

# 📌 Modelo Devengado
class Devengado(models.Model):
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    auxilio_transporte  = models.FloatField()
    exonerado_aportes   = models.FloatField()
    dias_liquidados     = models.IntegerField()
    horas_extras        = models.IntegerField()
    recargos_nocturnos  = models.IntegerField()
    recargos_dominical  = models.IntegerField()
    total               = models.FloatField()

    def calcular_total(self):
        return self.contrato.salario + self.auxilio_transporte + (self.horas_extras * 1.25) + (self.recargos_nocturnos * 1.35) + (self.recargos_dominical * 1.75)

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Devengado {self.total} - {self.contrato.perfil}"

# 📌 Modelo Deducciones
class Deducciones(models.Model):
    contrato   = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    salud      = models.FloatField()
    pension    = models.FloatField()
    fondo      = models.FloatField()
    retencion  = models.FloatField()
    otros      = models.FloatField()

    def total_deducciones(self):
        return self.salud + self.pension + self.fondo + self.retencion + self.otros

    def __str__(self):
        return f"Deducciones - {self.contrato.perfil}"

# 📌 Modelo Provisiones
class Provisiones(models.Model):
    contrato            = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    pension             = models.FloatField()
    salud               = models.FloatField()
    riesgo_laboral      = models.FloatField()
    sena                = models.FloatField()
    icbf                = models.FloatField()
    caja_compensacion   = models.FloatField()
    prima               = models.FloatField()
    cesantias           = models.FloatField()
    interes_cesantias   = models.FloatField()
    vacaciones          = models.FloatField()
    total               = models.FloatField()

    class Meta:
        verbose_name = 'Provision'
        verbose_name_plural = 'Provisiones'

    def calcular_total(self):
        return sum([
            self.pension, self.salud, self.riesgo_laboral, self.sena, self.icbf, 
            self.caja_compensacion, self.prima, self.cesantias, self.interes_cesantias, self.vacaciones
        ])

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Provisiones - {self.usuario}'

# 📌 Modelo Aportes Parafiscales
class AportesParafiscal(models.Model):
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    sena                = models.FloatField()
    icbf                = models.FloatField()
    caja_compensacion   = models.FloatField()
    aporte_salud        = models.FloatField()

    class Meta:
        verbose_name = 'Aporte Parafiscal'
        verbose_name_plural = 'Aportes Parafiscales'

    def __str__(self):
        return f"Aportes Parafiscales - {self.contrato.perfil}"

# 📌 Modelo Nómina
class Nomina(models.Model):
    fecha_inicio        = models.DateField(null=False, blank=True, default='2025-01-01')
    fecha_fin           = models.DateField(null=False, blank=True, default='2025-01-31')
    fecha_liquidacion   = models.DateField(auto_now_add=True)
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    devengado           = models.OneToOneField(Devengado, on_delete=models.CASCADE)
    deducciones         = models.OneToOneField(Deducciones, on_delete=models.CASCADE)
    provisiones         = models.OneToOneField(Provisiones, on_delete=models.CASCADE)
    aportes_parafiscal  = models.OneToOneField(AportesParafiscal, on_delete=models.CASCADE)
    neto_pagado         = models.FloatField()

    def calcular_neto(self):
        return self.devengado.calcular_total - self.deducciones.total_deducciones()
    
    def clean(self):
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio del periodo de Nomina no puede ser posterior a la fecha de fin.")


    def save(self, *args, **kwargs):
        self.clean()
        self.neto_pagado = self.calcular_neto()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Nómina {self.fecha_inicio} - {self.fecha_fin} - {self.contrato.perfil}"
