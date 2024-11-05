from django.db import models
from django.utils import timezone

class Ronda(models.Model):
    id_ronda = models.AutoField(primary_key=True)
    hora_inicio = models.DateTimeField(default=timezone.now)
    hora_encerramento = models.DateTimeField(null=True, blank=True)
    duracao_total = models.IntegerField(default=0, verbose_name='Duração (em segundos):')  # Duração em segundos
    status = models.CharField(max_length=50, null=True, blank=True)

    def calcular_duracao(self):
        if self.hora_inicio and self.hora_encerramento:
            duracao = (self.hora_encerramento - self.hora_inicio).total_seconds()
            self.duracao_total = int(duracao)

    def save(self, *args, **kwargs):
        # Se a hora de encerramento foi definida, calcula a duração antes de salvar
        if self.hora_encerramento:
            self.calcular_duracao()
        super(Ronda, self).save(*args, **kwargs)  # Salva o objeto Ronda
        


class Ocorrencia(models.Model):
    id_ocorrencia = models.AutoField(primary_key=True)
    ronda = models.ForeignKey(Ronda, on_delete=models.CASCADE)
    local = models.CharField(max_length=100)
    texto_ocorrencia = models.TextField()
    horario = models.DateTimeField(default=timezone.now)
    
class Local(models.Model):
    nome = models.CharField(max_length=100)
    predio = models.CharField(max_length=100)
    qr_code = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"

    def __str__(self):
        return self.nome

