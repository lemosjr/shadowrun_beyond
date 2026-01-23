from django.contrib import admin
from .models import Personagem, Atributo, Pericia

# Isso cria uma interface onde você edita Atributos DENTRO da tela do Personagem
class AtributoInline(admin.TabularInline):
    model = Atributo
    extra = 8 # Já abre 8 espaços para preencher os atributos básicos

class PericiaInline(admin.TabularInline):
    model = Pericia
    extra = 1

@admin.register(Personagem)
class PersonagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codinome', 'metatipo')
    inlines = [AtributoInline, PericiaInline] # Coloca tudo na mesma página

# Se quiser registrar solto também pode, mas o Inline acima é melhor
admin.site.register(Pericia)