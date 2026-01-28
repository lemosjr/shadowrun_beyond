from django import forms
from .models import Personagem

class PersonagemForm(forms.ModelForm):
    class Meta:
        model = Personagem
        fields = ['nome', 'codinome', 'metatipo', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Nome Real'}),
            'codinome': forms.TextInput(attrs={'class': 'cyber-input', 'placeholder': 'Street Name'}),
            'metatipo': forms.Select(attrs={'class': 'cyber-input'}),
        }