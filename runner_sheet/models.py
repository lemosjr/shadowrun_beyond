from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import math

class Personagem(models.Model):
    # Opções de Metatipo (Livro Básico)
    METATIPOS = [
        ('HUM', 'Humano (Padrão)'),
        ('ELF', 'Elfo (Agi+1, Car+2)'),
        ('ORK', 'Ork (Cor+3, For+2)'),
        ('DWF', 'Anão (Cor+2, For+2, Von+1)'),
        ('TRL', 'Troll (Cor+4, For+4, -1 Agi/Log/Car)'),
    ]
    
    # Opções de Arquétipo (Para ajudar no guia)
    ARQUETIPOS = [
        ('SAM', 'Samurai Urbano (Combate)'),
        ('MAG', 'Mago/Xamã (Magia)'),
        ('DEC', 'Decker (Hacker)'),
        ('RIG', 'Rigger (Drones/Veículos)'),
        ('FAC', 'Face (Social)'),
        ('ADE', 'Adepto (Combate Mágico)'),
    ]

    # Estilo de vida
    ESTILOS_VIDA = [
        ('RUA', 'Rua (Custo: 0¥) - Sem teto, perigoso.'),
        ('FUV', 'Favelado (Custo: 500¥) - Squatter, caixas ou contêineres.'),
        ('BAI', 'Baixo (Custo: 2.000¥) - Apartamento simples, comida barata.'),
        ('MED', 'Médio (Custo: 5.000¥) - Confortável, seguro.'),
        ('ALT', 'Alto (Custo: 10.000¥) - Luxo moderado, boa segurança.'),
        ('LUX', 'Luxo (Custo: 100.000¥+) - Elite corporativa.'),
    ]

    nome = models.CharField(max_length=100)
    codinome = models.CharField(max_length=100)
    metatipo = models.CharField(max_length=3, choices=METATIPOS, default='HUM')
    arquetipo = models.CharField(max_length=3, choices=ARQUETIPOS, default='SAM', help_text="Define o estilo de jogo")
    estilo_vida = models.CharField(max_length=3, choices=ESTILOS_VIDA, default='MED')
    
    foto = models.ImageField(upload_to='runners_avatars/', blank=True, null=True)
    
    # Recursos
    karma = models.IntegerField(default=0)
    nuyen = models.IntegerField(default=0)
    
    # Monitores
    dano_fisico = models.IntegerField(default=0)
    dano_atordoamento = models.IntegerField(default=0)
    max_fisico = models.IntegerField(default=10)
    max_stun = models.IntegerField(default=10)
    defesa_total = models.IntegerField(default=0)

    def recalcular_stats(self):
        try:
            corpo = self.atributos.get(nome='Corpo').valor
            vontade = self.atributos.get(nome='Vontade').valor
            # Regra oficial 6E: 8 + (Attr / 2) arredondado pra cima
            self.max_fisico = 8 + math.ceil(corpo / 2)
            self.max_stun = 8 + math.ceil(vontade / 2)
            
            # Defesa (Corpo + Armadura)
            armor_val = sum([a.valor_defesa for a in self.armaduras.filter(equipada=True)])
            self.defesa_total = corpo + armor_val
            
            self.save()
        except:
            pass

    def __str__(self):
        return f"{self.codinome}"

