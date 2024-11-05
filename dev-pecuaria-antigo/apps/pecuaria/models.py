# from apps.core.models import Animal, Manejo
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class SetorPecuaria(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')
	usuarios = models.ManyToManyField(User, related_name='setor', blank=True, verbose_name='Usuários')

	class Meta:
		verbose_name = 'Setor de Pecuária'
		verbose_name_plural = 'Setores de Pecuária'

	def __str__(self):
		return self.nome

class Galpao(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')

	class Meta:
		verbose_name = 'Galpão'
		verbose_name_plural = 'Galpões'

	def __str__(self):
		return self.nome

class Sala(models.Model):
	numero = models.PositiveIntegerField(verbose_name='Número')
	galpao = models.ForeignKey(Galpao, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Galpão')

	class Meta:
		verbose_name = 'Sala'
		verbose_name_plural = 'Salas'

	def __str__(self):
		return f'Sala {self.numero} - {self.galpao.nome}'

class Baia(models.Model):
	numero = models.PositiveIntegerField(verbose_name='Número')
	sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Sala')

	class Meta:
		verbose_name = 'Baia'
		verbose_name_plural = 'Baias'

	def __str__(self):
		return f'Baia {self.numero} ({self.sala})'

class Especie(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')

	class Meta:
		verbose_name = 'Espécie'
		verbose_name_plural = 'Espécies'

	def __str__(self):
		return self.nome

class Raca(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')

	class Meta:
		verbose_name = 'Raça'
		verbose_name_plural = 'Raças'

	def __str__(self):
		return self.nome

class Tipo(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')

	class Meta:
		verbose_name = 'Tipo'
		verbose_name_plural = 'Tipos'

	def __str__(self):
		return self.nome

class Animal(models.Model):
	SEXO_CHOICES = [
		('Macho', 'Macho'),
		('Fêmea', 'Fêmea'),
		('Indefinido', 'Indefinido'),
	]

	identificacao_unica = models.CharField(max_length=255, unique=True, verbose_name='Identificação única')
	rfid = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='RFID')
	especie = models.ForeignKey(Especie, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Espécie')
	raca = models.ForeignKey(Raca, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Raça')
	tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo')
	sexo = models.CharField(max_length=255, choices=SEXO_CHOICES, verbose_name='Sexo')
	peso_nascimento = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Peso de nascimento')
	data_hora_nascimento = models.DateTimeField(null=True, blank=True, verbose_name='Data e hora de nascimento')
	mae = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='mae_animal', null=True, blank=True, verbose_name='Mãe')
	pai = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='pai_animal', null=True, blank=True, verbose_name='Pai')
	status = models.BooleanField(default=True, verbose_name='Status')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')
	parto = models.ForeignKey('Parto', on_delete=models.SET_NULL, related_name='filhotes', null=True, blank=True, verbose_name='Parto')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	class Meta:
		verbose_name = 'Animal'
		verbose_name_plural = 'Animais'

	def __str__(self):
		return self.identificacao_unica

class Suino(Animal):
	class Meta:
		verbose_name = 'Suíno'
		verbose_name_plural = 'Suínos'

	def save(self, *args, **kwargs):
		self.identificacao_unica = 'SUI-' + self.identificacao_unica if not self.identificacao_unica.startswith('SUI-') else self.identificacao_unica
		self.tipo = Tipo.objects.get_or_create(nome='Leitão')[0] if self.parto else self.tipo
		self.data_hora_nascimento = self.data_hora_nascimento if self.data_hora_nascimento else self.parto.data_hora_parto if self.parto else datetime(2021, 1, 1, 0, 0, 0)
		self.mae = self.parto.femea if self.parto else None
		self.pai = self.parto.macho if self.parto else None
		self.setor = SetorPecuaria.objects.get_or_create(nome='Suínocultura')[0]

		super(Suino, self).save(*args, **kwargs)

	def __str__(self):
		return self.identificacao_unica

class BovinoCorte(Animal):
	MODO_CRIACAO_CHOICES = [
		('Confinamento', 'Confinamento'),
		('Pasto', 'Pasto'),
	]

	modo_criacao = models.CharField(max_length=255, choices=MODO_CRIACAO_CHOICES, null=True, blank=True, verbose_name='Modo de criação')
	local = models.CharField(max_length=255, null=True, blank=True, verbose_name='Local')

	class Meta:
		verbose_name = 'Bovino de Corte'
		verbose_name_plural = 'Bovinos de Corte'

	def save(self, *args, **kwargs):
		self.identificacao_unica = 'BVC-' + self.identificacao_unica if not self.identificacao_unica.startswith('BVC-') else self.identificacao_unica
		self.data_hora_nascimento = self.data_hora_nascimento if self.data_hora_nascimento else self.parto.data_hora_parto if self.parto else datetime(2021, 1, 1, 0, 0, 0)
		self.mae = self.parto.femea if self.parto else None
		self.pai = self.parto.macho if self.parto else None
		self.setor = SetorPecuaria.objects.get_or_create(nome='Bovinocultura de Corte')[0]

		super(BovinoCorte, self).save(*args, **kwargs)

	def __str__(self):
		return self.identificacao_unica

class BovinoLeite(Animal):
	nome = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome')
	grau_sangue = models.CharField(max_length=255, null=True, blank=True, verbose_name='Grau de sangue')
	pelagem = models.CharField(max_length=255, null=True, blank=True, verbose_name='Pelagem')

	class Meta:
		verbose_name = 'Bovino de Leite'
		verbose_name_plural = 'Bovinos de Leite'

	def save(self, *args, **kwargs):
		self.identificacao_unica = 'BVL-' + self.identificacao_unica if not self.identificacao_unica.startswith('BVL-') else self.identificacao_unica
		self.data_hora_nascimento = self.data_hora_nascimento if self.data_hora_nascimento else self.parto.data_hora_parto if self.parto else datetime(2021, 1, 1, 0, 0, 0)
		self.mae = self.parto.femea if self.parto else None
		self.pai = self.parto.macho if self.parto else None
		self.setor = SetorPecuaria.objects.get_or_create(nome='Bovinocultura de Leite')[0]

		super(BovinoLeite, self).save(*args, **kwargs)

	def __str__(self):
		return self.identificacao_unica

class Parto(models.Model):
	TIPO_PARTO_CHOICES = [
		('Normal', 'Normal'),
		('Cesárea', 'Cesárea'),
	]

	femea = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='femea_parto', verbose_name='Fêmea')
	macho = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='macho_parto', verbose_name='Macho')
	data_hora_parto = models.DateTimeField(verbose_name='Data e hora do parto')
	tipo = models.CharField(max_length=255, choices=TIPO_PARTO_CHOICES, default='Normal', verbose_name='Tipo')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')
	quantidade_filhotes_vivos = models.PositiveIntegerField(default=0, verbose_name='Nº de filhotes vivos')
	quantidade_filhotes_mortos = models.PositiveIntegerField(default=0, verbose_name='Nº de filhotes mortos')
	quantidade_filhotes_mumificados = models.PositiveIntegerField(default=0, verbose_name='Nº de filhotes mumificados')

	class Meta:
		verbose_name = 'Parto'
		verbose_name_plural = 'Partos'

	def save(self, *args, **kwargs):
		self.data_hora_parto = self.data_hora_parto if self.data_hora_parto else datetime(2021, 1, 1, 0, 0, 0)
		self.setor = self.femea.setor if self.femea.setor == self.macho.setor else None
		self.filhotes.all().update(data_hora_nascimento=self.data_hora_parto, mae=self.femea, pai=self.macho, setor=self.setor) if self.pk else None

		super(Parto, self).save(*args, **kwargs)

	def __str__(self):
		return self.data_hora_parto.strftime('%d/%m/%Y %H:%M:%S')

class Lote(models.Model):
	numero = models.PositiveIntegerField(verbose_name='Número')
	baia = models.ForeignKey(Baia, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Baia')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')
	animais = models.ManyToManyField(Animal, related_name='animais', blank=True, verbose_name='Animais')

	class Meta:
		verbose_name = 'Lote'
		verbose_name_plural = 'Lotes'

	def __str__(self):
		return str(self.numero)

class TipoProcedimento(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')

	class Meta:
		verbose_name = 'Tipo do Procedimento'
		verbose_name_plural = 'Tipos de Procedimento'

	def __str__(self):
		return self.nome

class Procedimento(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')
	tipo = models.ForeignKey(TipoProcedimento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo')

	class Meta:
		verbose_name = 'Procedimento'
		verbose_name_plural = 'Procedimentos'

	def __str__(self):
		return self.nome

class TipoProduto(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')

	class Meta:
		verbose_name = 'Tipo do Produto'
		verbose_name_plural = 'Tipos de Produto'

	def __str__(self):
		return self.nome

class Produto(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')
	tipo = models.ForeignKey(TipoProduto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo')
	fabricante = models.CharField(max_length=255, null=True, blank=True, verbose_name='Fabricante')
	quantidade = models.PositiveIntegerField(default=0, verbose_name='Quantidade')
	valor = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor')

	class Meta:
		verbose_name = 'Produto'
		verbose_name_plural = 'Produtos'

	def __str__(self):
		return self.nome

class Funcionario(models.Model):
	nome = models.CharField(max_length=255, verbose_name='Nome')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')

	class Meta:
		verbose_name = 'Funcionário'
		verbose_name_plural = 'Funcionários'

	def __str__(self):
		return self.nome


class Manejo(models.Model):
	funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Funcionário')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	class Meta:
		verbose_name = 'Manejo'
		verbose_name_plural = 'Manejos'

	def __str__(self):
		return self.funcionario.nome

class ManejoPecuaria(Manejo):
	animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Animal')
	lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Lote')
	data_hora_manejo = models.DateTimeField(verbose_name='Data e hora do manejo')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')

	class Meta:
		verbose_name = 'Manejo de Pecuária'
		verbose_name_plural = 'Manejos de Pecuária'

	def save(self, *args, **kwargs):
		self.data_hora_manejo = self.data_hora_manejo if self.data_hora_manejo else datetime(2021, 1, 1, 0, 0, 0)
		self.setor = self.animal.setor if self.animal else self.lote.setor if self.lote else None

		super(ManejoPecuaria, self).save(*args, **kwargs)

	def __str__(self):
		return self.data_hora_manejo.strftime('%d/%m/%Y às %H:%M')

class ProcedimentoManejo(models.Model):
	manejo = models.ForeignKey(ManejoPecuaria, on_delete=models.SET_NULL, related_name='procedimentos', null=True, blank=True, verbose_name='Manejo')
	procedimento = models.ForeignKey(Procedimento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Procedimento')
	quantidade = models.PositiveIntegerField(default=0, verbose_name='Quantidade')
	valor = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor')

	class Meta:
		verbose_name = 'Procedimento'
		verbose_name_plural = 'Procedimentos utilizados no Manejo'

	def __str__(self):
		return self.procedimento.nome

class ProdutoManejo(models.Model):
	manejo = models.ForeignKey(ManejoPecuaria, on_delete=models.SET_NULL, related_name='produtos', null=True, blank=True, verbose_name='Manejo')
	produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Produto')
	quantidade = models.PositiveIntegerField(default=0, verbose_name='Quantidade')
	valor = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor')

	class Meta:
		verbose_name = 'Produto'
		verbose_name_plural = 'Produtos utilizados no Manejo'

	def __str__(self):
		return self.produto.nome

class Cobertura(models.Model):
	femea = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='femea_cobertura', verbose_name='Fêmea')
	macho = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='macho_cobertura', verbose_name='Macho')
	data_hora_cobertura = models.DateTimeField(verbose_name='Data e hora da cobertura')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')

	class Meta:
		verbose_name = 'Cobertura'
		verbose_name_plural = 'Coberturas'

	def save(self, *args, **kwargs):
		self.data_hora_cobertura = self.data_hora_cobertura if self.data_hora_cobertura else datetime(2021, 1, 1, 0, 0, 0)
		self.setor = self.femea.setor if self.femea.setor == self.macho.setor else None
		super(Cobertura, self).save(*args, **kwargs)

	def __str__(self):
		return self.data_hora_cobertura.strftime('%d/%m/%Y às %H:%M')

class Saida(models.Model):
	TIPO_SAIDA_CHOICES = [
		('Morte natural', 'Morte natural'),
		('Abate sanitário', 'Abate sanitário'),
		('Descarte', 'Descarte'),
		('Outros', 'Outros')
	]

	animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Animal')
	data_hora_saida = models.DateTimeField(verbose_name='Data e hora da saída')
	tipo = models.CharField(max_length=255, choices=TIPO_SAIDA_CHOICES, verbose_name='Tipo')
	setor = models.ForeignKey(SetorPecuaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Setor')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	class Meta:
		verbose_name = 'Saída'
		verbose_name_plural = 'Saídas'

	def save(self, *args, **kwargs):
		Animal.objects.filter(pk=self.animal.pk).update(status=False) if self.animal else None
		self.data_hora_saida = self.data_hora_saida if self.data_hora_saida else datetime(2021, 1, 1, 0, 0, 0)
		self.setor = self.animal.setor if self.animal.setor else None
		super(Saida, self).save(*args, **kwargs)

	def __str__(self):
		return self.data_hora_saida.strftime('%d/%m/%Y às %H:%M')