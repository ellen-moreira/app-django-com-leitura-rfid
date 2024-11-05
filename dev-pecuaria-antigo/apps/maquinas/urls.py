from django.urls import path
from .views import *

urlpatterns = [
    '''
    path("", index_maquinas, name="index_maquinas"),
    path("controlegeral/", controlegeral, name="controlegeral"),
    path("funcionarios/", funcionarios, name="funcionarios"),
    path("marcas/", marcas, name="marcas"),
    path("modelos/", modelos, name="modelos"),
    path("combustivel/", abastecimento, name="combustivel"),
    path("maquinas/", maquinas, name="maquinas"),
    path("implementos/", implementos, name="implementos"),
    path("categoria_imple/", cat_implementos, name="categoria_imple"),
    path("categoria_produtos/", cat_produtos, name="categoria_produtos"),
    path("produtos/", produtos, name="produtos"),
    path("ferramentas/", ferramentas, name="ferramentas"),
    path("manutencao/", manutencao, name="manutencao"),
    path("gerencia_comb/", ger_combustivel, name="gerencia_comb"),
    path('gerencia_ferramentas/', gerferra, name='gerferra'),
    '''
]