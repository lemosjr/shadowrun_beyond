from django.urls import path
from . import views

"""
ARQUIVO: urls.py (do app runner_sheet)
OBJETIVO: Define os endereços específicos deste aplicativo.
"""

urlpatterns = [
    # --- [TELAS VISUAIS (HTML)] ---
    
    # Home (Lista de Cards) - Acessada via {% url 'home' %}
    path('', views.lista_personagens, name='home'),
    
    # Tela de Criação - Acessada via {% url 'criar_personagem' %}
    path('novo/', views.criar_personagem, name='criar_personagem'),
    
    # Ficha Completa - Acessada via {% url 'ficha_detalhe' id %}
    path('ficha/<int:pk>/', views.ficha_detalhe, name='ficha_detalhe'),

    # --- [API (JavaScript / Fetch)] ---
    # Essas rotas não abrem páginas, elas retornam dados JSON.
    
    # Rolar Perícia/Arma
    path('api/rolar/<int:pericia_id>/', views.api_rolar_pericia, name='api_rolar'),
    
    # Rolar Atributo Puro
    path('api/rolar_atributo/<int:atributo_id>/', views.api_rolar_atributo, name='api_rolar_attr'),
    
    # Salvar Dano (Vida)
    path('api/dano/<int:pk>/<str:tipo>/<int:valor>/', views.api_atualizar_dano, name='api_dano'),
]