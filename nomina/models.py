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
    ibc                   = models.FloatField(null=False, default=0)
    salario               = models.FloatField(null=False, default=1423500) # Salario Minimo

    def __str__(self):
        return f"{self.perfil.full_name()} - {self.empresa.razon_social} ({self.local.nombre if self.local else 'Sin local'})"

    
# 📌 Modelo Devengado
class Devengado(models.Model):
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    auxilio_transporte  = models.FloatField(null=False, default=200000)
    comisiones          = models.FloatField(null=True, default=0)
    dias_liquidados     = models.IntegerField(null=False, default=0)
    horas_extras_diurna = models.IntegerField(null=False, default=0) # Porcentaje adicional (25%)
    total_horas_extras_diurna = models.FloatField(null=True, default=0)
    horas_extras_nocturna = models.IntegerField(null=False, default=0) # Porcentaje adicional (75%)
    total_horas_extras_nocturna = models.FloatField(null=True, default=0)
    horas_extras_diurna_dominical = models.IntegerField(null=False, default=0) # Porcentaje adicional (100%)
    total_horas_extras_diurna_dominical = models.FloatField(null=True, default=0)
    horas_extras_nocturna_dominical = models.IntegerField(null=False, default=0) # Porcentaje adicional (150%)
    total_horas_extras_nocturna_dominical = models.FloatField(null=True, default=0)
    recargos_nocturnos  = models.IntegerField(null=False, default=0) #Sin hora extra Porcentaje adicional (35%)
    total_recargos_nocturnos = models.FloatField(null=True, default=0)
    recargos_dominical  = models.IntegerField(null=False, default=0) #Sin hora extra Porcentaje adicional (75%)
    total_recargos_dominical = models.FloatField(null=True, default=0)
    recargos_nocturnos_dominical = models.IntegerField(null=False, default=0) #Sin hora extra Porcentaje adicional (110%)
    total_recargos_nocturnos_dominical = models.FloatField(null=True, default=0)
    ibc                 = models.FloatField(null=False, default=0)
    total               = models.FloatField(null=False, default=0)

    def aux_transporte(self):
        self.auxilio_transporte = (200000 / 30) * self.dias_liquidados
    
    def calculo_valores(self):
        # Valor hora ordinaria
        valor_hora = self.contrato.salario / 220 # la jornada máxima legal es de 44 horas semanales, lo que equivale a 220 horas mensuales

        # Cálculo de hora extra diurna (25% adicional)
        valor_horas_extras_diurna = valor_hora * 1.25
        self.total_horas_extras_diurna = self.horas_extras_diurna * valor_horas_extras_diurna

        # Cálculo de hora extra nocturnas (75% adicional)
        valor_horas_extras_nocturna = valor_hora * 1.75
        self.total_horas_extras_nocturna = self.horas_extras_nocturna * valor_horas_extras_nocturna

        # Cálculo de hora extra nocturnas (100% adicional)
        valor_horas_extras_diurna_dominical = valor_hora * 2
        self.total_horas_extras_diurna_dominical = self.horas_extras_diurna_dominical * valor_horas_extras_diurna_dominical

        # Cálculo de hora extra nocturnas (150% adicional)
        valor_horas_extras_nocturna_dominical = valor_hora * 2.5
        self.total_horas_extras_nocturna_dominical = self.horas_extras_nocturna_dominical * valor_horas_extras_nocturna_dominical

        # Cálculo de hora extra nocturnas (35% adicional)
        valor_recargos_nocturnos = valor_hora * 1.35
        self.total_recargos_nocturnos = self.recargos_nocturnos * valor_recargos_nocturnos

        # Cálculo de hora extra nocturnas (75% adicional)
        valor_recargos_dominical = valor_hora * 1.75
        self.total_recargos_dominical = self.recargos_dominical * valor_recargos_dominical

        # Cálculo de hora extra nocturnas (110% adicional)
        valor_recargos_nocturnos_dominical = valor_hora * 2.1
        self.total_recargos_nocturnos_dominical = self.recargos_nocturnos_dominical * valor_recargos_nocturnos_dominical

    def calcular_total(self):
        base = (self.contrato.salario / 30) * self.dias_liquidados
        return  base + self.auxilio_transporte + self.comisiones + self.total_horas_extras_diurna + self.total_horas_extras_nocturna + self.total_horas_extras_diurna_dominical + self.total_horas_extras_nocturna_dominical + self.total_recargos_nocturnos + self.total_recargos_dominical + self.total_recargos_nocturnos_dominical

    def calcular_ibc(self):
        base = (self.contrato.salario / 30) * self.dias_liquidados
        return base + self.comisiones + self.total_horas_extras_diurna + self.total_horas_extras_nocturna + self.total_horas_extras_diurna_dominical + self.total_horas_extras_nocturna_dominical + self.total_recargos_nocturnos + self.total_recargos_dominical + self.total_recargos_nocturnos_dominical

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        self.ibc = self.calcular_ibc()

        # Actualizar el campo ibc en contrato
        contrato = self.contrato
        contrato.ibc = self.ibc
        contrato.save(update_fields=["ibc"])  # solo guarda ese campo
        super().save(*args, **kwargs)

    def __str__(self):
        return self.contrato.perfil.full_name()

