from django.shortcuts import render
from .models import *

'''
def index_iot(request):
    context = {}
    return render(request, 'index_iot.html', context)

def consulta_componente(request):
    componentes = {
        'componentes': Componente.objects.all()
    }
    return render(request,'componentes/componentes.html', componentes)

def consulta_dispositivo(request):
    dispositivos = {
        'dispositivos': Dispositivo.objects.all()
    }
    return render(request, 'dispositivos/dispositivos.html', dispositivos)

def consulta_atuador(request):
    atuadores = {
        'atuadores': Atuador.objects.all()
    }
    return render(request, 'atuadores/atuadores.html', atuadores)

def consulta_alocacao(request):
    dispositivos = Dispositivo.objects.all()
    alocacao = Alocacao_dispositivo.objects.all()

    return render(request, 'alocacao/alocacao.html', {'dispositivos': dispositivos, 'alocacao': alocacao})

def consulta_manutencao(request):
    manutencoes = Manutencao.objects.all()
    dispositivos = Dispositivo.objects.all()
    context = {'manutencoes': manutencoes}
    return render(request, 'manutencao/manutencao.html', {'dispositivos': dispositivos, 'manutencoes': manutencoes})

def consulta_tipo_dispositivo(request):
    tipo_dispositivo = {
        'tipo_dispositivo': Tipo_dispositivo.objects.all()
    }
    return render(request, 'tipo-dispositivo/tipo_dispositivo.html',tipo_dispositivo)
'''