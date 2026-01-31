from django.urls import path
from . import views

urlpatterns = [
    # Rotas Principais
    path('', views.lista_personagens, name='home'),
    path('novo/', views.criar_personagem, name='criar_personagem'),
    path('ficha/<int:pk>/', views.ficha_detalhe, name='ficha_detalhe'),
    
    # Rotas de Adição de Itens (FALTAVAM ESTAS AQUI)
    path('ficha/<int:pk>/add_pericia/', views.adicionar_pericia, name='add_pericia'),
    path('ficha/<int:pk>/add_arma/', views.adicionar_arma, name='add_arma'),
    
    # Novas rotas que corrigem o erro:
    path('ficha/<int:pk>/add_armadura/', views.adicionar_armadura, name='add_armadura'),
    path('ficha/<int:pk>/add_cyber/', views.adicionar_cyber, name='add_cyber'),
    path('ficha/<int:pk>/add_equip/', views.adicionar_equip, name='add_equip'),

    # APIs (Javascript)
    path('api/rolar/<int:pericia_id>/', views.api_rolar_pericia, name='api_rolar'),
    path('api/rolar_atributo/<int:atributo_id>/', views.api_rolar_atributo, name='api_rolar_attr'),
    path('api/iniciativa/<int:pk>/', views.api_rolar_iniciativa, name='api_iniciativa'),
    path('api/dano/<int:pk>/<str:tipo>/<int:valor>/', views.api_atualizar_dano, name='api_dano'),
]