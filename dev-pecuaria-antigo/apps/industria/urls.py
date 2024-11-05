from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index_industria"),
    path("industria/saida_produto/", saida_produto, name="saida_produto"),# type: ignore
    path("industria/ordem_producao/", ordem_producao, name="ordem_producao"),# type: ignore
    path("industria/ordem_producao/create/", create_ordem_producao, name="create_ordem_producao"),# type: ignore
    path("industria/ordem_producao/read/<int:id>/", read_ordem_producao, name="read_ordem_producao"),# type: ignore
    path("industria/ordem_producao/update/<int:id>/", update_ordem_producao, name="update_ordem_producao"),# type: ignore
    path("industria/ordem_producao/delete/<int:id>/", delete_ordem_producao, name="delete_ordem_producao"),# type: ignore
    path('industria/saida_produto/create/', create_saida_produto, name='create_saida_produto'), # type: ignore
    path('industria/saida_produto/read/<int:id>/', read_saida_produto, name='read_saida_produto'),# type: ignore
    path('industria/saida_produto/update/<int:id>/', update_saida_produto, name='update_saida_produto'), # type: ignore
    path('industria/saida_produto/delete/<int:id>/', delete_saida_produto, name='delete_saida_produto'),# type: ignore
    path('industria/entrada_produto/', entrada_produto, name='entrada_produto'),# type: ignore
    path('industria/entrada_produto/create/', create_entrada_produto, name='create_entrada_produto'), # type: ignore
    path('industria/entrada_produto/read/<int:id>/', read_entrada_produto, name='read_entrada_produto'),# type: ignore
    path('industria/entrada_produto/update/<int:id>/', update_entrada_produto, name='update_entrada_produto'), # type: ignore
    path('industria/entrada_produto/delete/<int:id>/', delete_entrada_produto, name='delete_entrada_produto'),# type: ignore
    path('industria/produto/', produto, name='produto'),
]