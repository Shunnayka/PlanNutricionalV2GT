from .models import Alimento, PreferenciaAlimenticia
import math

class SustitutorAlimentos:
    def __init__(self, usuario):
        self.usuario = usuario
        self.alimentos_no_gustan = self._obtener_alimentos_no_gustan()
        self.alimentos_alergias = self._obtener_alimentos_alergias()
    
    def _obtener_alimentos_no_gustan(self):
        """Obtiene lista de alimentos que no le gustan al usuario"""
        return list(PreferenciaAlimenticia.objects.filter(
            usuario=self.usuario, 
            tipo='no_gusta'
        ).values_list('alimento', flat=True))
    
    def _obtener_alimentos_alergias(self):
        """Obtiene lista de alimentos con alergias del usuario"""
        return list(PreferenciaAlimenticia.objects.filter(
            usuario=self.usuario, 
            tipo='alergia'
        ).values_list('alimento', flat=True))
    
    def calcular_similitud_nutricional(self, alimento1, alimento2):
        """Calcula la similitud nutricional entre dos alimentos usando distancia euclidiana"""
        # Vector nutricional: [calorias, proteinas, carbohidratos, grasas]
        vec1 = [alimento1.calorias, alimento1.proteinas, alimento1.carbohidratos, alimento1.grasas]
        vec2 = [alimento2.calorias, alimento2.proteinas, alimento2.carbohidratos, alimento2.grasas]
        
        # Calcular distancia euclidiana
        distancia = math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
        
        # Convertir a similitud (menor distancia = mayor similitud)
        similitud = 1 / (1 + distancia)
        return similitud
    
    def es_sustituto_valido(self, alimento_candidato, alimento_original):
        """Verifica si un alimento es un sustituto válido"""
        # Verificar que no esté en la lista de no gusta o alergias
        if (alimento_candidato.nombre.lower() in [a.lower() for a in self.alimentos_no_gustan] or
            alimento_candidato.nombre.lower() in [a.lower() for a in self.alimentos_alergias]):
            return False
        
        # Verificar similitud nutricional (misma categoría y valores similares)
        if alimento_candidato.categoria != alimento_original.categoria:
            return False
        
        # Verificar que las calorías estén dentro del ±10%
        calorias_original = alimento_original.calorias
        calorias_candidato = alimento_candidato.calorias
        margen_calorias = 0.1  # 10%
        
        if abs(calorias_candidato - calorias_original) / calorias_original > margen_calorias:
            return False
        
        return True
    
    def encontrar_sustitutos(self, alimento_original, max_sustitutos=3):
        """Encuentra sustitutos válidos para un alimento"""
        # Obtener todos los alimentos de la misma categoría
        candidatos = Alimento.objects.filter(categoria=alimento_original.categoria).exclude(
            nombre=alimento_original.nombre
        )
        
        sustitutos = []
        for candidato in candidatos:
            if self.es_sustituto_valido(candidato, alimento_original):
                similitud = self.calcular_similitud_nutricional(alimento_original, candidato)
                sustitutos.append((candidato, similitud))
        
        # Ordenar por similitud (mayor primero) y tomar los mejores
        sustitutos.sort(key=lambda x: x[1], reverse=True)
        return [sust[0] for sust in sustitutos[:max_sustitutos]]
    
    def sustituir_en_plan(self, plan_alimentos):
        """Sustituye alimentos no deseados en un plan"""
        plan_ajustado = []
        
        for comida in plan_alimentos:
            alimento = comida['alimento']
            cantidad = comida['cantidad']
            
            # Verificar si el alimento es aceptable
            if (alimento.nombre.lower() not in [a.lower() for a in self.alimentos_no_gustan] and
                alimento.nombre.lower() not in [a.lower() for a in self.alimentos_alergias]):
                plan_ajustado.append(comida)
            else:
                # Encontrar sustituto
                sustitutos = self.encontrar_sustitutos(alimento)
                if sustitutos:
                    sustituto = sustitutos[0]  # Tomar el mejor sustituto
                    plan_ajustado.append({
                        'alimento': sustituto,
                        'cantidad': cantidad,
                        'sustituto_de': alimento.nombre
                    })
                else:
                    # Si no hay sustituto, mantener el alimento pero marcar como conflicto
                    plan_ajustado.append({
                        'alimento': alimento,
                        'cantidad': cantidad,
                        'conflicto': True
                    })
        
        return plan_ajustado