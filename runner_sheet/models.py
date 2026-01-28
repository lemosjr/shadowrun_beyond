from django.db import models

"""
ARQUIVO: models.py
OBJETIVO: Define a estrutura do Banco de Dados.
NOTA PARA FRONTEND:
    - Aqui estão os nomes dos campos que vocês usarão no HTML.
    - Ex: Se aqui tem 'codinome', no HTML vocês usam {{ personagem.codinome }}.
"""

class Personagem(models.Model):
    # Opções de Metatipo (Dropdown no Admin)
    METATIPOS = [
        ('HUM', 'Humano'),
        ('ELF', 'Elfo'),
        ('ORK', 'Ork'),
        ('DWF', 'Anão'),
        ('TRL', 'Troll'),
    ]

    nome = models.CharField(max_length=100)
    codinome = models.CharField(max_length=100)
    metatipo = models.CharField(max_length=3, choices=METATIPOS, default='HUM')
    
    # [IMAGEM]
    # upload_to='runners_avatars/' -> As fotos vão para a pasta /media/runners_avatars/
    # No HTML: <img src="{{ personagem.foto.url }}">
    foto = models.ImageField(upload_to='runners_avatars/', blank=True, null=True)

    # Monitores de Dano (Guardam quantos quadradinhos estão pintados)
    dano_fisico = models.IntegerField(default=0)
    dano_atordoamento = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.codinome} ({self.metatipo})"


class Atributo(models.Model):
    # related_name='atributos' permite usar: {% for attr in personagem.atributos.all %}
    personagem = models.ForeignKey(Personagem, related_name='atributos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=50) # Ex: Agilidade, Força
    valor = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.nome}: {self.valor}"


class Pericia(models.Model):
    # related_name='pericias' permite usar: {% for p in personagem.pericias.all %}
    personagem = models.ForeignKey(Personagem, related_name='pericias', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100) # Ex: Pistolas, Hacking
    atributo_base = models.CharField(max_length=50) # Ex: Agilidade
    pontos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.pontos})"


class Arma(models.Model):
    # related_name='armas' permite usar: {% for arma in personagem.armas.all %}
    personagem = models.ForeignKey(Personagem, related_name='armas', on_delete=models.CASCADE)
    
    nome = models.CharField(max_length=100, help_text="Ex: Ares Predator V")
    dano = models.CharField(max_length=10, help_text="Ex: 8P")
    ap = models.IntegerField(default=0, help_text="Penetração de Armadura (Ex: -1)")
    
    # Link inteligente: A arma sabe qual perícia usa para atirar
    pericia_associada = models.ForeignKey(Pericia, on_delete=models.CASCADE, help_text="Qual perícia essa arma usa?")

    def __str__(self):
        return f"{self.nome} ({self.dano})"