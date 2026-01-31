from django import forms
from .models import Personagem, Pericia, Arma, Armadura, Cyberware, Equipamento

class PersonagemForm(forms.ModelForm):
    """
    Formulário Principal (WIZARD):
    Gerencia a criação passo-a-passo (Identidade -> Atributos -> Perícias -> Equipamentos).
    """
    
    # --- HELPER: OPÇÕES DE VALORES (1 a 12) ---
    OPCOES_VALOR = [(i, str(i)) for i in range(1, 13)]

    # --- PASSO 2: ATRIBUTOS (Dropdowns) ---
    attr_corpo = forms.ChoiceField(label='Corpo (BOD)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_agilidade = forms.ChoiceField(label='Agilidade (AGI)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_reacao = forms.ChoiceField(label='Reação (REA)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_forca = forms.ChoiceField(label='Força (STR)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    
    attr_vontade = forms.ChoiceField(label='Vontade (WIL)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_logica = forms.ChoiceField(label='Lógica (LOG)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_intuicao = forms.ChoiceField(label='Intuição (INT)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_carisma = forms.ChoiceField(label='Carisma (CHA)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    
    attr_trunfo = forms.ChoiceField(label='Trunfo (EDG)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    # Magia começa do 0 (Mundano)
    attr_magia = forms.ChoiceField(label='Mágica (MAG)', choices=[(0, '0 (Mundano)')] + OPCOES_VALOR, initial=0, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    # --- PASSO 3: PERÍCIAS INICIAIS (4 Slots) ---
    SKILL_CHOICES = [('', '--- Selecione uma Perícia ---')] + Pericia.OPCOES
    LEVEL_CHOICES = [(0, '---')] + OPCOES_VALOR

    skill_1 = forms.ChoiceField(label='Perícia 1', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_1 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    skill_2 = forms.ChoiceField(label='Perícia 2', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_2 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    skill_3 = forms.ChoiceField(label='Perícia 3', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_3 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    skill_4 = forms.ChoiceField(label='Perícia 4', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_4 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    # --- PASSO 4: RECURSOS & EQUIPAMENTO ---
    
    # Listas de Kits Iniciais
    OPCOES_ARMA_INICIAL = [
        ('', '--- Sem Arma Inicial ---'),
        ('Ares Predator VI', 'Pistola Pesada: Ares Predator VI (Dano: 3P)'),
        ('Colt America L36', 'Pistola Leve: Colt America L36 (Dano: 2P)'),
        ('AK-97', 'Fuzil de Assalto: AK-97 (Dano: 4P)'),
        ('Katana', 'Lâmina: Katana (Dano: 3P)'),
        ('Faca de Combate', 'Lâmina: Faca de Combate (Dano: 2P)'),
        ('Taser Yamaha Pulsar', 'Taser: Yamaha Pulsar (Dano: 4S Stun)'),
    ]
    
    OPCOES_ARMADURA_INICIAL = [
        ('', '--- Sem Armadura ---'),
        ('Jaqueta de Couro Sintético', 'Jaqueta de Couro (+2 Defesa)'),
        ('Colete Blindado', 'Colete Blindado (+3 Defesa)'),
        ('Jaqueta Blindada', 'Jaqueta Blindada (+4 Defesa)'),
        ('Traje Camaleão', 'Traje Camaleão (+2 Defesa, Furtividade)'),
    ]

    estilo_vida = forms.ChoiceField(label='Estilo de Vida', choices=Personagem.ESTILOS_VIDA, initial='BAI', widget=forms.Select(attrs={'class': 'cyber-input'}))
    nuyen_inicial = forms.IntegerField(label='Nuyen Inicial (¥)', initial=5000, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    
    starter_arma = forms.ChoiceField(label='Arma Principal', choices=OPCOES_ARMA_INICIAL, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    starter_armadura = forms.ChoiceField(label='Traje / Proteção', choices=OPCOES_ARMADURA_INICIAL, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    class Meta:
        model = Personagem
        fields = ['nome', 'codinome', 'metatipo', 'arquetipo', 'foto', 'estilo_vida']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Nome Real'}),
            'codinome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Apelido nas Sombras (Street Name)'}),
            'metatipo': forms.Select(attrs={'class': 'cyber-input'}),
            'arquetipo': forms.Select(attrs={'class': 'cyber-input'}),
            'estilo_vida': forms.Select(attrs={'class': 'cyber-input'}),
        }


# --- FORMULÁRIOS SECUNDÁRIOS (Para usar dentro da Ficha) ---

class PericiaForm(forms.ModelForm):
    class Meta:
        model = Pericia
        fields = ['nome', 'pontos']
        widgets = {
            'nome': forms.Select(attrs={'class': 'cyber-input'}),
            'pontos': forms.NumberInput(attrs={'class': 'cyber-input', 'min': 1, 'max': 12}),
        }

class ArmaForm(forms.ModelForm):
    class Meta:
        model = Arma
        fields = ['nome', 'dano', 'ap', 'pericia_associada']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: Ares Predator'}),
            'dano': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: 3P'}),
            'ap': forms.NumberInput(attrs={'class': 'cyber-input'}),
            'pericia_associada': forms.Select(attrs={'class': 'cyber-input'}),
        }

class ArmaduraForm(forms.ModelForm):
    class Meta:
        model = Armadura
        fields = ['nome', 'valor_defesa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: Colete à prova de balas'}),
            'valor_defesa': forms.NumberInput(attrs={'class': 'cyber-input'}),
        }

class CyberwareForm(forms.ModelForm):
    class Meta:
        model = Cyberware
        fields = ['nome', 'nivel', 'essencia']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: Braço Cibernético'}),
            'nivel': forms.NumberInput(attrs={'class': 'cyber-input'}),
            'essencia': forms.NumberInput(attrs={'class': 'cyber-input', 'step': '0.1'}),
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'qtd']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: Medkit'}),
            'qtd': forms.NumberInput(attrs={'class': 'cyber-input'}),
        }