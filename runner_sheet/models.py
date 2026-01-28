from django.db import models

class Personagem(models.Model):
    METATIPOS = [
        ('Humano', 'Humano'),
        ('Elfo', 'Elfo'),
        ('Anão', 'Anão'),
        ('Ork', 'Ork'),
        ('Troll', 'Troll'),
    ]
    
    nome = models.CharField(max_length=100)
    codinome = models.CharField(max_length=50, blank=True, help_text="Nome de rua (Ex: 'Street Samurai')")
    metatipo = models.CharField(max_length=20, choices=METATIPOS, default='Humano')

    foto = models.ImageField(upload_to='runners_avatars/', blank=True, null=True)
    
    # Monitores de Condição (Dano)
    dano_fisico = models.IntegerField(default=0, help_text="Dano Físico atual")
    dano_atordoamento = models.IntegerField(default=0, help_text="Dano de Atordoamento (Stun) atual")
    
    def __str__(self):
        return f"{self.nome} ({self.codinome})"

class Atributo(models.Model):
    # Siglas padrão de Shadowrun (Inglês/Português misto para facilitar)
    OPCOES_ATRIBUTOS = [
        ('BOD', 'Constituição (BOD)'),
        ('AGI', 'Agilidade (AGI)'),
        ('REA', 'Reação (REA)'),
        ('STR', 'Força (STR)'),
        ('WIL', 'Vontade (WIL)'),
        ('LOG', 'Lógica (LOG)'),
        ('INT', 'Intuição (INT)'),
        ('CHA', 'Carisma (CHA)'),
        ('EDG', 'Limite (Edge)'),
        ('MAG', 'Magia/Ressonância'),
    ]

    personagem = models.ForeignKey(Personagem, related_name='atributos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=3, choices=OPCOES_ATRIBUTOS)
    valor = models.IntegerField(default=1)

    class Meta:
        unique_together = ('personagem', 'nome') # Impede duplicar 'AGI' no mesmo char

    def __str__(self):
        return f"{self.nome}: {self.valor}"

class Pericia(models.Model):
    personagem = models.ForeignKey(Personagem, related_name='pericias', on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, help_text="Ex: Armas de Fogo, Furtividade")
    atributo_base = models.CharField(max_length=3, choices=Atributo.OPCOES_ATRIBUTOS)
    valor = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.valor})"

    def get_dice_pool(self):
        """
        Retorna a parada de dados: Valor da Perícia + Valor do Atributo Base
        """
        try:
            # Busca o atributo correspondente no mesmo personagem
            attr = self.personagem.atributos.get(nome=self.atributo_base)
            return self.valor + attr.valor
        except Atributo.DoesNotExist:
            return self.valor # Fallback se não achar o atributo
        
class Arma(models.Model):
    personagem = models.ForeignKey(Personagem, related_name='armas', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, help_text="Ex: Ares Predator V")
    dano = models.CharField(max_length=10, help_text="Ex: 8P")
    ap = models.IntegerField(default=0, help_text="Penetração de Armadura (Ex: -1)")
    
    # O Pulo do Gato: A arma sabe qual perícia usar
    pericia_associada = models.ForeignKey(Pericia, on_delete=models.CASCADE, help_text="Qual perícia essa arma usa?")

    def __str__(self):
        return f"{self.nome} ({self.dano})"