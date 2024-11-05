from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

# Create your models here.

class Setor(models.Model):
	"""
	Classe que representa o modelo Setor
	
	Atributos:
	----------
		>>> nome: CharField - Nome do setor
		>>> descricao: TextField - Descrição do setor
		>>> usuarios: ManyToManyField - Usuários do setor

	Métodos:
	----------
		>>> adicionar_usuario: Método que adiciona um usuário ao setor
		>>> remover_usuario: Método que remove um usuário do setor
		>>> listar_usuarios: Método que retorna a lista de usuários do setor
		>>> __str__: Método que retorna a representação em string do setor
	"""

	class Meta:
		verbose_name = 'Setor'
		verbose_name_plural = 'Setores'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome do setor')
	descricao = models.TextField(null=True, blank=True, verbose_name='Descrição do setor')
	usuarios = models.ManyToManyField(User, related_name='setor_usuarios', blank=True, verbose_name='Usuários do setor')

	def adicionar_usuario(self, usuario):
		"""
		Método que adiciona um usuário ao setor
		"""
		self.usuarios.add(usuario)

	def remover_usuario(self, usuario):
		"""
		Método que remove um usuário do setor
		"""
		self.usuarios.remove(usuario)

	def listar_usuarios(self):
		"""
		Método que retorna a lista de usuários do setor
		"""
		return self.usuarios.all()

	def __str__(self):
		return self.nome
	
class Galpao(models.Model):
	"""
	Classe que representa o modelo Galpão
	
	Atributos:
	----------
		>>> nome: CharField - Nome do galpão
		>>> setor: ForeignKey - Setor do galpão

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string do galpão
	"""

	class Meta:
		verbose_name = 'Galpão'
		verbose_name_plural = 'Galpões'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')
	setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, related_name='galpao_setor', null=True, blank=True, verbose_name='Setor')

	def __str__(self):
		return self.nome

class Sala(models.Model):
	"""
	Classe que representa o modelo Sala
	
	Atributos:
	----------
		>>> numero: PositiveIntegerField - Número da sala
		>>> galpao: ForeignKey - Galpão da sala

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string da sala
	"""

	class Meta:
		verbose_name = 'Sala'
		verbose_name_plural = 'Salas'
		ordering = ['numero']

	numero = models.PositiveIntegerField(verbose_name='Número')
	galpao = models.ForeignKey(Galpao, on_delete=models.SET_NULL, related_name='sala_galpao', null=True, blank=True, verbose_name='Galpão')

	def __str__(self):
		return f'Sala {self.numero} - {self.galpao.nome}'

class Baia(models.Model):
	"""
	Classe que representa o modelo Baia
	
	Atributos:
	----------
		>>> numero: PositiveIntegerField - Número da baia
		>>> sala: ForeignKey - Sala da baia

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string da baia
	"""

	class Meta:
		verbose_name = 'Baia'
		verbose_name_plural = 'Baias'
		ordering = ['numero']

	numero = models.PositiveIntegerField(verbose_name='Número')
	sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, related_name='baia_sala', null=True, blank=True, verbose_name='Sala')

	def __str__(self):
		return f'Baia {self.numero} ({self.sala})'
	
class Especie(models.Model):
	"""
	Classe que representa o modelo Espécie

	Atributos:
	----------
		>>> nome: CharField - Nome da espécie

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string da espécie
	"""

	class Meta:
		verbose_name = 'Espécie'
		verbose_name_plural = 'Espécies'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')

	def __str__(self):
		return self.nome

class Raca(models.Model):
	"""
	Classe que representa o modelo Raça

	Atributos:
	----------
		>>> nome: CharField - Nome da raça

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string da raça
	"""

	class Meta:
		verbose_name = 'Raça'
		verbose_name_plural = 'Raças'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')

	def __str__(self):
		return self.nome

