from django import forms
from .models import Personagem, Pericia, Arma

class PersonagemForm(forms.ModelForm):
    # Campos extras que não estão direto no Model Personagem, mas vamos usar para criar os Atributos
    val_corpo = forms.IntegerField(label='Corpo (BOD)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    val_agilidade = forms.IntegerField(label='Agilidade (AGI)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    val_reacao = forms.IntegerField(label='Reação (REA)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    val_forca = forms.IntegerField(label='Força (STR)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    val_vontade = forms.IntegerField(label='Vontade (WIL)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    val_logica = forms.IntegerField(label='Lógica (LOG)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    val_intuicao = forms.IntegerField(label='Intuição (INT)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))
    val_carisma = forms.IntegerField(label='Carisma (CHA)', initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'cyber-input'}))

    class Meta:
        model = Personagem
        fields = ['nome', 'codinome', 'metatipo', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Nome Real'}),
            'codinome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Street Name'}),
            'metatipo': forms.Select(attrs={'class': 'cyber-input'}),
        }

# Formulários Simples para adicionar Perícia e Arma depois (na Ficha)
class PericiaForm(forms.ModelForm):
    class Meta:
        model = Pericia
        fields = ['nome', 'atributo_base', 'pontos']
        widgets = {
            'nome': forms.Select(attrs={'class': 'cyber-input'}),
            'atributo_base': forms.Select(attrs={'class': 'cyber-input'}),
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