from django.db import models
from accounts.models import Titular
from django.conf import settings

class TipoPredio(models.Model):
    descripcion = models.CharField(max_length=50) # Urbano, Rural
    
    def __str__(self):
        return self.descripcion

class TipoVia(models.Model):
    descripcion = models.CharField(max_length=100) # Avenida, Jirón, Calle, Pasaje
    abreviatura = models.CharField(max_length=10) # Av., Jr., Ca., Pje.
    
    def __str__(self):
        return f"{self.descripcion} ({self.abreviatura})"

class Via(models.Model):
    tipo_via = models.ForeignKey(TipoVia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255) # Los Rosales, Grau
    
    def __str__(self):
        return f"{self.tipo_via.abreviatura} {self.nombre}"

class Direccion(models.Model):
    via = models.ForeignKey(Via, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.via}"

class CajaAgua(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    # Atributos por confirmar (posible lectura de medidor)
    
    def __str__(self):
        return self.codigo

class Predio(models.Model):
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE)
    tipo_predio = models.ForeignKey(TipoPredio, on_delete=models.CASCADE)
    caja_agua = models.OneToOneField(CajaAgua, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    numero_puerta = models.CharField(max_length=20, blank=True, null=True)
    referencia = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Predio {self.id} - {self.direccion} {self.numero_puerta or ''}"

class Tarifa(models.Model):
    tipo_predio = models.ForeignKey(TipoPredio, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.descripcion} - {self.monto}"

class Deuda(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('anulado', 'Anulado'),
    ]
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.PROTECT)
    periodo = models.DateField() # 2024-01-01
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_emision = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Deuda {self.periodo} - {self.predio} - {self.estado}"

class Pago(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Validar pagos parciales restringidos según V1
        if self.monto_pagado < self.deuda.monto_total:
            raise ValueError("No se permiten pagos parciales.")
        super().save(*args, **kwargs)
        # Actualizar deuda a pagado si cubre el monto
        if self.monto_pagado >= self.deuda.monto_total:
            self.deuda.estado = 'pagado'
            self.deuda.save()

    def __str__(self):
        return f"Pago {self.id} de Deuda {self.deuda.id}"

class Comprobante(models.Model):
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE) # Aseguramos un comprobante por pago
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    numero_serie = models.CharField(max_length=20, unique=True, blank=True) # Autoincremental
    fecha_emision = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_serie:
            last = Comprobante.objects.order_by('id').last()
            next_num = (last.id + 1) if last else 1
            self.numero_serie = f"B001-{next_num:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comprobante {self.numero_serie}"
