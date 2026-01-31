from django import forms
from .models import Personagem, Pericia, Arma, Armadura, Cyberware, Equipamento

class PersonagemForm(forms.ModelForm):
    """
    Formulário Principal (WIZARD):
    Coleta Dados Pessoais, Atributos e 4 Perícias Iniciais de uma vez só.
    """
    
    # 1. ATRIBUTOS (Dropdown de 1 a 12)
    # Criamos uma lista [(1,'1'), (2,'2')...] para o select
    OPCOES_VALOR = [(i, str(i)) for i in range(1, 12)]
    
    attr_corpo = forms.ChoiceField(label='Corpo (BOD)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_agilidade = forms.ChoiceField(label='Agilidade (AGI)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_reacao = forms.ChoiceField(label='Reação (REA)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_forca = forms.ChoiceField(label='Força (STR)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    
    attr_vontade = forms.ChoiceField(label='Vontade (WIL)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_logica = forms.ChoiceField(label='Lógica (LOG)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_intuicao = forms.ChoiceField(label='Intuição (INT)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    attr_carisma = forms.ChoiceField(label='Carisma (CHA)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    
    # Especiais
    attr_trunfo = forms.ChoiceField(label='Trunfo (EDG)', choices=OPCOES_VALOR, initial=1, widget=forms.Select(attrs={'class': 'cyber-input'}))
    # Magia começa do 0
    attr_magia = forms.ChoiceField(label='Mágica (MAG)', choices=[(0, '0 (Mundano)')] + OPCOES_VALOR, initial=0, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    # 2. PERÍCIAS INICIAIS (4 Slots para o Wizard)
    # Adicionamos uma opção vazia no começo da lista de perícias
    SKILL_CHOICES = [('', '--- Selecione uma Perícia ---')] + Pericia.OPCOES
    LEVEL_CHOICES = [(0, '---')] + OPCOES_VALOR

    skill_1 = forms.ChoiceField(label='Perícia Primária', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_1 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    skill_2 = forms.ChoiceField(label='Perícia Secundária', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_2 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    skill_3 = forms.ChoiceField(label='Perícia Extra', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_3 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    skill_4 = forms.ChoiceField(label='Perícia Extra', choices=SKILL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))
    skill_val_4 = forms.ChoiceField(label='Nível', choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'cyber-input'}))

    class Meta:
        model = Personagem
        fields = ['nome', 'codinome', 'metatipo', 'arquetipo', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Nome Real'}),
            'codinome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Street Name'}),
            'metatipo': forms.Select(attrs={'class': 'cyber-input'}),
            'arquetipo': forms.Select(attrs={'class': 'cyber-input'}), # Novo campo
        }

# --- FORMULÁRIOS PARA ADICIONAR ITENS NA FICHA (DEPOIS DE CRIADO) ---

class PericiaForm(forms.ModelForm):
    class Meta:
        model = Pericia
        fields = ['nome', 'pontos']
        widgets = {
            'nome': forms.Select(attrs={'class': 'cyber-input'}),
            'pontos': forms.NumberInput(attrs={'class': 'cyber-input'}),
        }

class ArmaForm(forms.ModelForm):
    class Meta:
        model = Arma
        fields = ['nome', 'dano', 'ap', 'pericia_associada']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: Katana'}),
            'dano': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: 4P'}),
            'ap': forms.NumberInput(attrs={'class': 'cyber-input'}),
            'pericia_associada': forms.Select(attrs={'class': 'cyber-input'}),
        }

class ArmaduraForm(forms.ModelForm):
    class Meta:
        model = Armadura
        fields = ['nome', 'valor_defesa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: Colete Blindado'}),
            'valor_defesa': forms.NumberInput(attrs={'class': 'cyber-input'}),
        }

class CyberwareForm(forms.ModelForm):
    class Meta:
        model = Cyberware
        fields = ['nome', 'nivel', 'essencia']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Ex: Olhos Cibernéticos'}),
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