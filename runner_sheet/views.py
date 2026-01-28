from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Personagem, Pericia, Atributo
from .forms import PersonagemForm
import random

"""
ARQUIVO: views.py
OBJETIVO: Controla a lógica de navegação e as regras do jogo (Rolagens).
"""

# --- [NAVEGAÇÃO] ---

def lista_personagens(request):
    """Tela Inicial: Mostra os cards de todos os runners."""
    runners = Personagem.objects.all()
    return render(request, 'runner_sheet/home.html', {'runners': runners})

def ficha_detalhe(request, pk):
    """Tela da Ficha: Mostra os detalhes de UM personagem específico."""
    personagem = get_object_or_404(Personagem, pk=pk)
    return render(request, 'runner_sheet/ficha.html', {'personagem': personagem})

def criar_personagem(request):
    """Tela de Cadastro: Cria um novo runner e gera seus atributos iniciais."""
    if request.method == 'POST':
        form = PersonagemForm(request.POST, request.FILES)
        if form.is_valid():
            personagem = form.save()
            
            # AUTOMACAO: Cria os 8 atributos básicos automaticamente com valor 1
            # Isso evita que a ficha quebre por falta de atributos.
            atributos_padrao = ['Corpo', 'Agilidade', 'Reação', 'Força', 'Vontade', 'Lógica', 'Intuição', 'Carisma']
            for nome_attr in atributos_padrao:
                Atributo.objects.create(personagem=personagem, nome=nome_attr, valor=1)
            
            return redirect('ficha_detalhe', pk=personagem.pk)
    else:
        form = PersonagemForm()
    
    return render(request, 'runner_sheet/cadastro.html', {'form': form})


# --- [API & REGRAS DO SISTEMA] ---
# Essas funções não retornam HTML, retornam JSON para o JavaScript.

def _rolar_dados_shadowrun(pool_dados):
    """
    Lógica Central de Regras (Shadowrun 5e/6e):
    - Rola N dados de 6 lados (d6).
    - 5 ou 6 = Sucesso (Hit).
    - 1 = Falha (Glitch).
    """
    resultados = [random.randint(1, 6) for _ in range(pool_dados)]
    hits = resultados.count(5) + resultados.count(6)
    uns = resultados.count(1)
    
    # Regra de Glitch (Falha Crítica)
    # Se mais da metade dos dados forem 1, é um Glitch.
    glitch = uns > (pool_dados / 2)
    
    mensagem = "Sucesso"
    if glitch:
        mensagem = "FALHA CRÍTICA" if hits == 0 else "GLITCH (Sucesso com problema)"
    
    return {
        'pool_total': pool_dados,
        'resultados': resultados,
        'hits': hits,
        'glitch': glitch,
        'mensagem': mensagem
    }

def api_rolar_pericia(request, pericia_id):
    """Chamada quando clica no botão 'EXECUTAR' de uma perícia ou arma."""
    pericia = get_object_or_404(Pericia, pk=pericia_id)
    
    # Tenta achar o atributo base (Ex: Agilidade) ligado à perícia
    # Se não achar (erro de digitação no cadastro), assume valor 0 pra não travar
    try:
        atributo = pericia.personagem.atributos.get(nome=pericia.atributo_base)
        valor_atributo = atributo.valor
    except Atributo.DoesNotExist:
        valor_atributo = 0

    # Pool = Atributo + Perícia
    pool = valor_atributo + pericia.pontos
    
    resultado = _rolar_dados_shadowrun(pool)
    
    return JsonResponse({
        'personagem': pericia.personagem.nome,
        'teste': f"Teste de {pericia.nome}",
        **resultado # Desempacota o dicionário de resultados
    })

def api_rolar_atributo(request, atributo_id):
    """Chamada quando clica direto na caixinha do Atributo."""
    attr = get_object_or_404(Atributo, pk=atributo_id)
    
    # Pool = Apenas o valor do atributo
    resultado = _rolar_dados_shadowrun(attr.valor)
    
    return JsonResponse({
        'personagem': attr.personagem.nome,
        'teste': f"Teste de {attr.nome}",
        **resultado
    })

def api_atualizar_dano(request, pk, tipo, valor):
    """Salva o dano (Físico ou Stun) quando clica nos quadradinhos."""
    personagem = get_object_or_404(Personagem, pk=pk)
    
    if tipo == 'fisico':
        personagem.dano_fisico = valor
    elif tipo == 'stun':
        personagem.dano_atordoamento = valor
        
    personagem.save()
    return JsonResponse({'status': 'ok', 'novo_valor': valor})