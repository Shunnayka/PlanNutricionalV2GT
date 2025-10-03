from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    OBJETIVO_OPCIONES = [
        ('perder', 'Perder peso'),
        ('mantener', 'Mantener peso'),
        ('ganar', 'Ganar masa muscular'),
    ]
    
    ACTIVIDAD_OPCIONES = [
        ('sedentario', 'Sedentario'),
        ('ligero', 'Ejercicio ligero'),
        ('moderado', 'Ejercicio moderado'),
        ('intenso', 'Ejercicio intenso'),
        ('atleta', 'Atleta'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1, choices=GENERO_OPCIONES)
    edad = models.IntegerField()
    altura = models.FloatField()  # en cm
    peso = models.FloatField()  # en kg
    nivel_actividad = models.CharField(max_length=20, choices=ACTIVIDAD_OPCIONES)
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_OPCIONES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class PreferenciaAlimenticia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    alimento = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=[
        ('gusta', 'Me gusta'),
        ('no_gusta', 'No me gusta'),
        ('alergia', 'Alergia'),
    ])

class Alimento(models.Model):
    nombre = models.CharField(max_length=100)
    calorias = models.FloatField()
    proteinas = models.FloatField()
    carbohidratos = models.FloatField()
    grasas = models.FloatField()
    categoria = models.CharField(max_length=50)

class PlanNutricional(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calorias_diarias = models.FloatField()
    proteinas_diarias = models.FloatField()
    carbohidratos_diarias = models.FloatField()
    grasas_diarias = models.FloatField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class ComidaPlan(models.Model):
    TIPO_COMIDA = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('snack', 'Snack'),
    ]
    
    plan = models.ForeignKey(PlanNutricional, on_delete=models.CASCADE)
    tipo_comida = models.CharField(max_length=20, choices=TIPO_COMIDA)
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    cantidad = models.FloatField()  # en gramos