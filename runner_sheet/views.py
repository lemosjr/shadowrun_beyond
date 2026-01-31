from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Personagem, Pericia, Atributo, Arma, Armadura, Cyberware, Equipamento
from .forms import (
    PersonagemForm, PericiaForm, ArmaForm, ArmaduraForm, 
    CyberwareForm, EquipamentoForm
)
import random
import math

# --- VIEW: TELA INICIAL ---
def lista_personagens(request):
    runners = Personagem.objects.all()
    return render(request, 'runner_sheet/home.html', {'runners': runners})

# --- VIEW: CRIAÇÃO DE PERSONAGEM (WIZARD) ---
def criar_personagem(request):
    """
    Processa o Wizard de Criação.
    Salva Identidade, Atributos, Perícias Iniciais e Kit de Equipamento.
    """
    if request.method == 'POST':
        form = PersonagemForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Salva a Identidade Básica e Recursos
            personagem = form.save(commit=False)
            personagem.nuyen = form.cleaned_data['nuyen_inicial']
            personagem.save()
            
            # 2. Processar ATRIBUTOS
            # (O Signal no models.py já criou os objetos com valor 1. Aqui só atualizamos.)
            mapa_attrs = {
                'Corpo': form.cleaned_data['attr_corpo'],
                'Agilidade': form.cleaned_data['attr_agilidade'],
                'Reação': form.cleaned_data['attr_reacao'],
                'Força': form.cleaned_data['attr_forca'],
                'Vontade': form.cleaned_data['attr_vontade'],
                'Lógica': form.cleaned_data['attr_logica'],
                'Intuição': form.cleaned_data['attr_intuicao'],
                'Carisma': form.cleaned_data['attr_carisma'],
                'Trunfo': form.cleaned_data['attr_trunfo'],
                'Mágica': form.cleaned_data['attr_magia'],
            }
            
            for nome_attr, valor in mapa_attrs.items():
                if valor: # Ignora campos vazios
                    try:
                        attr = personagem.atributos.get(nome=nome_attr)
                        attr.valor = int(valor)
                        attr.save()
                    except Atributo.DoesNotExist:
                        pass 

            # 3. Processar PERÍCIAS INICIAIS (Slots 1 a 4 do Wizard)
            for i in range(1, 5):
                nome_skill = form.cleaned_data.get(f'skill_{i}')
                val_skill = form.cleaned_data.get(f'skill_val_{i}')
                
                # Só cria se o usuário selecionou algo E colocou valor > 0
                if nome_skill and val_skill and int(val_skill) > 0:
                    Pericia.objects.create(
                        personagem=personagem,
                        nome=nome_skill,
                        pontos=int(val_skill)
                    )

            # 4. Processar KIT INICIAL (Arma e Armadura)
            
            # Arma Inicial
            arma_nome = form.cleaned_data.get('starter_arma')
            if arma_nome:
                # Valores padrão simplificados para o kit inicial
                dano = "2P" 
                ap = 0
                if "Predator" in arma_nome: dano, ap = "3P", -1
                elif "Katana" in arma_nome: dano, ap = "3P", -3
                elif "AK-97" in arma_nome: dano, ap = "4P", -2
                elif "Taser" in arma_nome: dano, ap = "4S(e)", -5
                
                Arma.objects.create(personagem=personagem, nome=arma_nome, dano=dano, ap=ap)

            # Armadura Inicial
            armor_nome = form.cleaned_data.get('starter_armadura')
            if armor_nome:
                defesa = 2 
                if "Colete" in armor_nome: defesa = 3
                if "Blindada" in armor_nome: defesa = 4
                
                Armadura.objects.create(
                    personagem=personagem, 
                    nome=armor_nome, 
                    valor_defesa=defesa, 
                    equipada=True
                )

            # Finaliza recalculando Vida e Defesa com base no que foi salvo
            personagem.recalcular_stats()
            
            return redirect('ficha_detalhe', pk=personagem.pk)
    else:
        form = PersonagemForm()
    
    return render(request, 'runner_sheet/cadastro.html', {'form': form})