class Tipo(models.Model):
	"""
	Classe que representa o modelo Tipo

	Atributos:
	----------
		>>> nome: CharField - Nome do tipo

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string do tipo
	"""

	class Meta:
		verbose_name = 'Tipo'
		verbose_name_plural = 'Tipos'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')

	def __str__(self):
		return self.nome
	
class Animal(models.Model):
	"""
	Classe que representa o modelo Animal

	Atributos:
	----------
		>>> identificacao_unica: CharField - Identificação única do animal
		>>> rfid: CharField - RFID do animal
		>>> especie: ForeignKey - Espécie do animal
		>>> raca: ForeignKey - Raça do animal
		>>> tipo: ForeignKey - Tipo do animal
		>>> sexo: CharField - Sexo do animal
		>>> data_hora_de_nascimento: DateTimeField - Data e hora de nascimento do animal
		>>> mae: ForeignKey - Mãe do animal
		>>> pai: ForeignKey - Pai do animal
		>>> status: BooleanField - Status do animal (ativo ou inativo)
		>>> setor: ForeignKey - Setor do animal
		>>> parto: ForeignKey - Parto do animal
		>>> observacao: TextField - Observação do animal

	Métodos:
	----------
		>>> calcular_idade_em_dias: Método que calcula a idade do animal em dias
		>>> calcular_idade_em_meses: Método que calcula a idade do animal em meses
		>>> calcular_idade_em_anos: Método que calcula a idade do animal em anos
		>>> get_observacao_resumida: Método que retorna uma versão resumida da observação do animal
		>>> __str__: Método que retorna a representação em string do animal
	"""

	class Meta:
		verbose_name = 'Animal'
		verbose_name_plural = 'Animais'
		ordering = ['identificacao_unica']

	SEXOS = [
		('Macho', 'Macho'),
		('Fêmea', 'Fêmea'),
		('Indefinido', 'Indefinido'),
	]

	identificacao_unica = models.CharField(max_length=255, unique=True, verbose_name='Identificação única')
	rfid = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='RFID')
	especie = models.ForeignKey(Especie, on_delete=models.SET_NULL, related_name='animal_especie', null=True, blank=True, verbose_name='Espécie')
	raca = models.ForeignKey(Raca, on_delete=models.SET_NULL, related_name='animal_raca', null=True, blank=True, verbose_name='Raça')
	tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, related_name='animal_tipo', null=True, blank=True, verbose_name='Tipo')
	sexo = models.CharField(max_length=255, choices=SEXOS, verbose_name='Sexo')
	peso_de_nascimento = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Peso de nascimento')
	data_hora_de_nascimento = models.DateTimeField(null=True, blank=True, verbose_name='Data e hora de nascimento')
	mae = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='animal_mae', null=True, blank=True, verbose_name='Mãe')
	pai = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='animal_pai', null=True, blank=True, verbose_name='Pai')
	status = models.BooleanField(default=True, verbose_name='Status')
	setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, related_name='animal_setor', null=True, blank=True, verbose_name='Setor')
	parto = models.ForeignKey('Parto', on_delete=models.SET_NULL, related_name='animal_parto', null=True, blank=True, verbose_name='Parto')
	foto = models.ImageField(upload_to='animais/', null=True, blank=True, verbose_name='Foto')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	def calcular_idade_em_dias(self):
		"""
		Método que calcula a idade do animal em dias
		"""
		return (timezone.now() - self.data_hora_de_nascimento).days
	
	def calcular_idade_em_meses(self):
		"""
		Método que calcula a idade do animal em meses
		"""
		return (timezone.now() - self.data_hora_de_nascimento).days // 30
	
	def calcular_idade_em_anos(self):
		"""
		Método que calcula a idade do animal em anos
		"""
		return (timezone.now() - self.data_hora_de_nascimento).days // 365
	
	def get_observacao_resumida(self):
		"""
		Método que retorna uma versão resumida da observação do animal.
		"""
		if self.observacao:
			return self.observacao[:50] + '...' if len(self.observacao) > 50 else self.observacao
		return ''

	def __str__(self):
		return self.identificacao_unica
	
