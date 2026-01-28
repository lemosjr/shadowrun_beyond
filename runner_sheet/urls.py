from django.urls import path
from . import views

# DICA: Se tiver uma linha "app_name = 'runner_sheet'" aqui em cima, APAGUE ELA.
# Ela muda o nome das rotas e causa esse erro.

urlpatterns = [
    # 1. Rota da Home (Raiz) - Essa é a que adicionamos por último
    path('', views.lista_personagens, name='home'),

    # 2. Rota da Ficha - Essa é a que o erro diz que sumiu
    path('ficha/<int:pk>/', views.ficha_detalhe, name='ficha_detalhe'),

    # 3. API de Dados
    path('api/rolar/<int:pericia_id>/', views.api_rolar_pericia, name='api_rolar'),
    
    # 4. API de Dano
    path('api/dano/<int:pk>/<str:tipo>/<int:valor>/', views.api_atualizar_dano, name='api_dano'),
]