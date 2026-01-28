import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Personagem, Pericia

# --- LÓGICA PURA (HELPER) ---
# Esta função não é uma "view", é apenas uma calculadora interna
def _rolar_dados_shadowrun(pool):
    """
    Rola 'pool' dados d6.
    Retorna:
    - hits: Quantidade de 5s e 6s
    - dados: Lista com os resultados individuais (ex: [1, 5, 6, 2])
    - glitch: Booleano (se mais da metade for 1)
    """
    if pool < 1:
        pool = 0
        
    resultados = [random.randint(1, 6) for _ in range(pool)]
    
    hits = 0
    uns = 0
    
    for dado in resultados:
        if dado >= 5:
            hits += 1
        if dado == 1:
            uns += 1
            
    # Regra de Glitch (Falha): Mais da metade dos dados são 1
    # Se pool for 0, não tem como ter glitch matemático normal, tratamos à parte
    glitch = False
    if pool > 0:
        glitch = uns > (pool / 2)
    
    mensagem = 'Sucesso'
    if hits == 0 and glitch:
        mensagem = 'FALHA CRÍTICA!'
    elif glitch:
        mensagem = 'GLITCH!'
    elif hits == 0:
        mensagem = 'Falha'

    return {
        'pool_total': pool,
        'resultados': resultados,
        'hits': hits,
        'glitch': glitch,
        'mensagem': mensagem
    }

# --- VIEWS (INTERFACE) ---

def ficha_detalhe(request, pk):
    """Renderiza a ficha do personagem (HTML)"""
    personagem = get_object_or_404(Personagem, pk=pk)
    
    # ATENÇÃO: Dependendo de onde você salvou o HTML, use uma das linhas abaixo:
    
    # Opção A: Se o arquivo está em runner_sheet/templates/runner_sheet/ficha.html (Padrão Django)
    return render(request, 'runner_sheet/ficha.html', {'personagem': personagem})
    
    # Opção B: Se o arquivo está solto em runner_sheet/templates/ficha.html (Padrão Rápido)
    # return render(request, 'ficha.html', {'personagem': personagem})

def api_rolar_pericia(request, pericia_id):
    """
    API que o Frontend vai chamar via JavaScript (AJAX).
    Retorna JSON puro, sem HTML.
    """
    pericia = get_object_or_404(Pericia, pk=pericia_id)
    
    # 1. Calcula a pool (Atributo + Pericia)
    # Certifique-se que seu model Pericia tem o método get_dice_pool()
    dice_pool = pericia.get_dice_pool()
    
    # 2. Rola os dados
    resultado = _rolar_dados_shadowrun(dice_pool)
    
    # 3. Monta a resposta para o Javascript
    response_data = {
        'personagem': pericia.personagem.nome,
        'teste': f"{pericia.nome} ({pericia.atributo_base})",
        **resultado # Desempacota hits, dados, glitch, etc.
    }
    
    return JsonResponse(response_data)

# Adicione essa função nova no final do views.py
def api_atualizar_dano(request, pk, tipo, valor):
    """
    Atualiza o dano Físico ('fisico') ou Atordoamento ('stun').
    Exemplo de uso: /runner/api/dano/1/fisico/3/ (Define 3 de dano físico)
    """
    personagem = get_object_or_404(Personagem, pk=pk)
    
    if tipo == 'fisico':
        personagem.dano_fisico = valor
    elif tipo == 'stun':
        personagem.dano_atordoamento = valor
        
    personagem.save()
    
    return JsonResponse({'status': 'ok', 'novo_valor': valor})

def lista_personagens(request):
    """Tela inicial que lista todos os runners disponíveis"""
    runners = Personagem.objects.all()
    return render(request, 'runner_sheet/home.html', {'runners': runners})