class Suino(Animal):
	"""
	Classe que representa o modelo Suíno
	
	Atributos:
	----------
		>>> identificacao_unica: CharField - Identificação única do suíno
		>>> rfid: CharField - RFID do suíno
		>>> especie: ForeignKey - Espécie do suíno
		>>> raca: ForeignKey - Raça do suíno
		>>> tipo: ForeignKey - Tipo do suíno
		>>> sexo: CharField - Sexo do suíno
		>>> data_hora_de_nascimento: DateTimeField - Data e hora de nascimento do suíno
		>>> mae: ForeignKey - Mãe do suíno
		>>> pai: ForeignKey - Pai do suíno
		>>> status: BooleanField - Status do suíno (ativo ou inativo)
		>>> setor: ForeignKey - Setor do suíno
		>>> parto: ForeignKey - Parto do suíno
		>>> observacao: TextField - Observação do suíno

	Métodos:
	----------
		>>> save: Método que salva o suíno no banco de dados
	"""

	class Meta:
		verbose_name = 'Suíno'
		verbose_name_plural = 'Suínos'
		ordering = ['identificacao_unica']

	def save(self, *args, **kwargs):
		self.identificacao_unica = 'SUI-' + self.identificacao_unica if not self.identificacao_unica.startswith('SUI-') else self.identificacao_unica
		self.tipo = Tipo.objects.get_or_create(nome='Leitão')[0] if self.parto else self.tipo
		self.data_hora_de_nascimento = self.data_hora_de_nascimento if self.data_hora_de_nascimento else self.parto.data_hora_do_parto if self.parto else datetime(2021, 1, 1, 0, 0, 0)
		self.mae = self.parto.femea if self.parto else None
		self.pai = self.parto.macho if self.parto else None
		self.setor = Setor.objects.get_or_create(nome='Suinocultura')[0]

		super(Suino, self).save(*args, **kwargs)

class BovinoCorte(Animal):
	"""
	Classe que representa o modelo Bovino de Corte

	Atributos:
	----------
		>>> identificacao_unica: CharField - Identificação única do bovino de corte
		>>> rfid: CharField - RFID do bovino de corte
		>>> especie: ForeignKey - Espécie do bovino de corte
		>>> raca: ForeignKey - Raça do bovino de corte
		>>> tipo: ForeignKey - Tipo do bovino de corte
		>>> sexo: CharField - Sexo do bovino de corte
		>>> data_hora_de_nascimento: DateTimeField - Data e hora de nascimento do bovino de corte
		>>> mae: ForeignKey - Mãe do bovino de corte
		>>> pai: ForeignKey - Pai do bovino de corte
		>>> status: BooleanField - Status do bovino de corte (ativo ou inativo)
		>>> setor: ForeignKey - Setor do bovino de corte
		>>> parto: ForeignKey - Parto do bovino de corte
		>>> observacao: TextField - Observação do bovino de corte
		>>> modo_de_criacao: CharField - Modo de criação do bovino de corte
		>>> local: CharField - Local do bovino de corte

	Métodos:
	----------
		>>> save: Método que salva o bovino de corte no banco de dados
	"""

	class Meta:
		verbose_name = 'Bovino de Corte'
		verbose_name_plural = 'Bovinos de Corte'
		ordering = ['identificacao_unica']

	MODOS_DE_CRIACAO = [
		('Confinamento', 'Confinamento'),
		('Pasto', 'Pasto'),
	]

	LOCAIS = []

	modo_de_criacao = models.CharField(max_length=255, choices=MODOS_DE_CRIACAO, null=True, blank=True, verbose_name='Modo de criação')
	local =	models.CharField(max_length=255, choices=LOCAIS, null=True, blank=True, verbose_name='Local')

	def save(self, *args, **kwargs):
		self.identificacao_unica = 'BVC-' + self.identificacao_unica if not self.identificacao_unica.startswith('BVC-') else self.identificacao_unica
		self.data_hora_de_nascimento = self.data_hora_de_nascimento if self.data_hora_de_nascimento else self.parto.data_hora_do_parto if self.parto else datetime(2021, 1, 1, 0, 0, 0)
		self.mae = self.parto.femea if self.parto else None
		self.pai = self.parto.macho if self.parto else None
		self.setor = Setor.objects.get_or_create(nome='Bovinocultura de Corte')[0]

		super(BovinoCorte, self).save(*args, **kwargs)

