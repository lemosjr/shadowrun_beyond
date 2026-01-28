from django import forms
from .models import Personagem

"""
ARQUIVO: forms.py
OBJETIVO: Define como o formulário de criação de personagem é gerado no HTML.
NOTA PARA FRONTEND:
    - Usamos 'widgets' para adicionar classes CSS (ex: 'cyber-input') nos campos.
    - Isso garante que o input já nasça com o estilo Cyberpunk.
"""

class PersonagemForm(forms.ModelForm):
    class Meta:
        model = Personagem
        # Campos que o usuário pode preencher
        fields = ['nome', 'codinome', 'metatipo', 'foto']
        
        # Aqui injetamos o CSS e Placeholders
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'cyber-input', 
                'placeholder': 'Nome Real (Ex: John Doe)'
            }),
            'codinome': forms.TextInput(attrs={
                'class': 'cyber-input', 
                'placeholder': 'Street Name (Ex: Razor)'
            }),
            'metatipo': forms.Select(attrs={
                'class': 'cyber-input'
            }),
            # O campo de foto usa o estilo padrão do navegador por enquanto
        }