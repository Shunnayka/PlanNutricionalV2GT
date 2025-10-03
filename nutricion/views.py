from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import json
from .models import PerfilUsuario, PreferenciaAlimenticia, Alimento, PlanNutricional, ComidaPlan
from .sustitucion import SustitutorAlimentos
from .generador_planes import GeneradorPlanNutricional

def index(request):
    return render(request, 'nutricion/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Autenticar al usuario automáticamente después del registro
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('perfil')
    else:
        form = UserCreationForm()
    
    return render(request, 'nutricion/register.html', {'form': form})

@login_required
def perfil_usuario(request):
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    if request.method == 'POST':
        # Actualizar o crear perfil
        if perfil:
            perfil.genero = request.POST.get('genero')
            perfil.edad = request.POST.get('edad')
            perfil.altura = request.POST.get('altura')
            perfil.peso = request.POST.get('peso')
            perfil.nivel_actividad = request.POST.get('nivel_actividad')
            perfil.objetivo = request.POST.get('objetivo')
            perfil.save()
        else:
            perfil = PerfilUsuario.objects.create(
                usuario=request.user,
                genero=request.POST.get('genero'),
                edad=request.POST.get('edad'),
                altura=request.POST.get('altura'),
                peso=request.POST.get('peso'),
                nivel_actividad=request.POST.get('nivel_actividad'),
                objetivo=request.POST.get('objetivo')
            )
        
        # Procesar preferencias alimenticias
        PreferenciaAlimenticia.objects.filter(usuario=request.user).delete()
        
        # Alimentos que le gustan
        gusta = request.POST.get('gusta', '').split(',')
        for alimento in gusta:
            if alimento.strip():
                PreferenciaAlimenticia.objects.create(
                    usuario=request.user,
                    alimento=alimento.strip(),
                    tipo='gusta'
                )
        
        # Alimentos que NO le gustan
        no_gusta = request.POST.get('no_gusta', '').split(',')
        for alimento in no_gusta:
            if alimento.strip():
                PreferenciaAlimenticia.objects.create(
                    usuario=request.user,
                    alimento=alimento.strip(),
                    tipo='no_gusta'
                )
        
        # Alergias
        alergias = request.POST.get('alergias', '').split(',')
        for alimento in alergias:
            if alimento.strip():
                PreferenciaAlimenticia.objects.create(
                    usuario=request.user,
                    alimento=alimento.strip(),
                    tipo='alergia'
                )
        
        return redirect('generar_plan')
    
    return render(request, 'nutricion/perfil.html', {'perfil': perfil})

@login_required
def generar_plan(request):
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
    except PerfilUsuario.DoesNotExist:
        return redirect('perfil')
    
    # Calcular macronutrientes
    macronutrientes = perfil.calcular_macronutrientes()
    
    if request.method == 'POST':
        # Generar plan nutricional
        generador = GeneradorPlanNutricional(macronutrientes)
        plan_base = generador.generar_plan_basico()
        
        # Aplicar sustituciones según preferencias
        sustitutor = SustitutorAlimentos(request.user)
        plan_ajustado = sustitutor.sustituir_en_plan(plan_base)
        
        # Guardar plan en la base de datos
        plan_nutricional = PlanNutricional.objects.create(
            usuario=request.user,
            calorias_diarias=macronutrientes['calorias'],
            proteinas_diarias=macronutrientes['proteinas'],
            carbohidratos_diarias=macronutrientes['carbohidratos'],
            grasas_diarias=macronutrientes['grasas']
        )
        
        for comida in plan_ajustado:
            ComidaPlan.objects.create(
                plan=plan_nutricional,
                tipo_comida=comida['tipo_comida'],
                alimento=comida['alimento'],
                cantidad=comida['cantidad']
            )
        
        return render(request, 'nutricion/plan_resultado.html', {
            'plan': plan_ajustado,
            'macronutrientes': macronutrientes,
            'perfil': perfil
        })
    
    return render(request, 'nutricion/generar_plan.html', {
        'macronutrientes': macronutrientes,
        'perfil': perfil
    })

def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pregunta = data.get('pregunta', '')
        
        respuesta = procesar_pregunta(pregunta, request.user)
        
        return JsonResponse({'respuesta': respuesta})
    
    return JsonResponse({'error': 'Método no permitido'})

def procesar_pregunta(pregunta, usuario):
    pregunta = pregunta.lower()
    
    # Respuestas contextuales basadas en el usuario
    try:
        perfil = PerfilUsuario.objects.get(usuario=usuario)
        if perfil:
            if 'calorías' in pregunta or 'calorias' in pregunta:
                calorias = perfil.calcular_calorias_diarias()
                return f"Según tu perfil, tu consumo diario recomendado es de {calorias} calorías."
            
            if 'proteína' in pregunta or 'proteina' in pregunta:
                macros = perfil.calcular_macronutrientes()
                return f"Necesitas aproximadamente {macros['proteinas']}g de proteína diarios."
    except:
        pass
    
    # Respuestas generales
    preguntas_frecuentes = {
        'snack': 'Te recomiendo frutas frescas, yogur griego, frutos secos, hummus con vegetales o un puñado de almendras como snacks saludables.',
        'proteína': 'Buenas fuentes de proteína son: pollo, pescado, huevos, legumbres, tofu, tempeh, quinoa y lácteos.',
        'carbohidratos': 'Opta por carbohidratos complejos como: avena, quinoa, batata, arroz integral, pasta integral y legumbres.',
        'grasas': 'Las grasas saludables las encuentras en: aguacate, nueces, almendras, aceite de oliva, pescados azules y semillas.',
        'desayuno': 'Un buen desayuno podría incluir: avena con frutas, huevos con pan integral, o yogur griego con granola y frutos rojos.',
        'vegetales': 'Incluye variedad de vegetales: espinacas, brócoli, zanahorias, pimientos, y vegetales de hojas verdes.',
    }
    
    for clave, respuesta in preguntas_frecuentes.items():
        if clave in pregunta:
            return respuesta
    
    return 'Puedo ayudarte con sugerencias sobre nutrición, planes alimenticios, snacks saludables y más. ¿En qué específicamente puedo asistirte?'