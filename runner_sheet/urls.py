from django.urls import path
from . import views

app_name = 'runner'

urlpatterns = [
    # Ex: /runner/ficha/1/
    path('ficha/<int:pk>/', views.ficha_detalhe, name='ficha_detalhe'),
    
    # Ex: /runner/api/rolar/5/ (Onde 5 é o ID da perícia)
    path('api/rolar/<int:pericia_id>/', views.api_rolar_pericia, name='api_rolar'),

    path('api/dano/<int:pk>/<str:tipo>/<int:valor>/', views.api_atualizar_dano, name='api_dano'),
]