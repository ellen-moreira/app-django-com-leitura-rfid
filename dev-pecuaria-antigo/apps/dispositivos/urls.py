from django.urls import path
from .views import *

urlpatterns = [
    '''
    path("", index_iot, name="index_iot"),
    path('alocacao/', consulta_alocacao, name='alocacao'),
    path('atuadores/', consulta_atuador, name='atuadores'),
    path('componentes/', consulta_componente, name='componentes'),
    path('dispositivos/', consulta_dispositivo, name = 'dispositivos'),
    path('manutencao/', consulta_manutencao, name = 'manutencao'),
    path('tipo-dispositivo/', consulta_tipo_dispositivo, name = 'tipo-dispositivo'),
    '''
]