class Atributo(models.Model):
    OPCOES = [
        ('Corpo', 'Corpo (BOD)'), 
        ('Agilidade', 'Agilidade (AGI)'),
        ('Reação', 'Reação (REA)'), 
        ('Força', 'Força (STR)'),
        ('Vontade', 'Vontade (WIL)'), 
        ('Lógica', 'Lógica (LOG)'),
        ('Intuição', 'Intuição (INT)'), 
        ('Carisma', 'Carisma (CHA)'),
        ('Trunfo', 'Trunfo (EDG)'), 
        ('Mágica', 'Mágica (MAG)'),
        ('Ressonância', 'Ressonância (RES)'),
    ]
    personagem = models.ForeignKey(Personagem, related_name='atributos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, choices=OPCOES)
    valor = models.IntegerField(default=1)

class Pericia(models.Model):
    # Lista Oficial do PDF 6E
    OPCOES = [
        ('Armas de Fogo', 'Armas de Fogo (AGI)'),
        ('Armas Exóticas', 'Armas Exóticas (AGI)'),
        ('Astral', 'Astral (INT)'),
        ('Atletismo', 'Atletismo (AGI)'),
        ('Biotec', 'Biotecnologia (LOG)'),
        ('Combate Prox', 'Combate Próximo (AGI)'),
        ('Conjuracao', 'Conjuração (MAG)'),
        ('Cracking', 'Cracking (LOG)'),
        ('Eletronica', 'Eletrônica (LOG)'),
        ('Encantar', 'Encantar (MAG)'),
        ('Engenharia', 'Engenharia (LOG)'),
        ('Exteriores', 'Exteriores (INT)'), # Tradução de Outdoors
        ('Feiticaria', 'Feitiçaria (MAG)'),
        ('Furtividade', 'Furtividade (AGI)'),
        ('Influencia', 'Influência (CHA)'),
        ('Percepcao', 'Percepção (INT)'),
        ('Pilotagem', 'Pilotagem (REA)'),
        ('Tarefa', 'Tarefa (RES)'), # Tasking
        ('Trapaca', 'Trapaça (CHA)'), # Con
    ]
    personagem = models.ForeignKey(Personagem, related_name='pericias', on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, choices=OPCOES)
    atributo_base = models.CharField(max_length=50, blank=True)
    pontos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Auto-mapeamento baseado no PDF
        mapa = {
            'Armas de Fogo': 'Agilidade', 'Armas Exóticas': 'Agilidade', 'Astral': 'Intuição',
            'Atletismo': 'Agilidade', 'Biotec': 'Lógica', 'Combate Prox': 'Agilidade',
            'Conjuracao': 'Mágica', 'Cracking': 'Lógica', 'Eletronica': 'Lógica',
            'Encantar': 'Mágica', 'Engenharia': 'Lógica', 'Exteriores': 'Intuição',
            'Feiticaria': 'Mágica', 'Furtividade': 'Agilidade', 'Influencia': 'Carisma',
            'Percepcao': 'Intuição', 'Pilotagem': 'Reação', 'Tarefa': 'Ressonância',
            'Trapaca': 'Carisma'
        }
        if self.nome in mapa and not self.atributo_base:
            self.atributo_base = mapa[self.nome]
        super().save(*args, **kwargs)

# Armas, Armaduras, etc. (Mantenha igual ao anterior)
class Arma(models.Model):
    personagem = models.ForeignKey(Personagem, related_name='armas', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    dano = models.CharField(max_length=10)
    ap = models.IntegerField(default=0)
    pericia_associada = models.ForeignKey(Pericia, on_delete=models.SET_NULL, null=True, blank=True)

class Armadura(models.Model):
    personagem = models.ForeignKey(Personagem, related_name='armaduras', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    valor_defesa = models.IntegerField(default=2)
    equipada = models.BooleanField(default=True)

class Cyberware(models.Model):
    personagem = models.ForeignKey(Personagem, related_name='cyberware', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    nivel = models.IntegerField(default=1)
    essencia = models.FloatField(default=0.1)

class Equipamento(models.Model):
    personagem = models.ForeignKey(Personagem, related_name='inventario', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    qtd = models.IntegerField(default=1)

@receiver(post_save, sender=Personagem)
def init_personagem(sender, instance, created, **kwargs):
    if created and not instance.atributos.exists():
        # Lista padrão de atributos para inicializar
        padrao = ['Corpo', 'Agilidade', 'Reação', 'Força', 'Vontade', 'Lógica', 'Intuição', 'Carisma', 'Trunfo', 'Mágica']
        for attr in padrao:
            Atributo.objects.create(personagem=instance, nome=attr, valor=1)