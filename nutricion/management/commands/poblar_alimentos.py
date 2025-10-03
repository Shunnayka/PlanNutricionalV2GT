from django.core.management.base import BaseCommand
from nutricion.models import Alimento

class Command(BaseCommand):
    help = 'Pobla la base de datos con alimentos básicos'

    def handle(self, *args, **options):
        alimentos = [
            # Proteínas
            {'nombre': 'Pechuga de pollo', 'calorias': 165, 'proteinas': 31, 'carbohidratos': 0, 'grasas': 3.6, 'categoria': 'proteina'},
            {'nombre': 'Salmón', 'calorias': 208, 'proteinas': 20, 'carbohidratos': 0, 'grasas': 13, 'categoria': 'proteina'},
            {'nombre': 'Huevos', 'calorias': 155, 'proteinas': 13, 'carbohidratos': 1.1, 'grasas': 11, 'categoria': 'proteina'},
            {'nombre': 'Tofu', 'calorias': 76, 'proteinas': 8, 'carbohidratos': 1.9, 'grasas': 4.8, 'categoria': 'proteina'},
            {'nombre': 'Lentejas', 'calorias': 116, 'proteinas': 9, 'carbohidratos': 20, 'grasas': 0.4, 'categoria': 'proteina'},
            
            # Carbohidratos
            {'nombre': 'Arroz integral', 'calorias': 111, 'proteinas': 2.6, 'carbohidratos': 23, 'grasas': 0.9, 'categoria': 'carbohidrato'},
            {'nombre': 'Avena', 'calorias': 389, 'proteinas': 16.9, 'carbohidratos': 66, 'grasas': 6.9, 'categoria': 'carbohidrato'},
            {'nombre': 'Batata', 'calorias': 86, 'proteinas': 1.6, 'carbohidratos': 20, 'grasas': 0.1, 'categoria': 'carbohidrato'},
            {'nombre': 'Quinoa', 'calorias': 120, 'proteinas': 4.4, 'carbohidratos': 21, 'grasas': 1.9, 'categoria': 'carbohidrato'},
            {'nombre': 'Pan integral', 'calorias': 265, 'proteinas': 13, 'carbohidratos': 49, 'grasas': 3.4, 'categoria': 'carbohidrato'},
            
            # Vegetales
            {'nombre': 'Brócoli', 'calorias': 34, 'proteinas': 2.8, 'carbohidratos': 7, 'grasas': 0.4, 'categoria': 'vegetal'},
            {'nombre': 'Espinacas', 'calorias': 23, 'proteinas': 2.9, 'carbohidratos': 3.6, 'grasas': 0.4, 'categoria': 'vegetal'},
            {'nombre': 'Zanahorias', 'calorias': 41, 'proteinas': 0.9, 'carbohidratos': 10, 'grasas': 0.2, 'categoria': 'vegetal'},
            {'nombre': 'Pimientos', 'calorias': 31, 'proteinas': 1, 'carbohidratos': 6, 'grasas': 0.3, 'categoria': 'vegetal'},
            
            # Frutas
            {'nombre': 'Manzana', 'calorias': 52, 'proteinas': 0.3, 'carbohidratos': 14, 'grasas': 0.2, 'categoria': 'fruta'},
            {'nombre': 'Plátano', 'calorias': 89, 'proteinas': 1.1, 'carbohidratos': 23, 'grasas': 0.3, 'categoria': 'fruta'},
            {'nombre': 'Fresas', 'calorias': 32, 'proteinas': 0.7, 'carbohidratos': 7.7, 'grasas': 0.3, 'categoria': 'fruta'},
            {'nombre': 'Aguacate', 'calorias': 160, 'proteinas': 2, 'carbohidratos': 9, 'grasas': 15, 'categoria': 'grasa'},
            
            # Grasas saludables
            {'nombre': 'Almendras', 'calorias': 579, 'proteinas': 21, 'carbohidratos': 22, 'grasas': 50, 'categoria': 'grasa'},
            {'nombre': 'Aceite de oliva', 'calorias': 884, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 100, 'categoria': 'grasa'},
            {'nombre': 'Nueces', 'calorias': 654, 'proteinas': 15, 'carbohidratos': 14, 'grasas': 65, 'categoria': 'grasa'},
            
            # Lácteos
            {'nombre': 'Yogur griego', 'calorias': 59, 'proteinas': 10, 'carbohidratos': 3.6, 'grasas': 0.4, 'categoria': 'lacteo'},
            {'nombre': 'Queso cottage', 'calorias': 98, 'proteinas': 11, 'carbohidratos': 3.4, 'grasas': 4.3, 'categoria': 'lacteo'},
        ]
        
        for alimento_data in alimentos:
            Alimento.objects.get_or_create(**alimento_data)
        
        self.stdout.write(self.style.SUCCESS('Base de datos poblada con alimentos básicos'))