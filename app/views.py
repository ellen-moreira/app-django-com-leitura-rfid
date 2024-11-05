from app.decorators import *
from app.forms import *
from app.models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.

# Função que renderiza a página de erro
def error_page(request):
    # Pega o status code da sessão ou 500
    status_code = request.session.get('status_code', 500)

    # Pega a mensagem da sessão ou 'Ocorreu um erro inesperado.'
    message = request.session.get('message', 'Ocorreu um erro inesperado.')

    # Remove o status code da sessão
    request.session.pop('status_code', None)

    # Remove a mensagem da sessão
    request.session.pop('message', None)

    # Contexto que será passado para a página de erro
    context = {
        'status_code': status_code,
        'message': message
    }

    # Renderiza a página de erro
    return render(request, 'pages/error_page.html', context)

# Função que permite criar uma conta
def create_account(request):
    if request.method == 'GET':
        form = UserCreationForm() # Renderiza um formulário de criação de usuário
    elif request.method == 'POST':
        # Renderiza um formulário de criação de usuário com os dados do POST
        form = UserCreationForm(request.POST)

        # Verifica se os campos de usuário, senha e confirmação de senha estão preenchidos
        if not request.POST.get('username') or not request.POST.get('password1') or not request.POST.get('password2'):
            # Adiciona uma mensagem de erro na sessão
            messages.error(request, 'Preencha todos os campos.')
            
            # Redireciona para a página de criação de conta
            return redirect('pecuaria:create_account')
        
        # Verifica se o usuário já existe
        user = User.objects.filter(username=request.POST.get('username'))

        # Se o usuário já existe
        if user:
            # Adiciona uma mensagem de erro na sessão
            messages.error(request, 'Usuário já existe.')

            # Redireciona para a página de criação de conta
            return redirect('pecuaria:create_account')
        
        # Verifica se o formulário é válido
        if form.is_valid():
            # Salva o usuário
            form.save()

            # Adiciona uma mensagem de sucesso na sessão
            messages.success(request, 'Usuário cadastrado com sucesso.')

            # Redireciona para a página de login
            return redirect('pecuaria:login')
        else:
            # Adiciona uma mensagem de erro na sessão
            messages.error(request, 'Erro ao cadastrar usuário.')

            # Redireciona para a página de criação de conta
            return redirect('pecuaria:create_account')
    
    # Contexto que será passado para a página de criação de conta
    context = {
        'form': form
    }

    # Renderiza a página de criação de conta
    return render(request, 'pages/create_account.html', context)

# Função que permite logar um usuário
def login_view(request):
    if request.method == 'GET':
        # Renderiza um formulário de autenticação
        form = AuthenticationForm()
    elif request.method == 'POST':
        # Renderiza um formulário de autenticação com os dados do POST
        form = AuthenticationForm(request, request.POST)

        # Verifica se os campos de usuário e senha estão preenchidos
        if not request.POST.get('username') or not request.POST.get('password'):
            # Adiciona uma mensagem de erro na sessão
            messages.error(request, 'Preencha todos os campos.')

            # Redireciona para a página de login
            return redirect('pecuaria:login')
        
        # Verifica se o formulário é válido
        if form.is_valid():
            # Autentica o usuário
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
            
            # Se o usuário existe
            if user:
                # Loga o usuário
                login(request, user)

                # Adiciona uma mensagem de sucesso na sessão
                messages.success(request, 'Usuário logado com sucesso.')

                # Redireciona para a página inicial
                return redirect('pecuaria:home')
            else:
                # Adiciona uma mensagem de erro na sessão
                messages.error(request, 'Usuário ou senha inválidos.')

                # Redireciona para a página de login
                return redirect('pecuaria:login')

    # Contexto que será passado para a página de login
    context = {
        'form': form
    }

    # Renderiza a página de login
    return render(request, 'pages/login.html', context)

# Função que permite deslogar um usuário
def logout_view(request):
    # Se o usuário está autenticado
    if request.user.is_authenticated:
        # Desloga o usuário
        logout(request)

        # Adiciona uma mensagem de sucesso na sessão
        messages.success(request, 'Usuário deslogado com sucesso.')

    # Redireciona para a página de login
    return redirect('pecuaria:login')

