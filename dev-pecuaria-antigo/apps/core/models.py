from django.db import models
from ..pecuaria.models import *

# Produtos

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Categoria")
    description = models.CharField(max_length=100, verbose_name="Descrição")

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Subcategoria")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Subcategorias"

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Marca")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.name
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fabricante")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Fabricantes"

    def __str__(self):
        return self.name
    
class Measure(models.Model):
    name = models.CharField(max_length=100, verbose_name="Medida")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Medidas"

    def __str__(self):
        return self.name
    
class Model(models.Model):
    name = models.CharField(max_length=100, verbose_name="Modelo")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Modelos"

    def __str__(self):
        return self.name
    
class Package(models.Model):
    name = models.CharField(max_length=100, verbose_name="Embalagem")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Embalagens"

    def __str__(self):
        return self.name


class Items(models.Model):

    # Campos obrigatórios

    name = models.CharField(max_length=100, verbose_name="Nome")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name="Subcategoria")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Marca")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Fabricante")

    # Campos não obrigatórios

    measure = models.ForeignKey(Measure, on_delete=models.CASCADE, blank=True, null=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=100, verbose_name="Descrição")

    class Meta:
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name
    
# Instituição

class Institution(models.Model):
    name = models.CharField(max_length=100, verbose_name="Instituição")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.name
    
class InstituitionUnit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Unidade")
    instituition = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Instituição")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Unidades de Instituição"

    def __str__(self):
        return self.name
    
class Sector(models.Model):
    name = models.CharField(max_length=100, verbose_name="Setor")
    instituitionUnit = models.ForeignKey(InstituitionUnit, on_delete=models.CASCADE, verbose_name="Unidade")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.name
    
class SubSector(models.Model):
    name = models.CharField(max_length=100, verbose_name="Sub Setor")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name="Setor")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    
    class Meta:
        verbose_name_plural = "Sub Setores"

    def __str__(self):
        return self.name

# Pecuária (Superclasses)

class Animal(models.Model):
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Fêmea', 'Fêmea'),
        ('Indefinido', 'Indefinido'),
    ]

    identificacao_unica = models.CharField(max_length=255, unique=True, verbose_name='Identificação única')
    rfid = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='RFID')
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Espécie')
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Raça')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tipo')
    sexo = models.CharField(max_length=255, choices=SEXO_CHOICES, verbose_name='Sexo')
    peso_nascimento = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Peso de nascimento')
    data_hora_nascimento = models.DateTimeField(null=True, blank=True, verbose_name='Data e hora de nascimento')
    mae = models.ForeignKey('self', on_delete=models.CASCADE, related_name='mae_set', null=True, blank=True, verbose_name='Mãe')
    pai = models.ForeignKey('self', on_delete=models.CASCADE, related_name='pai_set', null=True, blank=True, verbose_name='Pai')
    setor = models.ForeignKey(SetorPecuaria, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Setor')

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'

    def __str__(self):
        return self.identificacao_unica
    
class Manejo(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Funcionário')
    observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

    class Meta:
        verbose_name = 'Manejo'
        verbose_name_plural = 'Manejos'

    def __str__(self):
        return self.funcionario.nome