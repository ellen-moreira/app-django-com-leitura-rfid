from django.db import models
from django.utils.translation import gettext_lazy as _

class Questionario(models.Model):
    nome = models.CharField(max_length=255 ,null=True)
    objetivo = models.TextField(null=True)
    owner = models.CharField(max_length=50, null=True, verbose_name="Criado_por")
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now_add=True)
    link = models.CharField(max_length=25, null=True)
    link_resposta = models.CharField(max_length=25, null=True)
    
    def __str__(self):
        return self.nome
    
class Type(models.Model):
    type_choices = [
        ('text', 'text'),
        ('textarea', 'textarea'),
        ('radio', 'radio'),
        ('checkbox', 'checkbox'),
        ('select', 'select'),
    ]
    tipo = models.CharField(max_length=50, choices=type_choices, unique=True)

    def __str__(self):
        return self.tipo

class Questao(models.Model):
    title = models.TextField(null=True, verbose_name="Nome")
    tipo = models.ForeignKey(Type, on_delete=models.CASCADE)
    questionario_id = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    # tipo, se a questão tem como resposta texto, multiplas respostas, seleção única, ou caixa de seleção
    # 1 = area
    # 2 = textarea
    # 3 = radio
    # 4 = checkbox
    # 5 = select
    
    class Meta:
        verbose_name = _("Questão")
        verbose_name_plural = _("Questões")

    def __str__(self):
        return str(self.title)

class Alternativa(models.Model):
    title = models.TextField(null=True, verbose_name="Nome")
    questao_id = models.ForeignKey(Questao, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
    
class Answer(models.Model):
    questionario_id = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    questao_id = models.ForeignKey(Questao, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=True)
    
    
    # user_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.answer