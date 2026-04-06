from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.fields.CharField):
    # En vez de un modelo separado podemos usar las opciones de choices para el rol, pero la especificación pide un modelo ROL.
    pass

class RolModel(models.Model):
    class Opciones(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        TESORERO = 'tesorero', 'Tesorero'
        OPERADOR = 'operador', 'Operador'
        
    nombre = models.CharField(max_length=20, choices=Opciones.choices, unique=True)
    
    def __str__(self):
        return self.get_nombre_display()

class Usuario(AbstractUser):
    # La especificación: id_usuario (PK es heredada o abstracta), id_rol (FK a ROL), nombre_usuario, password_hash, nombre_completo, activo. Abstract User cubre varias.
    rol = models.ForeignKey(RolModel, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_completo = models.CharField(max_length=255, blank=True)
    dni = models.CharField(max_length=8, unique=True)
    # is_active y password vienen de AbstractUser. username viene de abstractUser.
    
    def __str__(self):
        return self.username

class Titular(models.Model):
    TIPO_CHOICES = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    def __str__(self):
        if self.tipo == 'natural' and hasattr(self, 'personanatural'):
            return f"{self.personanatural.nombres} {self.personanatural.apellidos}"
        elif self.tipo == 'juridica' and hasattr(self, 'personajuridica'):
            return self.personajuridica.razon_social
        return f"Titular {self.id}"

class PersonaNatural(models.Model):
    titular = models.OneToOneField(Titular, on_delete=models.CASCADE, primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class PersonaJuridica(models.Model):
    titular = models.OneToOneField(Titular, on_delete=models.CASCADE, primary_key=True)
    razon_social = models.CharField(max_length=255)
    ruc = models.CharField(max_length=11, unique=True)
    representante = models.ForeignKey(Titular, related_name='representante_de', on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.razon_social