class BovinoLeite(Animal):
	"""
	Classe que representa o modelo Bovino de Leite
	
	Atributos:
	----------
		>>> identificacao_unica: CharField - Identificação única do bovino de leite
		>>> rfid: CharField - RFID do bovino de leite
		>>> especie: ForeignKey - Espécie do bovino de leite
		>>> raca: ForeignKey - Raça do bovino de leite
		>>> tipo: ForeignKey - Tipo do bovino de leite
		>>> sexo: CharField - Sexo do bovino de leite
		>>> data_hora_de_nascimento: DateTimeField - Data e hora de nascimento do bovino de leite
		>>> mae: ForeignKey - Mãe do bovino de leite
		>>> pai: ForeignKey - Pai do bovino de leite
		>>> status: BooleanField - Status do bovino de leite (ativo ou inativo)
		>>> setor: ForeignKey - Setor do bovino de leite
		>>> parto: ForeignKey - Parto do bovino de leite
		>>> observacao: TextField - Observação do bovino de leite
		>>> nome: CharField - Nome do bovino de leite
		>>> grau_sangue: CharField - Grau de sangue do bovino de leite
		>>> pelagem: CharField - Pelagem do bovino de leite

	Métodos:
	----------
		>>> save: Método que salva o bovino de leite no banco de dados
	"""

	class Meta:
		verbose_name = 'Bovino de Leite'
		verbose_name_plural = 'Bovinos de Leite'
		ordering = ['identificacao_unica']

	nome = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome')
	grau_de_sangue = models.CharField(max_length=255, null=True, blank=True, verbose_name='Grau de sangue')
	pelagem = models.CharField(max_length=255, null=True, blank=True, verbose_name='Pelagem')

	def save(self, *args, **kwargs):
		self.identificacao_unica = 'BVL-' + self.identificacao_unica if not self.identificacao_unica.startswith('BVL-') else self.identificacao_unica
		self.data_hora_de_nascimento = self.data_hora_de_nascimento if self.data_hora_de_nascimento else self.parto.data_hora_do_parto if self.parto else datetime(2021, 1, 1, 0, 0, 0)
		self.mae = self.parto.femea if self.parto else None
		self.pai = self.parto.macho if self.parto else None
		self.setor = Setor.objects.get_or_create(nome='Bovinocultura de Leite')[0]

		super(BovinoLeite, self).save(*args, **kwargs)

