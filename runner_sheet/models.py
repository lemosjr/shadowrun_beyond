import math
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
ARQUIVO: models.py
OBJETIVO: Define a estrutura do Banco de Dados com as regras do Shadowrun 6E.
"""

class Personagem(models.Model):
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
    foto = models.ImageField(upload_to='runners_avatars/', blank=True, null=True)
    
    # Dano ATUAL (O quanto ele já apanhou)
    dano_fisico = models.IntegerField(default=0)
    dano_atordoamento = models.IntegerField(default=0)

    # LIMITE MÁXIMO (Calculado automaticamente)
    max_fisico = models.IntegerField(default=10) # 8 + Body/2
    max_stun = models.IntegerField(default=10)   # 8 + Will/2

    def recalcular_monitores(self):
        """
        Regra Shadowrun 6e:
        Monitor Físico = 8 + (Corpo / 2) arredondado pra cima.
        Monitor Stun   = 8 + (Vontade / 2) arredondado pra cima.
        """
        try:
            corpo = self.atributos.get(nome='Corpo').valor
            vontade = self.atributos.get(nome='Vontade').valor
            
            self.max_fisico = 8 + math.ceil(corpo / 2)
            self.max_stun = 8 + math.ceil(vontade / 2)
            self.save()
        except Exception as e:
            print(f"Erro ao calcular vida: {e}")

    def __str__(self):
        return f"{self.codinome} ({self.metatipo})"


class Atributo(models.Model):
    # Lista oficial de Atributos
    OPCOES_ATRIBUTOS = [
        ('Corpo', 'Corpo (BOD)'),
        ('Agilidade', 'Agilidade (AGI)'),
        ('Reação', 'Reação (REA)'),
        ('Força', 'Força (STR)'),
        ('Vontade', 'Vontade (WIL)'),
        ('Lógica', 'Lógica (LOG)'),
        ('Intuição', 'Intuição (INT)'),
        ('Carisma', 'Carisma (CHA)'),
        ('Edge', 'Edge (EDG)'),
        ('Mágica', 'Mágica (MAG)'),
        ('Ressonância', 'Ressonância (RES)'),
    ]

    personagem = models.ForeignKey(Personagem, related_name='atributos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, choices=OPCOES_ATRIBUTOS, default='Corpo')
    valor = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.nome}: {self.valor}"


class Pericia(models.Model):
    # Lista oficial de Perícias do Shadowrun 6E (Com Atributo Base sugerido)
    OPCOES_PERICIAS = [
        ('Astral', 'Astral (INT)'),          # Assensing, Astral Combat
        ('Atletismo', 'Atletismo (AGI)'),    # Archery, Throwing, Gymnastics, Running
        ('Biotecnologia', 'Biotecnologia (LOG)'), # First Aid, Medicine
        ('Combate Prox', 'Combate Próximo (AGI)'), # Close Combat (Melee, Unarmed)
        ('Trambique', 'Trambique (CHA)'),    # Con (Acting, Disguise)
        ('Conjuracao', 'Conjuração (MAG)'),  # Conjuring (Summoning)
        ('Eletronica', 'Eletrônica (LOG)'),  # Computer, Hardware, Software
        ('Engenharia', 'Engenharia (LOG)'),  # Mechanic, Armorer, Demolitions
        ('Armas de Fogo', 'Armas de Fogo (AGI)'), # Firearms (Automatics, Pistols, Rifles)
        ('Influencia', 'Influência (CHA)'),  # Influence (Negotiation, Etiquette, Leadership)
        ('Ao Ar Livre', 'Ao Ar Livre (INT)'), # Outdoors (Survival, Navigation)
        ('Percepcao', 'Percepção (INT)'),    # Perception (Visual, Audio)
        ('Pilotagem', 'Pilotagem (REA)'),    # Piloting (Ground, Air, Sea)
        ('Feiticaria', 'Feitiçaria (MAG)'),  # Sorcery (Spellcasting, Counterspelling)
        ('Furtividade', 'Furtividade (AGI)'), # Stealth (Sneaking, Palming)
        ('Cracking', 'Cracking (LOG)'),      # Hacking, Cybercombat
        ('Tasking', 'Tasking (RES)'),        # Technomancer skills
        ('Exoticas', 'Armas Exóticas (AGI)'), # Exotic Weapons
    ]
    
    OPCOES_ATRIBUTOS_BASE = [
        ('Agilidade', 'Agilidade'),
        ('Corpo', 'Corpo'),
        ('Reação', 'Reação'),
        ('Força', 'Força'),
        ('Lógica', 'Lógica'),
        ('Intuição', 'Intuição'),
        ('Carisma', 'Carisma'),
        ('Vontade', 'Vontade'),
        ('Mágica', 'Mágica'),
        ('Ressonância', 'Ressonância'),
    ]

    personagem = models.ForeignKey(Personagem, related_name='pericias', on_delete=models.CASCADE)
    
    # Agora é um menu Dropdown
    nome = models.CharField(max_length=50, choices=OPCOES_PERICIAS)
    
    # Também transformei em Dropdown para garantir que o nome bata com o atributo
    atributo_base = models.CharField(max_length=50, choices=OPCOES_ATRIBUTOS_BASE)
    
    pontos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        """
        Automacão Inteligente:
        Se o usuário escolher 'Armas de Fogo' e deixar o atributo vazio ou errado,
        o sistema tenta corrigir automaticamente antes de salvar.
        """
        # Dicionário de Correção (Opcional, mas ajuda muito)
        mapa_atributos = {
            'Astral': 'Intuição',
            'Atletismo': 'Agilidade',
            'Biotecnologia': 'Lógica',
            'Combate Prox': 'Agilidade',
            'Trambique': 'Carisma',
            'Conjuracao': 'Mágica',
            'Eletronica': 'Lógica',
            'Engenharia': 'Lógica',
            'Armas de Fogo': 'Agilidade',
            'Influencia': 'Carisma',
            'Ao Ar Livre': 'Intuição',
            'Percepcao': 'Intuição',
            'Pilotagem': 'Reação',
            'Feiticaria': 'Mágica',
            'Furtividade': 'Agilidade',
            'Cracking': 'Lógica',
            'Tasking': 'Ressonância',
        }
        
        # Se não tiver atributo definido, tenta preencher sozinho
        if not self.atributo_base and self.nome in mapa_atributos:
            self.atributo_base = mapa_atributos[self.nome]
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.pontos})"


class Arma(models.Model):
    personagem = models.ForeignKey(Personagem, related_name='armas', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, help_text="Ex: Ares Predator V")
    dano = models.CharField(max_length=10, help_text="Ex: 8P")
    ap = models.IntegerField(default=0, help_text="Penetração de Armadura (Ex: -1)")
    pericia_associada = models.ForeignKey(Pericia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.dano})"

# --- SIGNAL: Cria atributos padrão automaticamente ---
@receiver(post_save, sender=Personagem)
def criar_atributos_padrao(sender, instance, created, **kwargs):
    if created:
        atributos_padrao = ['Corpo', 'Agilidade', 'Reação', 'Força', 'Vontade', 'Lógica', 'Intuição', 'Carisma']
        if not instance.atributos.exists():
            for nome_attr in atributos_padrao:
                Atributo.objects.create(personagem=instance, nome=nome_attr, valor=1)