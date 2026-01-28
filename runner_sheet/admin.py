from django.contrib import admin
from .models import Personagem, Atributo, Pericia, Arma

# --- CONFIGURAÇÃO DE EDITORES "EMBUTIDOS" (INLINES) ---
# Essas classes permitem editar Atributos, Armas e Perícias 
# DENTRO da tela do Personagem, sem precisar ficar trocando de aba.

class AtributoInline(admin.TabularInline):
    model = Atributo
    # Abre 8 linhas vazias automaticamente (Para: BOD, AGI, REA, STR, CHA, INT, LOG, WIL)
    extra = 8 

class ArmaInline(admin.TabularInline):
    model = Arma
    extra = 1 # Abre 1 linha para arma (clique em "Adicionar" para mais)

class PericiaInline(admin.TabularInline):
    model = Pericia
    extra = 1

# --- CONFIGURAÇÃO DA TELA PRINCIPAL DE PERSONAGENS ---

@admin.register(Personagem)
class PersonagemAdmin(admin.ModelAdmin):
    # O que aparece na lista geral (Colunas da tabela)
    list_display = ('codinome', 'nome', 'metatipo')
    
    # Permite clicar tanto no Codinome quanto no Nome Real para editar
    list_display_links = ('codinome', 'nome')
    
    # Cria um filtro lateral (Útil para achar só os "Humanos" ou "Elfos" rapidamente)
    list_filter = ('metatipo',)
    
    # Barra de pesquisa (Busca por nome ou codinome)
    search_fields = ('nome', 'codinome')

    # Conecta os editores embutidos criados acima
    inlines = [AtributoInline, PericiaInline, ArmaInline]

# Registro avulso (Opcional, caso precisem editar uma Perícia isolada fora da ficha)
admin.site.register(Pericia)
# admin.site.register(Arma) # Descomente se quiser que Armas apareçam no menu principal