class Lote(models.Model):
	"""
	Classe que representa o modelo Lote

	Atributos:
	----------
		>>> numero: PositiveIntegerField - Número do lote
		>>> baia: ForeignKey - Baia do lote
		>>> animais: ManyToManyField - Animais do lote
		>>> setor: ForeignKey - Setor do lote
		>>> observacao: TextField - Observação do lote

	Métodos:
	----------
		>>> adicionar_animal: Método que adiciona um animal ao lote
		>>> remover_animal: Método que remove um animal do lote
		>>> get_animais: Método que retorna a lista de animais do lote
		>>> get_quantidade_animais: Método que retorna a quantidade de animais do lote
		>>> __str__: Método que retorna a representação em string do lote
	"""

	class Meta:
		verbose_name = 'Lote'
		verbose_name_plural = 'Lotes'
		ordering = ['numero']

	numero = models.PositiveIntegerField(verbose_name='Número')
	baia = models.ForeignKey(Baia, on_delete=models.SET_NULL, related_name='lote_baia', null=True, blank=True, verbose_name='Baia')
	animais = models.ManyToManyField(Animal, related_name='lote_animais', blank=True, verbose_name='Animais')
	setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, related_name='lote_setor', null=True, blank=True, verbose_name='Setor')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	def adicionar_animal(self, animal):
		"""
		Método que adiciona um animal ao lote
		"""
		self.animais.add(animal)

	def remover_animal(self, animal):
		"""
		Método que remove um animal do lote
		"""
		self.animais.remove(animal)

	def get_animais(self):
		"""
		Método que retorna a lista de animais do lote
		"""
		return [animal.identificacao_unica for animal in self.animais.all()]
	
	def get_quantidade_animais(self):
		"""
		Método que retorna a quantidade de animais do lote
		
		Retorno:
		----------
			>>> int - Quantidade de animais do lote
		"""
		return self.animais.count()
	
	def __str__(self):
		return str(self.numero)
		
class Parto(models.Model):
	"""
	Classe que representa o modelo Parto

	Atributos:
	----------
		>>> femea: ForeignKey - Fêmea do parto
		>>> macho: ForeignKey - Macho do parto
		>>> data_hora_do_parto: DateTimeField - Data e hora do parto
		>>> tipo: CharField - Tipo de parto
		>>> setor: ForeignKey - Setor do parto
		>>> observacao: TextField - Observação do parto

	Métodos:
	----------
		>>> save: Método que salva o parto no banco de dados
		>>> get_quantidade_filhotes: Método que retorna o número de filhotes nascidos no parto
		>>> get_idade_filhotes: Método que retorna a idade dos filhotes em dias
		>>> get_tipo_parto_display: Método que retorna a representação legível do tipo de parto
		>>> get_observacao_resumida: Método que retorna uma versão resumida da observação do parto
		>>> __str__: Método que retorna a representação em string do parto
	"""

	class Meta:
		verbose_name = 'Parto'
		verbose_name_plural = 'Partos'
		ordering = ['data_hora_do_parto']

	TIPOS_DE_PARTO = [
		('Normal', 'Normal'),
		('Cesárea', 'Cesárea'),
	]

	femea = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='parto_femea', verbose_name='Fêmea')
	macho = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='parto_macho', verbose_name='Macho')
	data_hora_do_parto = models.DateTimeField(verbose_name='Data e hora do parto')
	tipo = models.CharField(max_length=255, choices=TIPOS_DE_PARTO, verbose_name='Tipo de parto')
	quantidade_de_filhotes_vivos = models.PositiveIntegerField(default=0, verbose_name='Quantidade de filhotes vivos')
	quantidade_de_filhotes_mortos = models.PositiveIntegerField(default=0, verbose_name='Quantidade de filhotes mortos')
	quantidade_de_filhotes_mumificados = models.PositiveIntegerField(default=0, verbose_name='Quantidade de filhotes mumificados')
	setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True, related_name='parto_setor', verbose_name='Setor')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	def save(self, *args, **kwargs):
		self.data_hora_do_parto = self.data_hora_do_parto if self.data_hora_do_parto else datetime(2021, 1, 1, 0, 0, 0)
		self.setor = self.femea.setor if self.femea.setor == self.macho.setor else None
		self.animal_parto.all().update(data_hora_de_nascimento=self.data_hora_do_parto, mae=self.femea, pai=self.macho, setor=self.setor) if self.pk else None

		super(Parto, self).save(*args, **kwargs)

	def get_quantidade_filhotes(self):
		"""
		Método que retorna o número de filhotes nascidos no parto.
		"""
		return self.animal_parto.count() or self.quantidade_de_filhotes_vivos + self.quantidade_de_filhotes_mortos + self.quantidade_de_filhotes_mumificados

	def get_idade_filhotes(self):
		"""
		Método que retorna a idade dos filhotes em dias.
		"""
		horas = (datetime.now() - self.data_hora_do_parto).total_seconds() / 3600
		dias = horas / 24
		return int(dias)

	def get_tipo_parto_display(self):
		"""
		Método que retorna a representação legível do tipo de parto.
		"""
		return dict(self.TIPOS_DE_PARTO).get(self.tipo, '')

	def get_observacao_resumida(self):
		"""
		Método que retorna uma versão resumida da observação do parto.
		"""
		if self.observacao:
			return self.observacao[:50] + '...' if len(self.observacao) > 50 else self.observacao
		return ''
	
	def __str__(self):
		return self.data_hora_do_parto.strftime('%d/%m/%Y às %H:%M')
	
