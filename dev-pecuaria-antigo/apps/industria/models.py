from django.db import models

class Funcionario(models.Model):
    nome_funcionario = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_funcionario

class GrupoCategoria(models.Model):
    nome_grupo_categoria = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_grupo_categoria

class SubgrupoSubcategoria(models.Model):
    nome_subgrupo_subcategoria = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_subgrupo_subcategoria
    
class Marca(models.Model):
    nome_marca = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_marca

class Fabricante(models.Model):
    razao_social = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.razao_social} - {self.nome_fantasia}"
    
class Tipo(models.Model):
    nome_tipo = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_tipo

class UnidadeMedida(models.Model):
    nome_unidade_medida = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.nome_unidade_medida

class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    qtde_por_embalagem = models.IntegerField()
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoCategoria, on_delete=models.CASCADE)
    subgrupo = models.ForeignKey(SubgrupoSubcategoria, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    qtde_atual = models.IntegerField()
    def __str__(self):
        return self.nome_produto

class Receita(models.Model):
    nome_receita = models.ForeignKey(Produto, on_delete=models.CASCADE, limit_choices_to={'tipo__nome_tipo': 'ProdutoAcabado'})
    data_hora_registro = models.DateTimeField()
    detalhamento = models.TextField()
    def __str__(self):
        return self.nome_receita

class ReceitaItem(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, limit_choices_to={'tipo__nome_tipo': 'Ingrediente'})
    quantidade = models.IntegerField()
    nome_unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.SET_NULL, null=True, blank=True)

class AtividadeServico(models.Model):
    atividade_servico = models.CharField(max_length=100)
    def __str__(self):
        return self.atividade_servico
    
class EtapaProducao(models.Model):
    atividade_servico = models.ForeignKey(AtividadeServico, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    detalhes = models.TextField()

class OrdemProducao(models.Model):
    funcionario_emitiu_ordem = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    
class OrdemProducaoProduto(models.Model): 
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

class ExecucaoEtapa(models.Model):
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE)

class ProducaoFuncionario(models.Model):
    execucao = models.ForeignKey(ExecucaoEtapa, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    etapa_producao = models.ForeignKey(EtapaProducao, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data_hora_inicio = models.DateTimeField()
    data_hora_termino = models.DateTimeField()

class OrdemProducaoEtapa(models.Model):
    funcionario_etapa = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE)
    data_hora_inicio = models.DateTimeField()
    data_hora_termino = models.DateTimeField()

class TipoTransacao(models.Model):
    nome_transacao = models.CharField(max_length=100)
    tipo_entrada_ou_saida = models.CharField(max_length=10)

class EntradaProduto(models.Model):
    data_hora = models.DateTimeField()
    fornecedor = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    num_nota = models.CharField(max_length=100)
    tipo_transacao = models.ForeignKey(TipoTransacao, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

class EntradaProdutoItem(models.Model):
    entrada = models.ForeignKey(EntradaProduto, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)

class SaidaProduto(models.Model):
    data_hora = models.DateTimeField()
    destinatario = models.CharField(max_length=100)
    num_nota = models.CharField(max_length=100)
    tipo_transacao = models.ForeignKey(TipoTransacao, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

class SaidaProdutoItem(models.Model):
    saida = models.ForeignKey(SaidaProduto, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

class TesteQualidade(models.Model):
    teste_qualidade = models.CharField(max_length=100)

class TesteQualidadeItem(models.Model):
    teste_qualidade = models.ForeignKey(TesteQualidade, on_delete=models.CASCADE)