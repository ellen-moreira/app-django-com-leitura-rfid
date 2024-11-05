from django.contrib import admin
from .models import *

class ReceitaItemInline(admin.TabularInline):
    model = ReceitaItem
    extra = 1

class EtapaProducaoInline(admin.TabularInline):
    model = EtapaProducao
    extra = 1

class ReceitaAdmin(admin.ModelAdmin):
    inlines = [ReceitaItemInline, EtapaProducaoInline]


class ProducaoFuncionarioInline(admin.TabularInline):
    model = ProducaoFuncionario
    extra = 1
    
class OrdemProducaoProdutoInline(admin.TabularInline):
    model = OrdemProducaoProduto
    extra = 1

class EntradaProdutoItemInline(admin.TabularInline):
    model = EntradaProdutoItem
    extra = 1

class SaidaProdutoItemInline(admin.TabularInline):
    model = SaidaProdutoItem
    extra = 1

class OrdemProducaoAdmin(admin.ModelAdmin):
    inlines = [OrdemProducaoProdutoInline]

class ExecucaoEtapaAdmin(admin.ModelAdmin):
    inlines = [ProducaoFuncionarioInline]

class EntradaProdutoAdmin(admin.ModelAdmin):
    inlines = [EntradaProdutoItemInline]

class SaidaProdutoAdmin(admin.ModelAdmin):
    inlines = [SaidaProdutoItemInline]

admin.site.register(Funcionario)
admin.site.register(GrupoCategoria)
admin.site.register(SubgrupoSubcategoria)
admin.site.register(Marca)
admin.site.register(Fabricante)
admin.site.register(Tipo)
admin.site.register(UnidadeMedida)
admin.site.register(Produto)
admin.site.register(EtapaProducao)
admin.site.register(AtividadeServico)
admin.site.register(Receita, ReceitaAdmin)
admin.site.register(ExecucaoEtapa, ExecucaoEtapaAdmin)
admin.site.register(OrdemProducao, OrdemProducaoAdmin)
admin.site.register(TipoTransacao)
admin.site.register(EntradaProduto, EntradaProdutoAdmin)
admin.site.register(SaidaProduto, SaidaProdutoAdmin)
admin.site.register(TesteQualidade)