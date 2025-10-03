from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PerfilUsuario, PreferenciaAlimenticia, Alimento, PlanNutricional
import json

def index(request):
    return render(request, 'nutricion/index.html')

def perfil_usuario(request):
    if request.method == 'POST':
        # Procesar datos del formulario
        pass
    return render(request, 'nutricion/perfil.html')

def generar_plan(request):
    if request.method == 'POST':
        # Lógica para generar el plan nutricional
        pass
    return render(request, 'nutricion/plan.html')

def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pregunta = data.get('pregunta', '')
        
        # Lógica simple del chatbot
        respuesta = procesar_pregunta(pregunta)
        
        return JsonResponse({'respuesta': respuesta})
    
    return JsonResponse({'error': 'Método no permitido'})

def procesar_pregunta(pregunta):
    # Lógica básica del chatbot
    preguntas_frecuentes = {
        'snack': 'Te recomiendo frutas, yogur griego o frutos secos como snacks saludables.',
        'proteína': 'Buenas fuentes de proteína son pollo, pescado, huevos, legumbres y tofu.',
        'carbohidratos': 'Opta por carbohidratos complejos como avena, quinoa, batata y arroz integral.',
        'grasas': 'Las grasas saludables las encuentras en aguacate, nueces, aceite de oliva y pescados azules.',
    }
    
    pregunta = pregunta.lower()
    for clave, respuesta in preguntas_frecuentes.items():
        if clave in pregunta:
            return respuesta
    
    return 'Puedo ayudarte con sugerencias sobre snacks, proteínas, carbohidratos y grasas saludables. ¿En qué más puedo asistirte?'