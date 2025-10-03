from .models import Alimento
import random

class GeneradorPlanNutricional:
    def __init__(self, macronutrientes):
        self.calorias_objetivo = macronutrientes['calorias']
        self.proteinas_objetivo = macronutrientes['proteinas']
        self.carbohidratos_objetivo = macronutrientes['carbohidratos']
        self.grasas_objetivo = macronutrientes['grasas']
        
    def generar_plan_basico(self):
        """Genera un plan nutricional básico"""
        comidas = ['desayuno', 'almuerzo', 'cena', 'snack']
        
        # Distribuir calorías entre comidas
        distribucion_calorias = {
            'desayuno': 0.25,  # 25%
            'almuerzo': 0.35,  # 35%
            'cena': 0.30,      # 30%
            'snack': 0.10      # 10%
        }
        
        plan = []
        
        for comida in comidas:
            calorias_comida = self.calorias_objetivo * distribucion_calorias[comida]
            alimentos_comida = self._seleccionar_alimentos_para_comida(comida, calorias_comida)
            plan.extend(alimentos_comida)
        
        return plan
    
    def _seleccionar_alimentos_para_comida(self, tipo_comida, calorias_objetivo):
        """Selecciona alimentos apropiados para cada tipo de comida"""
        if tipo_comida == 'desayuno':
            categorias = ['carbohidrato', 'proteina', 'fruta']
        elif tipo_comida == 'almuerzo':
            categorias = ['proteina', 'carbohidrato', 'vegetal', 'grasa']
        elif tipo_comida == 'cena':
            categorias = ['proteina', 'vegetal', 'grasa']
        else:  # snack
            categorias = ['fruta', 'lacteo', 'grasa']
        
        alimentos_seleccionados = []
        calorias_actual = 0
        
        for categoria in categorias:
            if calorias_actual >= calorias_objetivo:
                break
                
            # Obtener alimentos de la categoría
            alimentos_categoria = list(Alimento.objects.filter(categoria=categoria))
            
            if alimentos_categoria:
                # Seleccionar alimento aleatorio
                alimento = random.choice(alimentos_categoria)
                cantidad = self._calcular_cantidad(alimento, calorias_objetivo - calorias_actual)
                
                alimentos_seleccionados.append({
                    'tipo_comida': tipo_comida,
                    'alimento': alimento,
                    'cantidad': cantidad
                })
                
                calorias_actual += (alimento.calorias * cantidad) / 100
        
        return alimentos_seleccionados
    
    def _calcular_cantidad(self, alimento, calorias_disponibles):
        """Calcula la cantidad apropiada del alimento"""
        # Calcular cuántos gramos necesitamos para las calorías disponibles
        gramos = (calorias_disponibles * 100) / alimento.calorias
        
        # Redondear a porciones razonables
        if gramos < 50:
            return 50
        elif gramos > 300:
            return 300
        else:
            return round(gramos / 10) * 10  # Redondear a múltiplos de 10