from django.db import models
from django.contrib.auth.models import User
import math

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
        ('ligero', 'Ejercicio ligero (1-2 días/semana)'),
        ('moderado', 'Ejercicio moderado (3-5 días/semana)'),
        ('intenso', 'Ejercicio intenso (6-7 días/semana)'),
        ('atleta', 'Atleta (2 veces al día)'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1, choices=GENERO_OPCIONES)
    edad = models.IntegerField()
    altura = models.FloatField()  # en cm
    peso = models.FloatField()  # en kg
    nivel_actividad = models.CharField(max_length=20, choices=ACTIVIDAD_OPCIONES)
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_OPCIONES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def calcular_calorias_diarias(self):
        """Calcula las calorías diarias usando la fórmula de Mifflin-St Jeor"""
        if self.genero == 'M':
            tmb = 10 * self.peso + 6.25 * self.altura - 5 * self.edad + 5
        else:
            tmb = 10 * self.peso + 6.25 * self.altura - 5 * self.edad - 161
        
        factores_actividad = {
            'sedentario': 1.2,
            'ligero': 1.375,
            'moderado': 1.55,
            'intenso': 1.725,
            'atleta': 1.9
        }
        
        calorias = tmb * factores_actividad[self.nivel_actividad]
        
        # Ajustar según objetivo
        if self.objetivo == 'perder':
            calorias -= 500
        elif self.objetivo == 'ganar':
            calorias += 500
            
        return round(calorias)
    
    def calcular_macronutrientes(self):
        """Calcula la distribución de macronutrientes"""
        calorias = self.calcular_calorias_diarias()
        
        if self.objetivo == 'ganar':
            # Más proteínas para ganar masa muscular
            proteinas_cal = calorias * 0.30  # 30%
            carbos_cal = calorias * 0.45     # 45%
            grasas_cal = calorias * 0.25     # 25%
        elif self.objetivo == 'perder':
            # Más proteínas para saciedad y preservar músculo
            proteinas_cal = calorias * 0.35  # 35%
            carbos_cal = calorias * 0.40     # 40%
            grasas_cal = calorias * 0.25     # 25%
        else:  # mantener
            proteinas_cal = calorias * 0.25  # 25%
            carbos_cal = calorias * 0.50     # 50%
            grasas_cal = calorias * 0.25     # 25%
        
        # Convertir calorías a gramos
        proteinas_gramos = proteinas_cal / 4
        carbos_gramos = carbos_cal / 4
        grasas_gramos = grasas_cal / 9
        
        return {
            'calorias': calorias,
            'proteinas': round(proteinas_gramos),
            'carbohidratos': round(carbos_gramos),
            'grasas': round(grasas_gramos)
        }

class PreferenciaAlimenticia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    alimento = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=[
        ('gusta', 'Me gusta'),
        ('no_gusta', 'No me gusta'),
        ('alergia', 'Alergia'),
    ])

class Alimento(models.Model):
    CATEGORIAS = [
        ('proteina', 'Proteína'),
        ('carbohidrato', 'Carbohidrato'),
        ('grasa', 'Grasa Saludable'),
        ('vegetal', 'Vegetal'),
        ('fruta', 'Fruta'),
        ('lacteo', 'Lácteo'),
    ]
    
    nombre = models.CharField(max_length=100)
    calorias = models.FloatField()  # por 100g
    proteinas = models.FloatField()  # por 100g
    carbohidratos = models.FloatField()  # por 100g
    grasas = models.FloatField()  # por 100g
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

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
    
    @property
    def calorias_totales(self):
        return (self.alimento.calorias * self.cantidad) / 100
    
    @property
    def proteinas_totales(self):
        return (self.alimento.proteinas * self.cantidad) / 100
    
    @property
    def carbohidratos_totales(self):
        return (self.alimento.carbohidratos * self.cantidad) / 100
    
    @property
    def grasas_totales(self):
        return (self.alimento.grasas * self.cantidad) / 100