from django.db import models

'''
class Pessoa(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

#cadastro de tipos de dispositivos
class Tipo_dispositivo(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Tipos de dispositivos"

    def __str__(self):
        return f"{self.nome}"
    
#montar os dispositivos
class Dispositivo(models.Model):
    nome = models.CharField(max_length=255)
    tipo_dispositivo = models.ForeignKey(Tipo_dispositivo, on_delete=models.CASCADE)
    especificacao_tecnica = models.TextField(null=True, blank=True, verbose_name="Especificação técnica")

    def __str__(self):
        return f"{self.nome} - Categoria: {self.tipo_dispositivo}"
    
class Atuador(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tipo de atuador")
    fabricante = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição")
    data_sheet = models.TextField(max_length=25, blank=True, null=True)
    data_sheet_local = models.TextField(max_length=255, blank=True, null=True)
    quantidade_estoque = models.CharField(max_length=255)
    localizacao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Localização")
    especificacao_tecnica = models.TextField(null=True, blank=True, verbose_name="Especificação técnica")
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='Atuadores', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Atuadores"

    def __str__(self):
        return f"{self.nome} - Categoria: {self.tipo}"

class Componente_Tipo(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Tipos de Componentes"

    def __str__(self):
        return self.nome
    
#cadastro de componentes
class Componente(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.ForeignKey(Componente_Tipo, on_delete=models.CASCADE, verbose_name="Tipo de componente")
    fabricante = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição")
    data_sheet = models.CharField(max_length=255, blank=True, null=True)
    data_sheet_local = models.CharField(max_length=255, blank=True, null=True)
    quantidade_estoque = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits = 10, decimal_places= 2, verbose_name="Preço")
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    especificacao_tecnica = models.TextField(null=True, blank=True, verbose_name="Especificação técnica")
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='Componentes')

    def __str__(self):
        return f"{self.nome} - Categoria: {self.tipo}"

class Componentes_especificacoes(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        verbose_name_plural = "Especificações componentes"

    def __str__(self):
        return f"{self.componente} - {self.descricao}"

class Servico(models.Model):
    servico = models.TextField()

    class Meta:
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.servico

#cadastro de manutenção
class Manutencao(models.Model):     
    dispositivo_manutencao = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, verbose_name="Dispositivo manutençaõ")
    responsavel = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    especificacao_tecnica = models.TextField(null=True, blank=True, verbose_name="Especificação técnica")
    data_manutencao = models.DateField(verbose_name="Data inicio manutenção")
    data_termino_manutencao = models.DateField(null=True, blank=True, verbose_name="Data término manutenção")
    tipo_manutencao = models.TextField(null=True, blank=True, verbose_name="Tipo de manutenção")

    class Meta:
        verbose_name_plural = "Manutenção"

    def __str__(self):
        formatted_data_manutencao = self.data_manutencao.strftime('%d/%m/%Y')
        formatted_data_termino = self.data_termino_manutencao.strftime('%d/%m/%Y') if self.data_termino_manutencao else "Em reparo"
        return f"{self.dispositivo_manutencao} - Data início: {formatted_data_manutencao} - Data término: {formatted_data_termino}"
    
class Manutencao_Servico(models.Model):
    manutencao = models.ForeignKey('Manutencao',on_delete=models.CASCADE, verbose_name="Manutenção")
    servico = models.ForeignKey('Servico',on_delete=models.CASCADE, verbose_name="Serviço")
    class Meta:
        verbose_name_plural = "Manutenção Serviços"
    def __str__(self):
        return f"{self.manutencao.name} - {self.servico.name}"

class Manutencao_Produto(models.Model):
    manutencao = models.ForeignKey(Manutencao, on_delete=models.CASCADE, verbose_name="Manutenção")
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE, verbose_name="Componentes")

    class Meta:
        verbose_name_plural = "Manutenção produto"

    def __str__(self):
        return f"{self.manutencao} - {self.componente}"

class Setor(models.Model):
    setor = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.setor

class Setor_Unidade(models.Model):
    nome = models.CharField(max_length=255)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Setor Unidade"

    def __str__(self):
        return f"{self.nome} - {self.setor}"

#cadastro de alocação dos dispositivos com suas localizações
class Alocacao_dispositivo(models.Model):
    nome = models.CharField(max_length=255)
    dispositivo_alocado = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    local_unidade = models.ForeignKey(Setor_Unidade, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_alocacao = models.DateField(verbose_name="Data de alocação")
    data_desalocacao = models.DateField(null=True, blank=True, verbose_name="Data de desalocação")
    notas_alocacao = models.TextField(null=True, blank=True, verbose_name="Notas sobre alocação")
    alerta_alocacao = models.TextField(null=True, blank=True, verbose_name="Alerta alocação")

    class Meta:
        verbose_name_plural = "Alocação Dispositivos"

    def formatted_data_alocacao(self):
        return self.data_alocacao.strftime('%d/%m/%Y')
    def __str__(self):
        return f"{self.dispositivo_alocado} - Localização: {self.local_unidade} - Alocação: {self.formatted_data_alocacao()}"
'''