# Função que renderiza a página inicial
def home(request):
    # Contexto que será passado para a página inicial
    context = {
        'user': request.user
    }

    # Renderiza a página inicial
    return render(request, 'pages/home.html', context)

# Função que renderiza a página de visualização de lotes
@login_required(login_url=reverse_lazy('pecuaria:login')) # Restringe o acesso à página de lotes para usuários autenticados
@restringir_acesso(['Suinocultura']) # Restringe o acesso à página de lotes para usuários do setor de suinocultura
@filtrar_lotes_por_setor # Filtra os lotes do setor do usuário autenticado
def lotes(request, lotes):
    # Contexto que será passado para a página de lotes
    context = {
        'lotes': lotes
    }

    # Renderiza a página de lotes
    return render(request, 'pages/batches.html', context)

# Função que permite cadastrar um lote
@login_required(login_url=reverse_lazy('pecuaria:login')) # Restringe o acesso à página de cadastro de lotes para usuários autenticados
@restringir_acesso(['Suinocultura']) # Restringe o acesso à página de cadastro de lotes para usuários do setor de suinocultura
def cadastrar_lote(request):
    if request.method == 'GET':
        # Renderiza um formulário de lote
        lote_form = LoteForm()

        # Renderiza um formulário de animal passando o usuário autenticado como argumento
        animal_formset = CadastrarLoteAnimalFormSet(user=request.user)
    elif request.method == 'POST':
        # Renderiza um formulário de lote com os dados do POST
        lote_form = LoteForm(request.POST)

        # Renderiza um formulário de animal com os dados do POST e o usuário autenticado como argumento
        animal_formset = CadastrarLoteAnimalFormSet(request.POST, user=request.user)

        # Verifica se o formulário de lote e o formulário de animal são válidos
        if lote_form.is_valid() and animal_formset.is_valid():
            # Salva o lote sem commit
            lote = lote_form.save(commit=False)

            # Define o setor do lote como o setor do usuário autenticado
            lote.setor = request.user.setor_usuarios.first()
            
            # Salva o lote
            lote.save()
            
            # Define o lote do formulário de animal como o lote salvo
            animal_formset.instance = lote

            # Salva o formulário de animal
            animal_formset.save()

            # Adiciona uma mensagem de sucesso na sessão
            messages.success(request, 'Lote cadastrado com sucesso!')

            # Redireciona para a página de lotes
            return redirect('pecuaria:lotes')
        else:
            # Adiciona uma mensagem de erro na sessão
            messages.error(request, 'Erro ao cadastrar lote!')

    # Contexto que será passado para a página de cadastro de lote
    context = {
        'lote_form': lote_form,
        'animal_formset': animal_formset,
    }

    # Renderiza a página de cadastro de lote
    return render(request, 'pages/create_update_batch.html', context)