class Funcionario(models.Model):
	"""
	Classe que representa o modelo Funcionário

	Atributos:
	----------
		>>> nome: CharField - Nome do funcionário
		>>> setor: ForeignKey - Setor do funcionário

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string do funcion
	"""

	class Meta:
		verbose_name = 'Funcionário'
		verbose_name_plural = 'Funcionários'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')
	setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, related_name='funcionario_setor', null=True, blank=True, verbose_name='Setor')

	def __str__(self):
		return self.nome
	
class TipoProcedimento(models.Model):
	"""
	Classe que representa o modelo Tipo de Procedimento

	Atributos:
	----------
		>>> nome: CharField - Nome do tipo de procedimento

	Métodos:
	----------
		>>> get_procedimentos: Método que retorna todos os procedimentos associados a este tipo de procedimento
		>>> get_numero_procedimentos: Método que retorna o número de procedimentos associados a este tipo de procedimento
		>>> __str__: Método que retorna a representação em string do tipo de procedimento
	"""

	class Meta:
		verbose_name = 'Tipo do Procedimento'
		verbose_name_plural = 'Tipos de Procedimento'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')

	def get_procedimentos(self):
		"""
		Método que retorna todos os procedimentos associados a este tipo de procedimento.
		"""
		return Procedimento.objects.filter(tipo=self)

	def get_numero_procedimentos(self):
		"""
		Método que retorna o número de procedimentos associados a este tipo de procedimento.
		"""
		return self.get_procedimentos().count()
	
	def __str__(self):
		return self.nome

class Procedimento(models.Model):
	"""
	Classe que representa o modelo Procedimento

	Atributos:
	----------
		>>> nome: CharField - Nome do procedimento
		>>> tipo: ForeignKey - Tipo do procedimento

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string do procedimento
	"""

	class Meta:
		verbose_name = 'Procedimento'
		verbose_name_plural = 'Procedimentos'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')
	tipo = models.ForeignKey(TipoProcedimento, on_delete=models.SET_NULL, related_name='procedimento_tipo', null=True, blank=True, verbose_name='Tipo')

	def __str__(self):
		return self.nome

class TipoProduto(models.Model):
	"""
	Classe que representa o modelo Tipo de Produto

	Atributos:
	----------
		>>> nome: CharField - Nome do tipo de produto

	Métodos:
	----------
		>>> get_produtos: Método que retorna todos os produtos associados a este tipo de produto
		>>> get_numero_produtos: Método que retorna o número de produtos associados a este tipo de produto
		>>> __str__: Método que retorna a representação em string do tipo de produto
	"""

	class Meta:
		verbose_name = 'Tipo do Produto'
		verbose_name_plural = 'Tipos de Produto'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')

	def get_produtos(self):
		"""
		Método que retorna todos os produtos associados a este tipo de produto.
		"""
		return Produto.objects.filter(tipo=self)
	
	def get_numero_produtos(self):
		"""
		Método que retorna o número de produtos associados a este tipo de produto.
		"""
		return self.get_produtos().count()

	def __str__(self):
		return self.nome

