from django.db import models


class Fazenda(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    cidade = models.CharField(max_length=50, verbose_name="Cidade")
    endereco = models.CharField(max_length=50, verbose_name="Endereço")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Fazenda"
        verbose_name_plural = "Fazendas"

    def __str__(self):
        return self.nome

class TipoCultura(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Tipo de Cultura"
        verbose_name_plural = "Tipos de Cultura"

    def __str__(self):
        return self.nome
    
class VariedadePlanta(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Variedade de Planta"
        verbose_name_plural = "Variedades de Planta"

    def __str__(self):
        return self.nome
    
class Cultivar(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Cultivar"
        verbose_name_plural = "Cultivares"

    def __str__(self):
        return self.nome
    
class Areas(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Área de Plantio"
        verbose_name_plural = "Áreas de Plantio"

    def __str__(self):
        return self.nome
    
class Talhao(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Área")
    medida = models.CharField(max_length=50, verbose_name="Medida")
    areas_plantio = models.ForeignKey(Areas, on_delete=models.CASCADE, verbose_name="Área de Plantio")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Talhão"
        verbose_name_plural = "Talhões"

    def __str__(self):
        return self.nome
    
class Planta(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    nome_cientifico = models.CharField(max_length=50, verbose_name="Nome Científico")
    tipo_cultura = models.ForeignKey(TipoCultura, on_delete=models.CASCADE, verbose_name="Tipo de Cultura")
    variedade_planta = models.ForeignKey(VariedadePlanta, on_delete=models.CASCADE, verbose_name="Variedade de Planta")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"

    def __str__(self):
        return self.nome
    
class Producao(models.Model):
    nome = models.ForeignKey(Planta, on_delete=models.CASCADE, verbose_name="Planta")
    cultivar = models.ForeignKey(Cultivar, on_delete=models.CASCADE, verbose_name="Cultivar")
    talhao = models.ForeignKey(Talhao, on_delete=models.CASCADE, verbose_name="Talhão")
    data_plantio = models.DateField(verbose_name="Data de Plantio")
    data_colheita = models.DateField(verbose_name="Data de Colheita")
    observacoes = models.TextField(verbose_name="Observações")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Produção"
        verbose_name_plural = "Produção"

    def __str__(self):
        return self.nome
    
class TipoFerramenta(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Tipo de Ferramenta"
        verbose_name_plural = "Tipos de Ferramenta"

    def __str__(self):
        return self.nome

class Ferramenta(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    tipo = models.ForeignKey(TipoFerramenta, on_delete=models.CASCADE, verbose_name="Tipo")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    quantidade = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Quantidade")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Ferramenta"
        verbose_name_plural = "Ferramentas"

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.CASCADE, verbose_name="Ferramenta")
    data_inicio = models.DateTimeField(verbose_name="Data de Início")
    data_fim = models.DateTimeField(verbose_name="Data de Fim")
    descricao = models.TextField(verbose_name="Descrição")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.nome

'''
class Insumos(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    quantidade = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Quantidade")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"

    def __str__(self):
        return self.nome
'''