# Função que permite atualizar um lote
@login_required(login_url=reverse_lazy('pecuaria:login')) # Restringe o acesso à página de atualização de lotes para usuários autenticados
@restringir_acesso(['Suinocultura']) # Restringe o acesso à página de atualização de lotes para usuários do setor de suinocultura
def atualizar_lote(request, id):
    # Pega o lote com o id passado na URL
    lote = get_object_or_404(Lote, id=id)

    if request.method == 'GET':
        # Renderiza um formulário de lote com o lote pego
        lote_form = LoteForm(instance=lote)

        # Renderiza um formulário de animal com o lote pego e o usuário autenticado como argumento
        animal_formset = AtualizarLoteAnimalFormSet(instance=lote, user=request.user)
    elif request.method == 'POST':
        # Renderiza um formulário de lote com os dados do POST e o lote pego
        lote_form = LoteForm(request.POST, instance=lote)

        # Renderiza um formulário de animal com os dados do POST, o lote pego e o usuário autenticado como argumento
        animal_formset = AtualizarLoteAnimalFormSet(request.POST, instance=lote, user=request.user)

        # Verifica se o formulário de lote e o formulário de animal são válidos
        if lote_form.is_valid() and animal_formset.is_valid():
            # Salva o lote sem commit
            lote = lote_form.save(commit=False)

            # Define o setor do lote como o setor do usuário autenticado
            lote.setor = request.user.setor_usuarios.first()

            # Salva o lote
            lote.save()

            # Define o lote do formulário de animal como o lote salvo
            animal_formset.instance = lote

            # Salva o formulário de animal
            animal_formset.save()

            # Adiciona uma mensagem de sucesso na sessão
            messages.success(request, 'Lote atualizado com sucesso!')

            # Redireciona para a página de lotes
            return redirect('pecuaria:lotes')
        else:
            # Adiciona uma mensagem de erro na sessão
            messages.error(request, 'Erro ao atualizar lote!')

    # Contexto que será passado para a página de atualização de lote
    context = {
        'lote_form': lote_form,
        'animal_formset': animal_formset,
    }

    # Renderiza a página de atualização de lote
    return render(request, 'pages/create_update_batch.html', context)

# Função que permite excluir um lote
@login_required(login_url=reverse_lazy('pecuaria:login')) # Restringe o acesso à página de excluir lotes para usuários autenticados
@restringir_acesso(['Suinocultura']) # Restringe o acesso à página de excluir lotes para usuários do setor de suinocultura
def excluir_lote(request, id):
    # Pega o lote com o id passado na URL
    lote = get_object_or_404(Lote, id=id)

    # Exclui o lote
    lote.delete()

    # Adiciona uma mensagem de sucesso na sessão
    messages.success(request, 'Lote excluído com sucesso!')

    # Redireciona para a página de lotes
    return redirect('pecuaria:lotes')

