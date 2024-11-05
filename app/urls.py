from app.views import *
from django.urls import path

app_name = 'pecuaria'

urlpatterns = [
    path('erro/', error_page, name='error_page'), # Rota para página de erro
    path('criar-conta/', create_account, name='create_account'), # Rota para criar conta
    path('entrar/', login_view, name='login'), # Rota para login
    path('sair/', logout_view, name='logout'), # Rota para logout
    path('', home, name='home'), # Rota para home
    path('lotes/', lotes, name='lotes'), # Rota para página de visualização de lotes
    path('lote/cadastrar/', cadastrar_lote, name='cadastrar_lote'), # Rota para página de cadastro de lotes
    path('lote/atualizar/<int:id>/', atualizar_lote, name='atualizar_lote'), # Rota para página de atualização de lotes
    path('lote/excluir/<int:id>/', excluir_lote, name='excluir_lote'), # Rota que permite excluir um lote
    path('partos/', partos, name='partos'), # Rota para página de visualização de partos
    path('parto/cadastrar/', cadastrar_parto, name='cadastrar_parto'), # Rota para página de cadastro de partos
    path('parto/atualizar/<int:id>/', atualizar_parto, name='atualizar_parto'), # Rota para página de atualização de partos
    path('parto/excluir/<int:id>/', excluir_parto, name='excluir_parto'), # Rota que permite excluir um parto
    path('manejos/', manejos, name='manejos'), # Rota para página de visualização de manejos
    path('manejo/cadastrar/', cadastrar_manejo, name='cadastrar_manejo'), # Rota para página de cadastro de manejos
    path('manejo/atualizar/<int:id>/', atualizar_manejo, name='atualizar_manejo'), # Rota para página de atualização de manejos
    path('manejo/excluir/<int:id>/', excluir_manejo, name='excluir_manejo'), # Rota que permite excluir um manejo
    path('saidas/', saidas, name='saidas'), # Rota para página de visualização de saídas
    path('saida/cadastrar/', cadastrar_saida, name='cadastrar_saida'), # Rota para página de cadastro de saídas
    path('saida/atualizar/<int:id>/', atualizar_saida, name='atualizar_saida'), # Rota para página de atualização de saídas
    path('saida/excluir/<int:id>/', excluir_saida, name='excluir_saida'), # Rota que permite excluir uma saída
    path('animais/', animais, name='animais'), # Rota para página de visualização de animais
    path('animal/', animal_info, name='animal_info'), # Rota para página de visualização das informações de um animal via RFID

    path('api/animal/<str:rfid>/', get_animal, name='get_animal'), # Rota para comunicar com o ESP 8266
    path('api/latest-animal/', latest_animal, name='latest_animal'), # Rota para retornar o último animal lido
]