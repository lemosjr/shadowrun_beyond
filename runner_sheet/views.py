from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Personagem, Pericia, Atributo
from .forms import PersonagemForm, PericiaForm, ArmaForm
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

def criar_personagem(request):
    """Cria personagem e define atributos iniciais + cálculo de vida"""
    if request.method == 'POST':
        form = PersonagemForm(request.POST, request.FILES)
        if form.is_valid():
            personagem = form.save()
            
            # ATUALIZA OS ATRIBUTOS COM O QUE O USUÁRIO DIGITOU
            # O Signal já criou os atributos com valor 1, agora vamos atualizar.
            mapa_campos = {
                'Corpo': form.cleaned_data['val_corpo'],
                'Agilidade': form.cleaned_data['val_agilidade'],
                'Reação': form.cleaned_data['val_reacao'],
                'Força': form.cleaned_data['val_forca'],
                'Vontade': form.cleaned_data['val_vontade'],
                'Lógica': form.cleaned_data['val_logica'],
                'Intuição': form.cleaned_data['val_intuicao'],
                'Carisma': form.cleaned_data['val_carisma'],
            }
            
            for nome_attr, valor in mapa_campos.items():
                attr = personagem.atributos.get(nome=nome_attr)
                attr.valor = valor
                attr.save()
            
            # CÁLCULO AUTOMÁTICO DE VIDA (FISICO E STUN)
            personagem.recalcular_monitores()
            
            return redirect('ficha_detalhe', pk=personagem.pk)
    else:
        form = PersonagemForm()
    
    return render(request, 'runner_sheet/cadastro.html', {'form': form})

def ficha_detalhe(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    
    # Forms para os modais de adicionar coisas
    form_pericia = PericiaForm()
    form_arma = ArmaForm()
    
    # Precisamos gerar um range numérico no Python para o Template usar no Loop de Vida
    range_fisico = range(1, personagem.max_fisico + 1)
    range_stun = range(1, personagem.max_stun + 1)
    
    return render(request, 'runner_sheet/ficha.html', {
        'personagem': personagem,
        'range_fisico': range_fisico,
        'range_stun': range_stun,
        'form_pericia': form_pericia,
        'form_arma': form_arma
    })

# --- NOVAS VIEWS PARA ADICIONAR ITENS ---

def adicionar_pericia(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    if request.method == 'POST':
        form = PericiaForm(request.POST)
        if form.is_valid():
            pericia = form.save(commit=False)
            pericia.personagem = personagem
            pericia.save()
    return redirect('ficha_detalhe', pk=pk)

def adicionar_arma(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    if request.method == 'POST':
        form = ArmaForm(request.POST)
        if form.is_valid():
            arma = form.save(commit=False)
            arma.personagem = personagem
            arma.save()
    return redirect('ficha_detalhe', pk=pk)


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


def api_rolar_iniciativa(request, pk):
    """Calcula Iniciativa: (Reação + Intuição) + 1d6"""
    personagem = get_object_or_404(Personagem, pk=pk)
    
    try:
        reacao = personagem.atributos.get(nome='Reação').valor
        intuicao = personagem.atributos.get(nome='Intuição').valor
    except:
        reacao = 0
        intuicao = 0
    
    dado = random.randint(1, 6)
    total = reacao + intuicao + dado
    
    return JsonResponse({
        'personagem': personagem.codinome,
        'teste': 'Iniciativa',
        'pool_total': f"{reacao} + {intuicao} + 1d6", # Apenas informativo
        'resultados': [dado],
        'hits': total, # Na iniciativa, "Hits" é o valor total
        'mensagem': f"VALOR FINAL: {total}",
        'glitch': False
    })