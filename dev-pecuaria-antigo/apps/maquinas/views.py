from django.shortcuts import render
from .models import *

'''
def index_maquinas(request):
    context = {}
    return render(request, "index_maquinas.html", context)


def funcionarios(request):
    if request.POST:
        novo_funcionario = Funcionario()
        novo_funcionario.nome = request.POST.get("nome")
        novo_funcionario.cpf = request.POST.get("cpf")
        novo_funcionario.setor = request.POST.get("funcao")
        novo_funcionario.funcao = request.POST.get("setor")
        try:
            novo_funcionario.save()
        except:
            print("Erro de integridade")

    context = {"funcionarios": Funcionario.objects.all()}

    return render(request, "funcionarios/funcionarios.html", context)


def marcas(request):
    if request.POST:
        nova_marca = Marca()
        nova_marca.nome = request.POST.get("nome_marca")
        nova_marca.categoria = request.POST.get("categoria_marca")
        try:
            nova_marca.save()
        except:
            print("Erro de integridade")

    context = {"marcas": Marca.objects.all()}

    return render(request, "marcas/marcas.html", context)


def modelos(request):
    if request.POST:
        novo_modelo = Modelo()
        novo_modelo.categoria = request.POST.get("categoria_modelo")
        try:
            novo_modelo.save()
        except:
            print("Erro de integridade")

    context = {"modelos": Modelo.objects.all()}

    return render(request, "modelos/modelos.html", context)


def ger_combustivel(request):
    if request.POST:
        novo_combustivel = Combustivel()
        novo_combustivel.tipo = request.POST.get("tp_combustivel")
        try:
            novo_combustivel.save()
        except:
            print("Erro de integridade")

    context = {"combustivel": Combustivel.objects.all()}

    return render(request, "gerencia_comb/ger_comb.html", context)


def maquinas(request):
    if request.POST:
        nova_maquina = Maquina()
        nova_maquina.eixos = request.POST.get("eixos")
        nova_maquina.cor = request.POST.get("cor")
        nova_maquina.data_fabricacao = request.POST.get("ano_fab")
        nova_maquina.placa = request.POST.get("placa")
        nova_maquina.chassi = request.POST.get("chassi")
        nova_maquina.potencia_motor = request.POST.get("pot_motor")
        nova_maquina.renavam = request.POST.get("renavam")
        try:
            marca = Marca.objects.get(pk=request.POST.get("marca"))
            modelo = Modelo.objects.get(pk=request.POST.get("modelo"))
            combustivel = Combustivel.objects.get(pk=request.POST.get("tp_comb"))
            nova_maquina.marca = marca
            nova_maquina.modelo = modelo
            nova_maquina.combustivel = combustivel
            nova_maquina.save()
        except Marca.DoesNotExist:
            print("Marca não encontrada")
        except Modelo.DoesNotExist:
            print("Modelo não encontrado")
        except Combustivel.DoesNotExist:
            print("Modelo não encontrado")
        except Exception as e:
            print("Erro de integridade:", e)
    context = {
        "maquinas": Maquina.objects.all(),
        "marcas": Marca.objects.all(),
        "modelos": Modelo.objects.all(),
        "combustiveis": Combustivel.objects.all(),
    }
    return render(request, "maquinas/maquinas.html", context)


def cat_implementos(request):
    if request.POST:
        nova_cat_imple = CategoriaImplemento()
        nova_cat_imple.categoria = request.POST.get("cat_implementos")

        try:
            nova_cat_imple.save()
        except:
            print("Erro de integridade")

    context = {"cat_implementos": CategoriaImplemento.objects.all()}

    return render(request, "categoria_imple/categoria_imple.html", context)


def implementos(request):
    if request.POST:
        novo_implemento = Implemento()
        novo_implemento.nome = request.POST.get("nome")
        novo_implemento.local = request.POST.get("local")
        novo_implemento.quantidade = request.POST.get("quant")
        try:
            marca = Marca.objects.get(pk=request.POST.get("marca"))
            categoria = CategoriaImplemento.objects.get(pk=request.POST.get("categoria"))
            novo_implemento.marca = marca
            novo_implemento.categoria = categoria
            novo_implemento.save()
        except Marca.DoesNotExist:
            print("Marca não encontrada")
        except CategoriaImplemento.DoesNotExist:
            print("Modelo não encontrado")
        except Exception as e:
            print("Erro de integridade:", e)
    implementos = {
        "implementos": Implemento.objects.all(),
        "marca": Marca.objects.all(),
        "cat_implementos": CategoriaImplemento.objects.all(),
    }
    return render(request, "implementos/implementos.html", implementos)


def cat_produtos(request):
    if request.POST:
        nova_cat_produto = CategoriaProduto()
        nova_cat_produto.categoria_produto = request.POST.get("cat_produto")
        try:
            nova_cat_produto.save()
        except:
            print("Erro de integridade")

    context = {"cat_produtos": CategoriaProduto.objects.all()}

    return render(request, "categoria_produtos/categoria_produtos.html", context)


def produtos(request):
    if request.POST:
        novo_produto = Produto()
        novo_produto.nome = request.POST.get("nome")
        novo_produto.quantidade = request.POST.get("quant")
        novo_produto.uso = request.POST.get("uso")
        try:
            categoria = CategoriaProduto.objects.get(pk=request.POST.get("categoria"))
            marca = Marca.objects.get(pk=request.POST.get("marca"))
            novo_produto.categoria = categoria
            novo_produto.marca = marca
            novo_produto.save()
        except Marca.DoesNotExist:
            print("Marca não encontrada")
        except CategoriaProduto.DoesNotExist:
            print("Modelo não encontrado")
        except Maquina.DoesNotExist:
            print("Modelo não encontrado")
        except Exception as e:
            print("Erro de integridade:", e)
    context = {
        "produtos": Produto.objects.all(),
        "marca": Marca.objects.all(),
        "cat_produtos": CategoriaProduto.objects.all(),
        "maquinas": Maquina.objects.all(),
    }
    return render(request, "produtos/produtos.html", context)


def gerferra(request):
    if request.POST:
        nova_ferramenta = Ferramenta()
        nova_ferramenta.nome = request.POST.get("ferramentas")
        nova_ferramenta.quantidade = request.POST.get("quantF")
        nova_ferramenta.local = request.POST.get("localF")
        try:
            nova_ferramenta.save()
        except:
            print("Erro de integridade")
    context = {"gerferra": Ferramenta.objects.all()}

    return render(request, "gerencia_ferramentas/ger_fer.html", context)


def ferramentas(request):
    if request.POST:
        nova_ferramenta = ControleFerramenta()
        nova_ferramenta.data_inicio = request.POST.get("data_inicio")
        nova_ferramenta.hora_inicio = request.POST.get("hora_inicio")
        nova_ferramenta.data_termino = request.POST.get("data_termino")
        nova_ferramenta.hora_termino = request.POST.get("hora_termino")
        nova_ferramenta.quantidade = request.POST.get("quant")
        nova_ferramenta.local = request.POST.get("local")
        nova_ferramenta.motivo = request.POST.get("motivo")
        try:
            ferramentaaa = Ferramenta.objects.get(pk=request.POST.get("ferramenta"))
            funcionario = Funcionario.objects.get(pk=request.POST.get("Funcionario"))
            nova_ferramenta.ferramenta = ferramentaaa
            nova_ferramenta.funcionario = funcionario
            nova_ferramenta.save()
        except Ferramenta.DoesNotExist:
            print("Ferramenta não encontrada")
        except Funcionario.DoesNotExist:
            print("Funcionario não encontrado")
        except Exception as e:
            print("Erro de integridade:", e)
    context = {
        "ferramentaaa": Ferramenta.objects.all(),
        "Funcionario": Funcionario.objects.all(),
        "ferramentas": ControleFerramenta.objects.all(),
    }
    return render(request, "ferramentas/ferramentas.html", context)


def manutencao(request):
    if request.POST:
        nova_manutencao = Manutencao()
        nova_manutencao.descricao = request.POST.get("problema")
        nova_manutencao.tipo = request.POST.get("tipo")
        nova_manutencao.data = request.POST.get("data_realizacao")
        nova_manutencao.materiais_usados = request.POST.get("materiais_usados")
        nova_manutencao.resultado = request.POST.get("resultado")
        try:
            veiculo = Maquina.objects.get(pk=request.POST.get("veiculo"))
            nova_manutencao.veiculo = veiculo
            nova_manutencao.save()
        except Maquina.DoesNotExist:
            print("Máquina não encontrada")
        except Exception as e:
            print("Erro de integridade:", e)
    context = {
        "manutencao": Manutencao.objects.all(),
        "maquinas": Maquina.objects.all(),
    }

    return render(request, "manutencao/manutencao.html", context)


# Refatorado só daqui pra baixo, o resto eu só adaptei - Caio


def abastecimento(request):
    if request.POST:
        novo_registro = AbastecimentoCombustivel()
        novo_registro.data = request.POST.get("data")
        novo_registro.hora = request.POST.get("hora")
        novo_registro.quantidade = request.POST.get("quantidade")
        novo_registro.observacao = request.POST.get("motivo")
        try:
            veiculo = Maquina.objects.get(pk=request.POST.get("maquina_veiculo"))
            funcionario = Funcionario.objects.get(pk=request.POST.get("funcionario"))
            novo_registro.maquina_veiculo = veiculo
            novo_registro.funcionario = funcionario
            novo_registro.save()
        except Maquina.DoesNotExist:
            print("Máquina não encontrada")
        except Funcionario.DoesNotExist:
            print("Funcionario não encontrado")
        except Exception as e:
            print("Erro de integridade:", e)
    context = {
        "combustiveis": AbastecimentoCombustivel.objects.all(),
        "manutencao": Manutencao.objects.all(),
        "maquinas": Maquina.objects.all(),
        "funcionario": Funcionario.objects.all(),
    }

    return render(request, "combustivel/combustivel.html", context)


def controlegeral(request):
    if request.method == "POST":
        novo_registro = ControleGeral()
        novo_registro.funcionario = Funcionario.objects.get(
            pk=request.POST.get("funcionario")
        )
        novo_registro.descricao = request.POST.get("descricao")
        novo_registro.veiculo = Maquina.objects.get(pk=request.POST.get("veiculo"))
        novo_registro.implementos = Implemento.objects.get(
            pk=request.POST.get("implementos")
        )
        novo_registro.data_inicio = request.POST.get("quantidade")
        novo_registro.local = request.POST.get("local")
        novo_registro.data_inicio = request.POST.get("data_inicio")
        novo_registro.hora_inicio = request.POST.get("hora_inicio")
        novo_registro.data_termino = request.POST.get("data_termino")
        novo_registro.hora_termino = request.POST.get("hora_termino")

        try:
            novo_registro.save()
        except Exception as e:
            print("Erro ao salvar:", e)

    context = {
        "controlegeral": ControleGeral.objects.all(),
        "funcionarios": Funcionario.objects.all(),
        "maquinas": Maquina.objects.all(),
        "implementos": Implemento.objects.all(),
    }

    return render(request, "controlegeral/controlegeral.html", context)
'''