from django.db import models

'''
class Funcionario(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    funcao = models.CharField(max_length=50, verbose_name="Função")
    setor = models.CharField(max_length=50, verbose_name="Setor")

    class Meta:
        ordering = ["cpf"]
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome


class Marca(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome")
    categoria = models.CharField(max_length=50, verbose_name="Categoria")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nome


class Modelo(models.Model):
    categoria = models.CharField(max_length=50, unique=True, verbose_name="Categoria")

    class Meta:
        ordering = ["categoria"]
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"

    def __str__(self):
        return self.categoria


class CategoriaImplemento(models.Model):
    categoria = models.CharField(max_length=50, unique=True, verbose_name="Categoria")

    class Meta:
        ordering = ["categoria"]
        verbose_name = "Categoria de Implemento"
        verbose_name_plural = "Categorias de Implementos"

    def __str__(self):
        return self.categoria


class CategoriaProduto(models.Model):
    categoria = models.CharField(max_length=50, unique=True, verbose_name="Categoria")

    class Meta:
        ordering = ["categoria"]
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produtos"

    def __str__(self):
        return self.categoria


class Combustivel(models.Model):
    tipo = models.CharField(max_length=100, unique=True, verbose_name="Tipo")

    class Meta:
        ordering = ["tipo"]
        verbose_name = "Combustível"
        verbose_name_plural = "Combustíveis"

    def __str__(self):
        return self.tipo


class Maquina(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name="Marca")
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, verbose_name="Modelo")
    eixos = models.CharField(max_length=50, verbose_name="Nº de Eixos")
    cor = models.CharField(max_length=50, verbose_name="Cor")
    data_fabricacao = models.DateField(verbose_name="Data de Fabricacao")
    placa = models.CharField(max_length=50, unique=True, verbose_name="Placa")
    chassi = models.CharField(max_length=50, unique=True, verbose_name="Chassi")
    potencia_motor = models.CharField(max_length=50, verbose_name="Potencia do Motor")
    renavam = models.CharField(max_length=50, verbose_name="Código Renavam")
    combustivel = models.ForeignKey(Combustivel, on_delete=models.CASCADE, verbose_name="Combustivel Utilizado")

    class Meta:
        ordering = ["modelo"]
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"

    def __str__(self):
        return f"{self.marca} {self.modelo}"


class Local(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Local"
        verbose_name_plural = "Locais"

    def __str__(self):
        return self.nome


class Implemento(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name="Marca")
    categoria = models.ForeignKey(CategoriaImplemento, on_delete=models.CASCADE, verbose_name="Categoria")
    quantidade = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Quantidade")
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name="Local")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Implemento"
        verbose_name_plural = "Implementos"

    def __str__(self):
        return self.nome


class AbastecimentoCombustivel(models.Model):
    data = models.DateField(verbose_name="Data de Abastecimento")
    hora = models.TimeField(verbose_name="Hora de Abastecimento")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, verbose_name="Funcionário")
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, verbose_name="Maquina")
    quantidade = models.CharField(max_length=50, verbose_name="Quantidade")
    observacao = models.CharField(max_length=50, verbose_name="Observacao")

    class Meta:
        ordering = ["data"]
        verbose_name = "Abastecimento de Combustível"
        verbose_name_plural = "Abastecimentos de Combustível"

    def __str__(self):
        return f"{self.data} - {self.maquina.marca} {self.maquina.modelo}"


class Ferramenta(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Ferramenta")
    quantidade = models.CharField(max_length=50, verbose_name="Quantidade")
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name="Local")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Ferramentas"
        verbose_name_plural = "Ferramentas"

    def __str__(self):
        return self.nome


class ControleFerramenta(models.Model):
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.CASCADE, verbose_name="Ferramenta")
    quantidade = models.CharField(max_length=50, verbose_name="Quantidade")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, verbose_name="Funcionário")
    data_inicio = models.DateField(verbose_name="Data Início")
    hora_inicio = models.TimeField(verbose_name="Hora Início")
    data_termino = models.DateField(verbose_name="Data Término")
    hora_termino = models.TimeField(verbose_name="Hora Término")
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name="Local")
    motivo = models.CharField(max_length=50, verbose_name="Motivo")

    class Meta:
        ordering = ["data_inicio"]
        verbose_name = "Controle de Ferramenta"
        verbose_name_plural = "Controle de Ferramentas"

    def __str__(self):
        return (
            f"{self.ferramenta.nome} - DE: {self.data_inicio} ATÉ: {self.data_termino}"
        )


class Produto(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome")
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE, verbose_name="Categoria")
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name="Marca")
    quantidade = models.CharField(max_length=50, verbose_name="Quantidade")
    uso = models.CharField(max_length=50, verbose_name="Uso")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome


class Manutencao(models.Model):
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    tipo = models.CharField(max_length=100, verbose_name="Tipo")
    veiculo = models.ForeignKey(Maquina, on_delete=models.CASCADE, verbose_name="Veiculo")
    data = models.DateField(verbose_name="Data da Manutenção")
    materiais_usados = models.CharField(max_length=100, verbose_name="Materiais Utilizados")
    resultado = models.CharField(max_length=100, verbose_name="Resultado")

    class Meta:
        ordering = ["data"]
        verbose_name = "Manutenção"
        verbose_name_plural = "Manutenções"

    def __str__(self):
        return f"{self.veiculo.marca} {self.veiculo.modelo} - {self.data}"


class ControleGeral(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, verbose_name="Funcionário")
    descricao = models.CharField(max_length=50, verbose_name="Descrição")
    veiculo = models.ForeignKey(Maquina, on_delete=models.CASCADE, verbose_name="Veiculo")
    implementos = models.ForeignKey(Implemento, on_delete=models.CASCADE, default=None, verbose_name="Implemento")
    quantidade = models.CharField(max_length=50, verbose_name="Quantidade de Imp.")
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name="Local")
    data_inicio = models.DateField(verbose_name="Data Início")
    hora_inicio = models.TimeField(verbose_name="Hora Início")
    data_termino = models.DateField(verbose_name="Data Término")
    hora_termino = models.TimeField(verbose_name="Hora Término")

    class Meta:
        ordering = ["data_inicio"]
        verbose_name = "Controle Geral"
        verbose_name_plural = "Controle Geral"

    def __str__(self):
        return f"{self.descricao}"
'''