# --- VIEW: FICHA DO PERSONAGEM ---
def ficha_detalhe(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    personagem.recalcular_stats() # Garante que Defesa/Vida estejam certos ao abrir
    
    context = {
        'personagem': personagem,
        # Ranges para os loops de caixinhas de dano no HTML
        'range_fisico': range(1, personagem.max_fisico + 1),
        'range_stun': range(1, personagem.max_stun + 1),
        
        # Instâncias vazias dos formulários para os Modais de Adição
        'form_pericia': PericiaForm(),
        'form_arma': ArmaForm(),
        'form_armadura': ArmaduraForm(),
        'form_cyber': CyberwareForm(),
        'form_equip': EquipamentoForm(),
    }
    return render(request, 'runner_sheet/ficha.html', context)

# --- VIEWS: ADIÇÃO DE ITENS (Chamadas pelos Modais) ---

def adicionar_pericia(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    if request.method == 'POST':
        form = PericiaForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.personagem = personagem
            item.save()
    return redirect('ficha_detalhe', pk=pk)

def adicionar_arma(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    if request.method == 'POST':
        form = ArmaForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.personagem = personagem
            item.save()
    return redirect('ficha_detalhe', pk=pk)

def adicionar_armadura(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    if request.method == 'POST':
        form = ArmaduraForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.personagem = personagem
            item.save()
            # Importante: Recalcular stats pois armadura muda a Defesa Total
            personagem.recalcular_stats()
    return redirect('ficha_detalhe', pk=pk)

def adicionar_cyber(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    if request.method == 'POST':
        form = CyberwareForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.personagem = personagem
            item.save()
    return redirect('ficha_detalhe', pk=pk)

def adicionar_equip(request, pk):
    personagem = get_object_or_404(Personagem, pk=pk)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.personagem = personagem
            item.save()
    return redirect('ficha_detalhe', pk=pk)

# --- APIS (Backend para o Javascript) ---

def api_rolar_pericia(request, pericia_id):
    """Rola dados: (Pontos da Perícia + Atributo Vinculado)"""
    pericia = get_object_or_404(Pericia, id=pericia_id)
    personagem = pericia.personagem
    
    # Tenta achar o valor do atributo base (ex: Agilidade para Armas de Fogo)
    try:
        atributo = personagem.atributos.get(nome=pericia.atributo_base).valor
    except:
        atributo = 0
        
    pool = pericia.pontos + atributo
    
    resultados = [random.randint(1, 6) for _ in range(pool)]
    hits = resultados.count(5) + resultados.count(6)
    glitch = resultados.count(1) > (pool / 2)
    
    return JsonResponse({
        'personagem': personagem.codinome,
        'teste': f"{pericia.nome} + {pericia.atributo_base}",
        'pool_total': pool,
        'resultados': resultados,
        'hits': hits,
        'glitch': glitch,
        'mensagem': f"SUCESSOS: {hits}"
    })

def api_rolar_atributo(request, atributo_id):
    """Rola apenas o atributo puro (ex: Teste de Força para arrombar porta)"""
    attr = get_object_or_404(Atributo, id=atributo_id)
    pool = attr.valor
    
    resultados = [random.randint(1, 6) for _ in range(pool)]
    hits = resultados.count(5) + resultados.count(6)
    glitch = resultados.count(1) > (pool / 2)
    
    return JsonResponse({
        'personagem': attr.personagem.codinome,
        'teste': f"Teste de {attr.nome}",
        'pool_total': pool,
        'resultados': resultados,
        'hits': hits,
        'glitch': glitch,
        'mensagem': f"SUCESSOS: {hits}"
    })

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
        'pool_total': f"{reacao} + {intuicao} + 1d6",
        'resultados': [dado],
        'hits': total, 
        'mensagem': f"VALOR FINAL: {total}",
        'glitch': False
    })

def api_atualizar_dano(request, pk, tipo, valor):
    """Atualiza o Banco de Dados quando o usuário clica nas caixinhas de vida"""
    personagem = get_object_or_404(Personagem, pk=pk)
    
    if tipo == 'fisico':
        personagem.dano_fisico = valor
    elif tipo == 'stun':
        personagem.dano_atordoamento = valor
        
    personagem.save()
    return JsonResponse({'status': 'ok'})