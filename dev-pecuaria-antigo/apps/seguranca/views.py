from django.shortcuts import render, redirect
from .models import Ronda, Ocorrencia
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import Local

def is_seguranca_member(user):
    return user.groups.filter(name='Seguranca').exists() or user.is_superuser

@login_required
@user_passes_test(is_seguranca_member)
def index_seguranca(request):
    context = {}
    return render(request, 'index_seguranca.html', context)

def index_seguranca(request):
    locais = Local.objects.all()
    ronda_andamento = Ronda.objects.filter(status='Andamento').first()
    hora_inicio = None

    if ronda_andamento:
        hora_inicio = ronda_andamento.hora_inicio.strftime("%H:%M:%S")  # Formatação para exibir apenas a hora:minuto:segundo
        return render(request, 'index_seguranca.html', {'ronda_andamento': ronda_andamento, 'locais': locais, 'hora_inicio': hora_inicio})
    else:
        return render(request, 'index_seguranca.html', {'sem_ronda_andamento': True})


def iniciar_ronda(request):
    # Verifica se já existe uma ronda em andamento
    ronda_em_andamento = Ronda.objects.filter(status='Andamento').first()
    
    if ronda_em_andamento:
        # Se já houver uma ronda em andamento, retorna um erro ou uma mensagem indicando isso
        return JsonResponse({'message': 'Já existe uma ronda em andamento.'}, status=400)
    else:
        # Se não houver uma ronda em andamento, cria uma nova ronda e redireciona para a página inicial
        Ronda.objects.create(hora_inicio=timezone.now(), status='Andamento')
        return redirect('index_seguranca')
    
def encerrar_ronda(request):
    # Busca a ronda em andamento, se existir
    ronda_andamento = Ronda.objects.filter(status='Andamento').first()
    
    if ronda_andamento:
        # Atualiza a hora de encerramento e o status da ronda
        ronda_andamento.hora_encerramento = timezone.now()
        ronda_andamento.status = 'Encerrada'
        ronda_andamento.save()
        
    # Redireciona de volta para a página inicial após encerrar a ronda
    return redirect('index_seguranca')

from django.shortcuts import get_object_or_404

from .models import Ocorrencia, Ronda

def registrar_ocorrencia(request):
    if request.method == 'POST':
        local_id = request.POST.get('local')  # Obtém o ID do local selecionado no formulário
        texto_ocorrencia = request.POST.get('descricao')  # Obtém a descrição da ocorrência
        
        local = get_object_or_404(Local, id=local_id)  # Obtém o objeto Local com base no ID enviado
        
        # Busca a ronda em andamento, se existir
        ronda_andamento = Ronda.objects.filter(status='Andamento').first()
        
        if ronda_andamento:
            # Cria uma nova instância de Ocorrencia associada à ronda em andamento
            nova_ocorrencia = Ocorrencia.objects.create(
                ronda=ronda_andamento,
                local=local,
                texto_ocorrencia=texto_ocorrencia,
                horario=timezone.now()  # Define o horário da ocorrência como o momento atual
            )
            return redirect('index_seguranca')
        else:
            return JsonResponse({'error': 'Não há ronda em andamento para registrar a ocorrência.'}, status=400)

    # Caso não seja uma requisição POST, retorne um erro
    return JsonResponse({'error': 'Método não permitido'}, status=405)