class Produto(models.Model):
	"""
	Classe que representa o modelo Produto

	Atributos:
	----------
		>>> nome: CharField - Nome do produto
		>>> tipo: ForeignKey - Tipo do produto
		>>> fabricante: CharField - Fabricante do produto
		>>> quantidade: PositiveIntegerField - Quantidade do produto
		>>> valor: DecimalField - Valor do produto

	Métodos:
	----------
		>>> __str__: Método que retorna a representação em string do produto
	"""

	class Meta:
		verbose_name = 'Produto'
		verbose_name_plural = 'Produtos'
		ordering = ['nome']

	nome = models.CharField(max_length=255, verbose_name='Nome')
	tipo = models.ForeignKey(TipoProduto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo')
	fabricante = models.CharField(max_length=255, null=True, blank=True, verbose_name='Fabricante')
	quantidade = models.PositiveIntegerField(default=0, verbose_name='Quantidade')
	valor = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor')

	def __str__(self):
		return self.nome
	
class Manejo(models.Model):
	"""
	Classe que representa o modelo Manejo

	Atributos:
	----------
		>>> funcionario: ForeignKey - Funcionário do manejo
		>>> data_hora_do_manejo: DateTimeField - Data e hora do manejo
		>>> animal: ForeignKey - Animal do manejo
		>>> setor: ForeignKey - Setor do manejo
		>>> observacao: TextField - Observação do manejo

	Métodos:
	----------
		>>> save: Método que salva o manejo no banco de dados
		>>> get_observacao_resumida: Método que retorna uma versão resumida da observação do manejo
		>>> __str__: Método que retorna a representação em string do manejo
	"""

	class Meta:
		verbose_name = 'Manejo'
		verbose_name_plural = 'Manejos'
		ordering = ['data_hora_do_manejo']

	funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, related_name='manejo_funcionario', null=True, blank=True, verbose_name='Funcionário')
	data_hora_do_manejo = models.DateTimeField(verbose_name='Data e hora do manejo')
	animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, related_name='manejo_animal', null=True, blank=True, verbose_name='Animal')
	lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, related_name='manejo_lote', null=True, blank=True, verbose_name='Lote')
	setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, related_name='manejo_setor', null=True, blank=True, verbose_name='Setor')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	def save(self, *args, **kwargs):
		self.data_hora_do_manejo = self.data_hora_do_manejo if self.data_hora_do_manejo else datetime(2021, 1, 1, 0, 0, 0)
		self.setor = self.animal.setor if self.animal else self.lote.setor if self.lote else None

		super(Manejo, self).save(*args, **kwargs)

	def get_observacao_resumida(self):
		"""
		Método que retorna uma versão resumida da observação do manejo.
		"""
		if self.observacao:
			return self.observacao[:50] + '...' if len(self.observacao) > 50 else self.observacao
		return ''

	def __str__(self):
		return self.data_hora_do_manejo.strftime('%d/%m/%Y às %H:%M')
	
class ProcedimentoManejo(models.Model):
	"""
	Classe que representa o modelo Procedimento do Manejo

	Atributos:
	----------
		>>> manejo: ForeignKey - Manejo do procedimento do manejo
		>>> procedimento: ForeignKey - Procedimento do procedimento do manejo
		>>> quantidade: PositiveIntegerField - Quantidade do procedimento do manejo
		>>> valor: DecimalField - Valor do procedimento do manejo

	Métodos:
	----------
		>>> calcular_custo_total: Método que calcula o custo total do procedimento do manejo
		>>> __str__: Método que retorna a representação em string do procedimento do manejo
	"""

	class Meta:
		verbose_name = 'Procedimento do Manejo'
		verbose_name_plural = 'Procedimentos do Manejo'
		ordering = ['manejo']

	manejo = models.ForeignKey(Manejo, on_delete=models.SET_NULL, related_name='procedimento_manejo', null=True, blank=True, verbose_name='Manejo')
	procedimento = models.ForeignKey(Procedimento, on_delete=models.SET_NULL, related_name='procedimento_procedimento', null=True, blank=True, verbose_name='Procedimento')
	quantidade = models.PositiveIntegerField(default=0, verbose_name='Quantidade')
	valor = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor')

	def calcular_custo_total(self):
		"""
		Método que calcula o custo total do procedimento do manejo, multiplicando a quantidade pelo valor do procedimento.
		"""
		return self.quantidade * self.valor

	def __str__(self):
		return self.procedimento.nome
	
