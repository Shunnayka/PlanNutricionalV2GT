from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('generar-plan/', views.generar_plan, name='generar_plan'),
    path('chatbot/', views.chatbot, name='chatbot'),
]