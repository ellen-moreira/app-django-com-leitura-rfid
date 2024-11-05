from .views import *
from django.urls import path

urlpatterns = [
    path('', index_pecuaria, name='index_pecuaria'),
    path('lote/', lote, name='lote'),
    path('lote/criar/', create_lote, name='criar_lote'),
    path('lote/atualizar/<int:id>/', update_lote, name='atualizar_lote'),
    path('lote/excluir/<int:id>/', delete_lote, name='excluir_lote'),
    path('parto/', parto, name='parto'),
    path('parto/criar/', create_parto, name='criar_parto'),
    path('parto/atualizar/<int:id>/', update_parto, name='atualizar_parto'),
    path('parto/excluir/<int:id>/', delete_parto, name='excluir_parto'),
    path('manejo/', manejo, name='manejo'),
    path('manejo/criar/', create_manejo, name='criar_manejo'),
    path('manejo/atualizar/<int:id>/', update_manejo, name='atualizar_manejo'),
    path('manejo/excluir/<int:id>/', delete_manejo, name='excluir_manejo'),
    path('saida/', saida, name='saida'),
    path('saida/criar/', create_saida, name='criar_saida'),
    path('saida/atualizar/<int:id>/', update_saida, name='atualizar_saida'),
    path('saida/excluir/<int:id>/', delete_saida, name='excluir_saida'),
    path('animal/', animal, name='animal'),
    path('dashboard/', dashboard, name='dashboard'),
    path('gerar_grafico_dinamico/', gerar_grafico_dinamico, name='gerar_grafico_dinamico'),
    # path('logout/', logout_view, name='logout'),
]