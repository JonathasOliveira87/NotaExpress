from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
import secrets
from manageStock.models import Produto

class selectSetor(models.Model):
    nomeSetor = models.CharField(max_length=255)

    def __str__(self):
        return self.nomeSetor
    
    class Meta:
        verbose_name = 'Gerenciar Setor'
        verbose_name_plural = 'Gerenciar Setores'


class cNota(models.Model):
    titulo = models.CharField(max_length=255)
    setor = models.ForeignKey(selectSetor, on_delete=models.CASCADE)
    tag = models.CharField(max_length=12, default=0)
    descricao = models.TextField()
    #data_criacao = models.DateTimeField(auto_now_add=True)
    data_criacao = models.DateTimeField(auto_now_add=False, default=timezone.now)
    numero = models.IntegerField(primary_key=True, editable=False, unique=True)
    #numero = models.CharField(max_length=255, primary_key=True, editable=False, unique=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, default='Null')
    fechada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero:06d}\t{self.titulo}\t{self.setor}\t{self.tag}\t{self.descricao}\t{self.data_criacao}"


    def save(self, *args, **kwargs):
        # Garante que a primeira letra de cada palavra no título seja maiúscula
        self.titulo = self.titulo.title()
        self.tag = self.tag.upper()
        super(cNota, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Gerenciar Nota'


@receiver(pre_save, sender=cNota)
def calcular_numero(sender, instance, **kwargs):
    if not instance.numero:
        # Obtenha o próximo número disponível com seis dígitos
        ultimo_numero = cNota.objects.aggregate(ultimo_numero=models.Max('numero'))['ultimo_numero']
        novo_numero = ultimo_numero + 1 if ultimo_numero else 1
        instance.numero = novo_numero
    

def generate_short_hex(length):
    return secrets.token_hex(length // 2)  # O comprimento é dividido por 2 porque cada byte é representado por 2 caracteres hexadecimais


class OrdemServico(models.Model):
    STATUS_CHOICES = (
        ('aberto', 'Aberto'),
        ('programado', 'Programado'),
        ('encerrado', 'Encerrado'),
        ('finalizado', 'Finalizado'),
    )
    orderm_criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()
    total_horas = models.CharField(max_length=12, default=0)
    itens_requisitados = models.TextField()  # JSON ou outro formato para armazenar os itens
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    id_hexadecimal = models.CharField(max_length=8, unique=True, editable=False)
    nota = models.ForeignKey(cNota, on_delete=models.CASCADE)  # Chave estrangeira referenciando a classe cNota
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)  # Chave estrangeira referenciando a classe Produto
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    encerrado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='encerradas')
    finalizado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='finalizadas')


    class Meta:
        verbose_name = 'Gerenciar Ordem'


    def save(self, *args, **kwargs):
        if not self.id_hexadecimal:  # Se o id_hexadecimal não estiver definido
            self.id_hexadecimal = generate_short_hex(8)  # Gerar um identificador hexadecimal de 4 bytes (8 caracteres)
            self.nota.fechada = True
            self.nota.save()  # Salva a nota para aplicar a alteração
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ordem criada em: {self.data_criacao.strftime('%d/%m/%Y as %H:%M')}"  # Formata data e hora


        