# 📌 Modelo Deducciones
class Deducciones(models.Model):
    contrato   = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    salud      = models.FloatField(null=False, default=0) # 4% a cargo del empleado
    pension    = models.FloatField(null=False, default=0) # 4% a cargo del empleado
    fondo      = models.FloatField(null=False, default=0) # voluntario
    retencion  = models.FloatField(null=False, default=0)
    otros      = models.FloatField(null=False, default=0)
    total      = models.FloatField(null=False, default=0)

    def calculo_valores(self):
        base = self.contrato.ibc or 0 # Ingreso Base de Cotización

        # Aportes obligatorios del empleado
        self.salud = base * 0.04  # 4% salud
        self.pension = base * 0.04  # 4% pensión

    def total_deducciones(self):
        return self.salud + self.pension + self.fondo + self.retencion + self.otros
    
    def save(self, *args, **kwargs):
        self.calculo_valores()
        self.total = self.total_deducciones()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.contrato.perfil.full_name()
    
# 📌 Modelo Nómina
class Nomina(models.Model):
    periodo_pago        = models.DateField(null=False, default=timezone.now)
    fecha_liquidacion   = models.DateField(auto_now_add=True)
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    devengado           = models.OneToOneField(Devengado, on_delete=models.CASCADE)
    deducciones         = models.OneToOneField(Deducciones, on_delete=models.CASCADE)
    neto_pagado         = models.FloatField(default=0)

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
    
# 📌 Modelo Aportes Parafiscales
class AportesParafiscal(models.Model):
    nomina            = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    sena                = models.FloatField(null=False, default=0) #Servicio Nacional de Aprendizaje (2%)
    icbf                = models.FloatField(null=False, default=0) #Instituto Colombiano de Bienestar Familiar (3%)
    ccf                 = models.FloatField(null=False, default=0) #Cajas de Compensación Familiar (4%)
    aporte_salud        = models.FloatField(null=False, default=0)
    total               = models.FloatField()

    class Meta:
        verbose_name = 'Aporte Parafiscal'
        verbose_name_plural = 'Aportes Parafiscales'

    def save(self, *args, **kwargs):

        ibc = self.nomina.contrato.ibc or 0
        self.sena = ibc * 0.02
        self.icbf = ibc * 0.03
        self.ccf = ibc * 0.04
        self.total = self.sena + self.icbf + self.ccf + self.aporte_salud

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Aportes Parafiscales - {self.nomina.contrato.perfil}"
    
# 📌 Modelo Provisiones
class Provisiones(models.Model):
    niveles = (
        ('1', 'Nivel 1'),
        ('2', 'Nivel 2'),
        ('3', 'Nivel 3'),
        ('4', 'Nivel 44'),
        ('5', 'Nivel 5'),
    )
    nomina              = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    pension             = models.FloatField(null=False, default=0) # 12% a cargo del empleador
    salud               = models.FloatField(null=False, default=0) # 8.5% a cargo del empleador
    nivel_riesgo        = models.CharField(max_length=50, choices=niveles, default="1")
    riesgo_laboral      = models.FloatField(null=False, default=0) # 0.522% y 6.96% a cargo del empleador
    prima               = models.FloatField(null=False, default=0) # 8.33% a cargo del empleador
    cesantias           = models.FloatField(null=False, default=0) # 8.33% a cargo del empleador
    interes_cesantias   = models.FloatField(null=False, default=0) # 12% anual sobre las cesantías a cargo del empleador
    vacaciones          = models.FloatField(null=False, default=0) # 4.17% a cargo del empleador
    aportes_parafiscal  = models.ForeignKey(AportesParafiscal, on_delete=models.CASCADE)
    total               = models.FloatField()

    class Meta:
        verbose_name = 'Provision'
        verbose_name_plural = 'Provisiones'

    def calcular_riesgo_laboral(self, ibc, nivel):
        niveles_riesgo = {
            '1': 0.00522,
            '2': 0.01044,
            '3': 0.02436,
            '4': 0.0435,
            '5': 0.0696
        }
        porcentaje = niveles_riesgo.get(nivel, 0.00522)
        return ibc * porcentaje 

    def calcular_total(self):
        ibc = self.nomina.contrato.ibc or 0
        self.pension = ibc * 0.12
        self.salud = ibc * 0.085
        self.riesgo_laboral = self.calcular_riesgo_laboral(ibc, self.nivel_riesgo)
        self.prima = ibc * 0.0833
        self.cesantias = ibc * 0.0833
        self.interes_cesantias = self.cesantias * 0.12
        self.vacaciones = ibc * 0.0417

        total_aportes = self.aportes_parafiscal.total or 0

        return sum([
            self.pension,
            self.salud,
            self.riesgo_laboral,
            self.prima,
            self.cesantias,
            self.interes_cesantias,
            self.vacaciones,
            total_aportes
        ])

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.contrato.perfil


    