@login_required(login_url=reverse_lazy('pecuaria:login'))
@filtrar_partos_por_setor
def partos(request, partos):
    context = {
        'partos': partos
    }

    return render(request, 'pages/births.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def cadastrar_parto(request):
    SETORES_FORMSETS = {
        'Suinocultura': CadastrarPartoSuinoFormSet,
        'Bovinocultura de Corte': CadastrarPartoBovinoCorteFormSet,
        'Bovinocultura de Leite': CadastrarPartoBovinoLeiteFormSet,
    }

    setor_usuario = request.user.setor_usuarios.first()
    AnimalFormset = SETORES_FORMSETS.get(setor_usuario.nome)

    if not AnimalFormset:
        messages.error(request, 'Setor não tem permissão para cadastrar partos!')
        return redirect('pecuaria:partos')
    
    if request.method == 'GET':
        parto_form = PartoForm(user=request.user)
        animal_formset = AnimalFormset()
    elif request.method == 'POST':
        parto_form = PartoForm(request.POST, user=request.user)
        animal_formset = AnimalFormset(request.POST)

        if parto_form.is_valid() and animal_formset.is_valid():
            parto = parto_form.save(commit=False)
            parto.setor = setor_usuario

            parto.save()

            animal_formset.instance = parto

            animal_formset.save()

            messages.success(request, 'Parto cadastrado com sucesso!')

            return redirect('pecuaria:partos')
        else:
            messages.error(request, 'Erro ao cadastrar parto!')

    context = {
        'parto_form': parto_form,
        'animal_formset': animal_formset,
    }

    return render(request, 'pages/create_update_birth.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def atualizar_parto(request, id):
    parto = get_object_or_404(Parto, id=id)

    SETORES_FORMSETS = {
        'Suinocultura': AtualizarPartoSuinoFormSet,
        'Bovinocultura de Corte': AtualizarPartoBovinoCorteFormSet,
        'Bovinocultura de Leite': AtualizarPartoBovinoLeiteFormSet,
    }

    setor_usuario = request.user.setor_usuarios.first()
    AnimalFormset = SETORES_FORMSETS.get(setor_usuario.nome)

    if not AnimalFormset:
        messages.error(request, 'Setor não tem permissão para atualizar partos!')
        return redirect('pecuaria:partos')

    if request.method == 'GET':
        parto_form = PartoForm(instance=parto, user=request.user)
        animal_formset = AnimalFormset(instance=parto)
    elif request.method == 'POST':
        parto_form = PartoForm(request.POST, instance=parto, user=request.user)
        animal_formset = AnimalFormset(request.POST, instance=parto)

        if parto_form.is_valid() and animal_formset.is_valid():
            parto = parto_form.save(commit=False)
            parto.setor = setor_usuario

            parto.save()

            animal_formset.instance = parto

            animal_formset.save()

            messages.success(request, 'Parto atualizado com sucesso!')

            return redirect('pecuaria:partos')
        else:
            messages.error(request, 'Erro ao atualizar parto!')

    context = {
        'parto_form': parto_form,
        'animal_formset': animal_formset,
    }

    return render(request, 'pages/create_update_birth.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def excluir_parto(request, id):
    parto = get_object_or_404(Parto, id=id)

    parto.delete()
    messages.success(request, 'Parto excluído com sucesso!')

    return redirect('pecuaria:partos')

@login_required(login_url=reverse_lazy('pecuaria:login'))
@filtrar_manejos_por_setor
def manejos(request, manejos):
    context = {
        'manejos': manejos
    }

    return render(request, 'pages/handlings.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def cadastrar_manejo(request):
    if request.method == 'GET':
        manejo_form = ManejoForm(user=request.user)
        procedimento_formset = CadastrarProcedimentoManejoFormSet()
        produto_formset = CadastrarProdutoManejoFormSet()
    elif request.method == 'POST':
        manejo_form = ManejoForm(request.POST, user=request.user)
        procedimento_formset = CadastrarProcedimentoManejoFormSet(request.POST)
        produto_formset = CadastrarProdutoManejoFormSet(request.POST)

        if (manejo_form.is_valid() and procedimento_formset.is_valid() and produto_formset.is_valid()):
            manejo = manejo_form.save(commit=False)
            manejo.setor = request.user.setor_usuarios.first()

            manejo.save()

            procedimento_formset.instance = manejo
            produto_formset.instance = manejo

            procedimento_formset.save()
            produto_formset.save()

            messages.success(request, 'Manejo cadastrado com sucesso!')

            return redirect('pecuaria:manejos')
        else:
            messages.error(request, 'Erro ao cadastrar manejo!')

    context = {
        'manejo_form': manejo_form,
        'procedimento_formset': procedimento_formset,
        'produto_formset': produto_formset,
    }

    return render(request, 'pages/create_update_handling.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def atualizar_manejo(request, id):
    manejo = get_object_or_404(Manejo, id=id)

    if request.method == 'GET':
        manejo_form = ManejoForm(instance=manejo, user=request.user)
        procedimento_formset = AtualizarProcedimentoManejoFormSet(instance=manejo)
        produto_formset = AtualizarProdutoManejoFormSet(instance=manejo)
    elif request.method == 'POST':
        manejo_form = ManejoForm(request.POST, instance=manejo, user=request.user)
        procedimento_formset = AtualizarProcedimentoManejoFormSet(request.POST, instance=manejo)
        produto_formset = AtualizarProdutoManejoFormSet(request.POST, instance=manejo)

        if (manejo_form.is_valid() and procedimento_formset.is_valid() and produto_formset.is_valid()):
            manejo = manejo_form.save(commit=False)
            manejo.setor = request.user.setor_usuarios.first()

            manejo.save()

            procedimento_formset.instance = manejo
            produto_formset.instance = manejo

            procedimento_formset.save()
            produto_formset.save()

            messages.success(request, 'Manejo atualizado com sucesso!')

            return redirect('pecuaria:manejos')
        else:
            messages.error(request, 'Erro ao atualizar manejo!')

    context = {
        'manejo_form': manejo_form,
        'procedimento_formset': procedimento_formset,
        'produto_formset': produto_formset,
    }

    return render(request, 'pages/create_update_handling.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def excluir_manejo(request, id):
    manejo = get_object_or_404(Manejo, id=id)

    manejo.delete()
    messages.success(request, 'Manejo excluído com sucesso!')

    return redirect('pecuaria:manejos')

@login_required(login_url=reverse_lazy('pecuaria:login'))
@filtrar_saidas_por_setor
def saidas(request, saidas):
    context = {
        'saidas': saidas
    }

    return render(request, 'pages/outputs.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def cadastrar_saida(request):
    if request.method == 'GET':
        saida_form = SaidaForm(user=request.user)
        animal_formset = CadastrarSaidaFormSet(user=request.user)
    elif request.method == 'POST':
        saida_form = SaidaForm(request.POST, user=request.user)
        animal_formset = CadastrarSaidaFormSet(request.POST, user=request.user)

        if saida_form.is_valid() and animal_formset.is_valid():
            saida = saida_form.save(commit=False)
            saida.setor = request.user.setor_usuarios.first()

            saida.save()

            animal_formset.instance = saida

            animal_formset.save()

            messages.success(request, 'Saída cadastrada com sucesso!')

            return redirect('pecuaria:saidas')
        else:
            messages.error(request, 'Erro ao cadastrar saída!')

    context = {
        'saida_form': saida_form,
        'animal_formset': animal_formset,
    }

    return render(request, 'pages/create_update_output.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def atualizar_saida(request, id):
    saida = get_object_or_404(Saida, id=id)

    if request.method == 'GET':
        saida_form = SaidaForm(instance=saida, user=request.user)
        
        # converta o campo data_hora_da_saida para aparecer no campo de input do tipo datetime-local
        saida_form.fields['data_hora_da_saida'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')

        animal_formset = AtualizarSaidaFormSet(instance=saida, user=request.user)
    elif request.method == 'POST':
        saida_form = SaidaForm(request.POST, instance=saida, user=request.user)
        animal_formset = AtualizarSaidaFormSet(request.POST, instance=saida, user=request.user)

        if saida_form.is_valid() and animal_formset.is_valid():
            saida = saida_form.save(commit=False)
            saida.setor = request.user.setor_usuarios.first()

            saida.save()

            animal_formset.instance = saida

            animal_formset.save()

            messages.success(request, 'Saída atualizada com sucesso!')

            return redirect('pecuaria:saidas')
        else:
            messages.error(request, 'Erro ao atualizar saída!')

    context = {
        'saida_form': saida_form,
        'animal_formset': animal_formset,
    }

    return render(request, 'pages/create_update_output.html', context)

@login_required(login_url=reverse_lazy('pecuaria:login'))
def excluir_saida(request, id):
    saida = get_object_or_404(Saida, id=id)

    saida.delete()
    messages.success(request, 'Saída excluída com sucesso!')

    return redirect('pecuaria:saidas')

@login_required(login_url=reverse_lazy('pecuaria:login'))
@filtrar_animais_por_setor
def animais(request, animais):
    COLUNAS_SETOR = {
        'Suinocultura': [],
        'Bovinocultura de Corte': [],
        'Bovinocultura de Leite': [],
    }

    for field in Suino._meta.fields:
        if field.name not in ['animal_ptr', 'parto', 'setor', 'id']:
            COLUNAS_SETOR['Suinocultura'].append(field.verbose_name)

    for field in BovinoCorte._meta.fields:
        if field.name not in ['animal_ptr', 'parto', 'setor', 'id']:
            COLUNAS_SETOR['Bovinocultura de Corte'].append(field.verbose_name)

    for field in BovinoLeite._meta.fields:
        if field.name not in ['animal_ptr', 'parto', 'setor', 'id']:
            COLUNAS_SETOR['Bovinocultura de Leite'].append(field.verbose_name)

    setor_nome = request.user.setor_usuarios.first().nome
    colunas = COLUNAS_SETOR.get(setor_nome, [])

    # Mude o campo status para a primeira posição da lista independente do setor
    if 'Status' in colunas:
        colunas.remove('Status')
        colunas.insert(0, 'Status')

    for animal in animais:
        animal.data_hora_de_nascimento = localtime(animal.data_hora_de_nascimento)

    print(animais)

    context = {
        'setor': setor_nome,
        'animais': animais,
        'colunas': colunas,
    }

    return render(request, 'pages/animals.html', context)

# ---------------------------- Python/IOT ----------------------------

latest_animal_data = None  # Inicializa a variável global

@csrf_exempt
def get_animal(request, rfid):
    global latest_animal_data

    try:
        animal = Animal.objects.get(rfid=rfid)
        data = {
            'id': animal.id,
            'identificacao_unica': animal.identificacao_unica,
            'rfid': animal.rfid,
            'especie': animal.especie.nome if animal.especie else 'N/A',
            'raca': animal.raca.nome if animal.raca else 'N/A',
            'tipo': animal.tipo.nome if animal.tipo else 'N/A',
            'sexo': animal.sexo,
            'data_hora_de_nascimento': animal.data_hora_de_nascimento.strftime('%d/%m/%Y às %H:%M') if animal.data_hora_de_nascimento else 'N/A',
            'peso_de_nascimento': animal.peso_de_nascimento,
            'mae': animal.mae.identificacao_unica if animal.mae else 'N/A',
            'pai': animal.pai.identificacao_unica if animal.pai else 'N/A',
            'status': animal.status,
            'setor': animal.setor.nome if animal.setor else 'N/A',
            'foto': animal.foto.url if animal.foto else os.path.join(settings.MEDIA_URL, 'bois/guliro.jpg'),
        }

        latest_animal_data = data  # Armazena os dados lidos

        return JsonResponse(data, status=200)
    except Animal.DoesNotExist:
        return JsonResponse({'error': 'Animal not found'}, status=404)

def latest_animal(request):
    """Retorna os dados do animal mais recente lido."""
    if latest_animal_data:
        return JsonResponse(latest_animal_data, status=200)
    else:
        return JsonResponse({'error': 'No data available'}, status=404)
    
def animal_info(request):
    return render(request, 'pages/animal_info.html')

    # try:
    #     animal = Animal.objects.latest('id')  # Último animal registrado
    #     idade_em_dias = animal.calcular_idade_em_dias()
    #     idade_em_meses = animal.calcular_idade_em_meses()
    #     idade_em_anos = animal.calcular_idade_em_anos()

    #     data = {
    #         'id': animal.id,
    #         'identificacao_unica': animal.identificacao_unica,
    #         'nome': animal.nome if hasattr(animal, 'nome') else 'Sem nome',
    #         'rfid': animal.rfid,
    #         'especie': animal.especie.nome if animal.especie else 'Indefinida',
    #         'raca': animal.raca.nome if animal.raca else 'Indefinida',
    #         'tipo': animal.tipo.nome if animal.tipo else 'Indefinido',
    #         'sexo': animal.sexo,
    #         'peso_de_nascimento': float(animal.peso_de_nascimento) if animal.peso_de_nascimento else 0,
    #         'data_hora_de_nascimento': animal.data_hora_de_nascimento.strftime('%d/%m/%Y %H:%M') if animal.data_hora_de_nascimento else 'Não informado',
    #         'mae': animal.mae.identificacao_unica if animal.mae else 'Desconhecida',
    #         'pai': animal.pai.identificacao_unica if animal.pai else 'Desconhecido',
    #         'status': 'Ativo' if animal.status else 'Inativo',
    #         'setor': animal.setor.nome if animal.setor else 'Indefinido',
    #         'parto': animal.parto.nome if animal.parto else 'Indefinido',
    #         'observacao': animal.get_observacao_resumida(),
    #         'idade_dias': idade_em_dias,
    #         'idade_meses': idade_em_meses,
    #         'idade_anos': idade_em_anos,
    #         'foto': animal.foto.url if animal.foto else os.path.join(settings.MEDIA_URL, 'bois/default.jpg'),
    #     }

    #     return JsonResponse(data, status=200)
    # except Animal.DoesNotExist:
    #     return JsonResponse({'error': 'Animal não encontrado'}, status=404)