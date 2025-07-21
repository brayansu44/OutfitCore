from django.db import models
from usuarios.models import PerfilUsuario
from empresas.models import Empresa
from locales.models import Local
from django.core.exceptions import ValidationError
from django.utils import timezone

# 📌 Modelo EPS
class EPS(models.Model):
    nombre      = models.CharField(max_length=100, unique=True, null=False)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    estado      = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Activo')

    class Meta:
        verbose_name = 'EPS'
        verbose_name_plural = 'EPS'

    def __str__(self):
        return self.nombre

# 📌 Modelo ARL
class ARL(models.Model):
    nombre      = models.CharField(max_length=100, unique=True, null=False)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    estado      = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Activo')

    class Meta:
        verbose_name = 'ARL'
        verbose_name_plural = 'ARL'

    def __str__(self):
        return self.nombre

# 📌 Modelo Pension
class Pension(models.Model):
    nombre      = models.CharField(max_length=100, unique=True, null=False)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    estado      = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Activo')

    class Meta:
        verbose_name = 'Pensión'
        verbose_name_plural = 'Pensiones'

    def __str__(self):
        return self.nombre

# 📌 Modelo Caja de Compensación
class CajaCompensacion(models.Model):
    nombre      = models.CharField(max_length=100, unique=True, null=False)
    direccion   = models.CharField(max_length=100)
    telefono    = models.IntegerField(unique=True)
    correo      = models.EmailField(max_length=100, unique=True)
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    estado      = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Activo')

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
    auxilio_transporte  = models.FloatField(null=False, default=200000)
    exonerado_aportes   = models.FloatField(null=True, default=0)
    dias_liquidados     = models.IntegerField(null=False, default=0)
    horas_extras_diurna = models.IntegerField(null=False, default=0) # Porcentaje adicional (25%)
    horas_extras_nocturna = models.IntegerField(null=False, default=0) # Porcentaje adicional (75%)
    horas_extras_diurna_dominical = models.IntegerField(null=False, default=0) # Porcentaje adicional (100%)
    horas_extras_nocturna_dominical = models.IntegerField(null=False, default=0) # Porcentaje adicional (150%)
    recargos_nocturnos  = models.IntegerField(null=False, default=0) #Sin hora extra Porcentaje adicional (35%)
    recargos_dominical  = models.IntegerField(null=False, default=0) #Sin hora extra Porcentaje adicional (75%)
    recargos_nocturnos_dominical = models.IntegerField(null=False, default=0) #Sin hora extra Porcentaje adicional (110%)
    ibc                 = models.FloatField()
    total               = models.FloatField()

    def aux_transporte(self):
        self.auxilio_transporte = (200000 / 30) * self.dias_liquidados

    def calcular_total(self):
        base = (self.contrato.salario / 30) * self.dias_liquidados
        hora = (self.contrato.salario / 220) # la jornada máxima legal es de 44 horas semanales, lo que equivale a 220 horas mensuales
        return  base + self.auxilio_transporte + ((self.horas_extras * 1.25)) + (self.recargos_nocturnos * 1.35) + (self.recargos_dominical * 1.75)

    def calcular_ibc(self):
        return((self.contrato.salario /30) * self.dias_liquidados) + self.horas_extras + self

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.contrato.perfil

# 📌 Modelo Deducciones
class Deducciones(models.Model):
    contrato   = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    salud      = models.FloatField(null=False, default=0)
    pension    = models.FloatField(null=False, default=0)
    fondo      = models.FloatField(null=False, default=0)
    retencion  = models.FloatField(null=False, default=0)
    otros      = models.FloatField(null=False, default=0)
    total      = models.FloatField()

    def total_deducciones(self):
        return self.salud + self.pension + self.fondo + self.retencion + self.otros
    
    def save(self, *args, **kwargs):
        self.total = self.total_deducciones()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.contrato.perfil

# 📌 Modelo Nómina
class Nomina(models.Model):
    fecha_inicio        = models.DateField(null=False, blank=True, default=timezone.now().date())
    fecha_fin           = models.DateField(null=False, blank=True)
    fecha_liquidacion   = models.DateField(auto_now_add=True)
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    devengado           = models.OneToOneField(Devengado, on_delete=models.CASCADE)
    deducciones         = models.OneToOneField(Deducciones, on_delete=models.CASCADE)
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
    
# 📌 Modelo Provisiones
class Provisiones(models.Model):
    nomina            = models.ForeignKey(Nomina, on_delete=models.CASCADE)
    pension             = models.FloatField(null=False, default=0)
    salud               = models.FloatField(null=False, default=0)
    riesgo_laboral      = models.FloatField(null=False, default=0)
    sena                = models.FloatField(null=False, default=0)
    icbf                = models.FloatField(null=False, default=0)
    caja_compensacion   = models.FloatField(null=False, default=0)
    prima               = models.FloatField(null=False, default=0)
    cesantias           = models.FloatField(null=False, default=0)
    interes_cesantias   = models.FloatField(null=False, default=0)
    vacaciones          = models.FloatField(null=False, default=0)
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
        return self.nomina.contrato.perfil

# 📌 Modelo Aportes Parafiscales
class AportesParafiscal(models.Model):
    nomina              = models.ForeignKey(Nomina, on_delete=models.CASCADE)
    sena                = models.FloatField(null=False, default=0) #Servicio Nacional de Aprendizaje (2%)
    icbf                = models.FloatField(null=False, default=0) #Instituto Colombiano de Bienestar Familiar (3%)
    ccf                 = models.FloatField(null=False, default=0) #Cajas de Compensación Familiar (4%)
    aporte_salud        = models.FloatField(null=False, default=0)
    total               = models.FloatField()

    class Meta:
        verbose_name = 'Aporte Parafiscal'
        verbose_name_plural = 'Aportes Parafiscales'

    def calcular_total(self):
        base = self.nomina.contrato.salario
        return base

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Aportes Parafiscales - {self.nomina.contrato.perfil}"