class ProdutoManejo(models.Model):
	"""
	Classe que representa o modelo Produto do Manejo

	Atributos:
	----------
		>>> manejo: ForeignKey - Manejo do produto do manejo
		>>> produto: ForeignKey - Produto do produto do manejo
		>>> quantidade: PositiveIntegerField - Quantidade do produto do manejo
		>>> valor: DecimalField - Valor do produto do manejo

	Métodos:
	----------
		>>> calcular_custo_total: Método que calcula o custo total do produto do manejo
		>>> __str__: Método que retorna a representação em string do produto do manejo
	"""

	class Meta:
		verbose_name = 'Produto do Manejo'
		verbose_name_plural = 'Produtos do Manejo'
		ordering = ['manejo']

	manejo = models.ForeignKey(Manejo, on_delete=models.SET_NULL, related_name='produto_manejo', null=True, blank=True, verbose_name='Manejo')
	produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, related_name='produto_produto', null=True, blank=True, verbose_name='Produto')
	quantidade = models.PositiveIntegerField(default=0, verbose_name='Quantidade')
	valor = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor')

	def calcular_custo_total(self):
		"""
		Método que calcula o custo total do produto do manejo, multiplicando a quantidade pelo valor do produto.
		"""
		return self.quantidade * self.valor
	
	def __str__(self):
		return self.produto.nome
	
class Saida(models.Model):
	"""
	Classe que representa o modelo Saída

	Atributos:
	----------
		>>> data_hora_da_saida: DateTimeField - Data e hora da saída
		>>> tipo: CharField - Tipo de saída
		>>> animais: ManyToManyField - Animais da saída
		>>> setor: ForeignKey - Setor da saída
		>>> observacao: TextField - Observação da saída

	Métodos:
	----------
		>>> get_animais: Método que retorna a lista de animais na saída
		>>> get_quantidade_animais: Método que calcula a quantidade de animais na saída
		>>> get_observacao_resumida: Método que retorna uma versão resumida da observação da saída
		>>> __str__: Método que retorna a representação em string da saída
	"""

	class Meta:
		verbose_name = 'Saída'
		verbose_name_plural = 'Saídas'
		ordering = ['data_hora_da_saida']

	TIPOS_DE_SAIDA = [
		('Morte natural', 'Morte natural'),
		('Abate sanitário', 'Abate sanitário'),
		('Descarte', 'Descarte'),
		('Outros', 'Outros')
	]

	data_hora_da_saida = models.DateTimeField(verbose_name='Data e hora da saída')
	tipo = models.CharField(max_length=255, choices=TIPOS_DE_SAIDA, verbose_name='Tipo de saída')
	animais = models.ManyToManyField(Animal, related_name='saida_animais', blank=True, verbose_name='Animais')
	setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, related_name='saida_setor', null=True, blank=True, verbose_name='Setor')
	observacao = models.TextField(null=True, blank=True, verbose_name='Observação')

	def get_animais(self):
		"""
		Método que retorna a lista de animais na saída.
		"""
		return [animal.identificacao_unica for animal in self.animais.all()]

	def get_quantidade_animais(self):
		"""
		Método que calcula a quantidade de animais na saída.
		"""
		return self.animais.count()
	
	def get_observacao_resumida(self):
		"""
		Método que retorna uma versão resumida da observação da saída.
		"""
		if self.observacao:
			return self.observacao[:50] + '...' if len(self.observacao) > 50 else self.observacao
		return ''

	def __str__(self):
		return self.data_hora_da_saida.strftime('%d/%m/%Y às %H:%M')