import calendar
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import ExtractDay, ExtractWeek, ExtractMonth, ExtractYear
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import localtime
from functools import wraps

# Restrição de acesso com base em grupos de usuários (utiliza classe)
from braces.views import GroupRequiredMixin

# Restrição de acesso com base em grupos de usuários (utiliza função)
from django.contrib.auth.decorators import user_passes_test, login_required

# Função que verifica se o usuário é membro do grupo Pecuaria
def is_pecuaria_member(user):
    return user.groups.filter(name='Pecuaria').exists() or user.is_superuser

# Função que verifica os setores que o usuário tem acesso
def verificar_setor_usuario(setores):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                try:
                    for setor_nome in setores:
                        if request.user.setor.filter(nome=setor_nome).exists():
                            return JsonResponse({'permissao': True})
                    if not request.user.setor.exists():
                        return JsonResponse({'permissao': False, 'mensagem': "Você não está associado a nenhum setor de pecuária"})
                except SetorPecuaria.DoesNotExist:
                    return JsonResponse({'permissao': False, 'mensagem': "Setor não encontrado."})
                return JsonResponse({'permissao': False, 'mensagem': "Você não tem permissão para acessar esta página"})
            else:
                try:
                    for setor_nome in setores:
                        if request.user.setor.filter(nome=setor_nome).exists():
                            return view_func(request, *args, **kwargs)
                    if not request.user.setor.exists():
                        return HttpResponseForbidden("Você não está associado a nenhum setor de pecuária")
                except SetorPecuaria.DoesNotExist:
                    return HttpResponseForbidden("Setor não encontrado.")
                return HttpResponseForbidden("Você não tem permissão para acessar esta página")
        return _wrapped_view
    return decorator


# Função que filtra os lotes por setor do usuário
def filtrar_lotes_por_setor_usuario(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setor_usuario = request.user.setor.first()

        if setor_usuario:
            lotes = Lote.objects.filter(setor=setor_usuario)
        else:
            lotes = None

        kwargs["lotes"] = lotes

        return view_func(request, *args, **kwargs)

    return _wrapped_view


# Função que filtra os partos por setor do usuário
def filtrar_partos_por_setor_usuario(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setor_usuario = request.user.setor.first()

        if setor_usuario:
            partos = Parto.objects.filter(setor=setor_usuario)
            kwargs["partos"] = partos
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                "Sua conta não está associada a nenhum setor de pecuária. Contate o administrador do sistema."
            )

    return _wrapped_view


# Função que filtra os manejos por setor do usuário
def filtrar_manejos_por_setor_usuario(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setor_usuario = request.user.setor.first()

        if setor_usuario:
            manejos = ManejoPecuaria.objects.filter(setor=setor_usuario)
            kwargs["manejos"] = manejos
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                "Sua conta não está associada a nenhum setor de pecuária. Contate o administrador do sistema."
            )

    return _wrapped_view


# Função que filtra as saídas por setor do usuário
def filtrar_saidas_por_setor_usuario(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setor_usuario = request.user.setor.first()

        if setor_usuario:
            saidas = Saida.objects.filter(setor=setor_usuario)
            kwargs["saidas"] = saidas
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                "Sua conta não está associada a nenhum setor de pecuária. Contate o administrador do sistema."
            )

    return _wrapped_view


# Função que filtra os animais por setor do usuário
def filtrar_animais_por_setor_usuario(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setor_usuario = request.user.setor.first()
        MODELOS_ANIMAIS = {
            "Suínocultura": Suino,
            "Bovinocultura de Corte": BovinoCorte,
            "Bovinocultura de Leite": BovinoLeite,
        }

        if setor_usuario:
            animais = MODELOS_ANIMAIS.get(setor_usuario.nome).objects.filter(
                setor=setor_usuario
            )
            kwargs["animais"] = animais
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                "Sua conta não está associada a nenhum setor de pecuária. Contate o administrador do sistema."
            )

    return _wrapped_view


# Função que renderiza a página inicial (index.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"])
def index_pecuaria(request):
    user = request.user
    context = {
        "user": user,
    }

    return render(request, "pages/index_pecuaria.html", context)


# Função que renderiza a página de listagem dos lotes (lote.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(["Suínocultura"])
@filtrar_lotes_por_setor_usuario
def lote(request, lotes):
    lotes = Lote.objects.all()
    context = {
        "lotes": lotes,
    }

    return render(request, "pages/lote.html", context)


# Função que possibilita a criação de um novo lote (create_update_lote.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(["Suínocultura"])
def create_lote(request):
    if request.method == "GET":
        lote_form = LoteForm()
        animal_formset = AdicionarLoteAnimalFormSet(user=request.user)
    elif request.method == "POST":
        lote_form = LoteForm(request.POST)
        animal_formset = AdicionarLoteAnimalFormSet(request.POST, user=request.user)

        if lote_form.is_valid() and animal_formset.is_valid():
            lote = lote_form.save(commit=False)
            lote.setor = request.user.setor.first()
            lote.save()
            animal_formset.instance = lote
            animal_formset.save()

            messages.success(request, "Lote criado com sucesso!")

            return redirect("lote")
        else:
            messages.error(request, "Erro ao criar lote!")

    context = {
        "lote_form": lote_form,
        "animal_formset": animal_formset,
    }

    return render(request, "pages/create_update_lote.html", context)


# Função que possibilita a atualização de um lote (create_update_lote.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(["Suínocultura"])
def update_lote(request, id):
    lote = get_object_or_404(Lote, id=id)

    if request.method == "GET":
        lote_form = LoteForm(instance=lote)
        animal_formset = EditarLoteAnimalFormSet(instance=lote, user=request.user)
    elif request.method == "POST":
        lote_form = LoteForm(request.POST, instance=lote)
        animal_formset = EditarLoteAnimalFormSet(
            request.POST, instance=lote, user=request.user
        )

        if lote_form.is_valid() and animal_formset.is_valid():
            lote = lote_form.save(commit=False)
            lote.setor = request.user.setor.first()
            lote.save()
            animal_formset.instance = lote
            animal_formset.save()

            messages.success(request, "Lote atualizado com sucesso!")

            return redirect("lote")
        else:
            messages.error(request, "Erro ao atualizar lote!")

    context = {
        "lote_form": lote_form,
        "animal_formset": animal_formset,
    }

    return render(request, "pages/create_update_lote.html", context)


# Função que possibilita a exclusão de um lote
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(["Suínocultura"])
def delete_lote(request, id):
    lote = get_object_or_404(Lote, id=id)

    lote.delete()

    messages.success(request, "Lote excluído com sucesso!")

    return redirect("lote")


# Função que renderiza a página de listagem dos partos (parto.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
@filtrar_partos_por_setor_usuario
def parto(request, partos):
    context = {
        "partos": partos,
    }

    return render(request, "pages/parto.html", context)


# Função que possibilita a criação de um novo parto (create_update_parto.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def create_parto(request):
    SETORES_FORMSETS = {
        "Suínocultura": AdicionarPartoSuinoFormSet,
        "Bovinocultura de Corte": AdicionarPartoBovinoCorteFormSet,
        "Bovinocultura de Leite": AdicionarPartoBovinoLeiteFormSet,
    }

    setor_usuario = request.user.setor.first()
    AnimalFormset = SETORES_FORMSETS.get(setor_usuario.nome)

    if not AnimalFormset:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página")

    if request.method == "GET":
        parto_form = PartoForm(user=request.user)
        animal_formset = AnimalFormset()
    elif request.method == "POST":
        parto_form = PartoForm(request.POST, user=request.user)
        animal_formset = AnimalFormset(request.POST)

        if parto_form.is_valid() and animal_formset.is_valid():
            parto = parto_form.save()
            animal_formset.instance = parto
            animal_formset.save()

            messages.success(request, "Parto criado com sucesso!")

            return redirect("parto")
        else:
            messages.error(request, "Erro ao criar parto!")

    context = {
        "parto_form": parto_form,
        "animal_formset": animal_formset,
    }

    return render(request, "pages/create_update_parto.html", context)


# Função que possibilita a atualização de um parto (create_update_parto.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def update_parto(request, id):
    parto = get_object_or_404(Parto, id=id)

    SETORES_FORMSETS = {
        "Suínocultura": EditarPartoSuinoFormSet,
        "Bovinocultura de Corte": EditarPartoBovinoCorteFormSet,
        "Bovinocultura de Leite": EditarPartoBovinoLeiteFormSet,
    }

    setor_usuario = request.user.setor.first()
    AnimalFormset = SETORES_FORMSETS.get(setor_usuario.nome)

    if not AnimalFormset:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página")

    if request.method == "GET":
        parto_form = PartoForm(instance=parto, user=request.user)
        animal_formset = AnimalFormset(instance=parto)
    elif request.method == "POST":
        parto_form = PartoForm(request.POST, instance=parto, user=request.user)
        animal_formset = AnimalFormset(request.POST, instance=parto)

        if parto_form.is_valid() and animal_formset.is_valid():
            parto = parto_form.save()
            animal_formset.instance = parto
            animal_formset.save()

            messages.success(request, "Parto atualizado com sucesso!")

            return redirect("parto")
        else:
            messages.error(request, "Erro ao atualizar parto!")

    context = {
        "parto_form": parto_form,
        "animal_formset": animal_formset,
    }

    return render(request, "pages/create_update_parto.html", context)


# Função que possibilita a exclusão de um parto
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def delete_parto(request, id):
    parto = get_object_or_404(Parto, id=id)

    parto.delete()

    messages.success(request, "Parto excluído com sucesso!")

    return redirect("parto")


# Função que renderiza a página de lista de manejos (manejo.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
@filtrar_manejos_por_setor_usuario
def manejo(request, manejos):
    context = {
        "manejos": manejos,
    }

    return render(request, "pages/manejo.html", context)


# Função que possibilita a criação de um novo manejo (create_update_manejo.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def create_manejo(request):
    if request.method == "GET":
        manejo_form = ManejoForm(user=request.user)
        procedimento_formset = AdicionarProcedimentoManejoFormSet()
        produto_formset = AdicionarProdutoManejoFormSet()
    elif request.method == "POST":
        manejo_form = ManejoForm(request.POST, user=request.user)
        procedimento_formset = AdicionarProcedimentoManejoFormSet(request.POST)
        produto_formset = AdicionarProdutoManejoFormSet(request.POST)

        if (
            manejo_form.is_valid()
            and procedimento_formset.is_valid()
            and produto_formset.is_valid()
        ):
            manejo = manejo_form.save()
            procedimento_formset.instance = manejo
            produto_formset.instance = manejo
            procedimento_formset.save()
            produto_formset.save()

            messages.success(request, "Manejo criado com sucesso!")

            return redirect("manejo")
        else:
            messages.error(request, "Erro ao criar manejo!")

    context = {
        "manejo_form": manejo_form,
        "procedimento_formset": procedimento_formset,
        "produto_formset": produto_formset,
    }

    return render(request, "pages/create_update_manejo.html", context)


# Função que possibilita a atualização de um manejo (create_update_manejo.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def update_manejo(request, id):
    manejo = get_object_or_404(ManejoPecuaria, id=id)

    if request.method == "GET":
        manejo_form = ManejoForm(instance=manejo, user=request.user)
        procedimento_formset = EditarProcedimentoManejoFormSet(instance=manejo)
        produto_formset = EditarProdutoManejoFormSet(instance=manejo)
    elif request.method == "POST":
        manejo_form = ManejoForm(request.POST, instance=manejo, user=request.user)
        procedimento_formset = EditarProcedimentoManejoFormSet(
            request.POST, instance=manejo
        )
        produto_formset = EditarProdutoManejoFormSet(request.POST, instance=manejo)

        if (
            manejo_form.is_valid()
            and procedimento_formset.is_valid()
            and produto_formset.is_valid()
        ):
            manejo = manejo_form.save()
            procedimento_formset.instance = manejo
            produto_formset.instance = manejo
            procedimento_formset.save()
            produto_formset.save()

            messages.success(request, "Manejo atualizado com sucesso!")

            return redirect("manejo")
        else:
            messages.error(request, "Erro ao atualizar manejo!")

    context = {
        "manejo_form": manejo_form,
        "procedimento_formset": procedimento_formset,
        "produto_formset": produto_formset,
    }

    return render(request, "pages/create_update_manejo.html", context)


# Função que possibilita a exclusão de um manejo
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def delete_manejo(request, id):
    manejo = get_object_or_404(Manejo, id=id)

    manejo.delete()

    messages.success(request, "Manejo excluído com sucesso!")

    return redirect("manejo")


# Função que renderiza a página de listagem das saídas (saida.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
@filtrar_saidas_por_setor_usuario
def saida(request, saidas):
    context = {
        "saidas": saidas,
    }

    return render(request, "pages/saida.html", context)


# Função que possibilita a criação de uma nova saída (saida.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def create_saida(request):
    if request.method == "GET":
        saida_form = SaidaForm(user=request.user)
    elif request.method == "POST":
        saida_form = SaidaForm(request.POST, user=request.user)

        if saida_form.is_valid():
            saida = saida_form.save(commit=False)
            saida.setor = request.user.setor.first()
            saida.save()

            messages.success(request, "Saída criada com sucesso!")

            return redirect("saida")
        else:
            messages.error(request, "Erro ao criar saída!")

    context = {
        "saida_form": saida_form,
    }

    return render(request, "pages/create_update_saida.html", context)


# Função que possibilita a atualização de uma saída (saida.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def update_saida(request, id):
    saida = get_object_or_404(Saida, id=id)

    if request.method == "GET":
        saida_form = SaidaForm(instance=saida, user=request.user)
    elif request.method == "POST":
        saida_form = SaidaForm(request.POST, instance=saida, user=request.user)

        if saida_form.is_valid():
            saida = saida_form.save(commit=False)
            saida.setor = request.user.setor.first()
            saida.save()

            messages.success(request, "Saída atualizada com sucesso!")

            return redirect("saida")
        else:
            messages.error(request, "Erro ao atualizar saída!")
    
    context = {
        "saida_form": saida_form,
    }

    return render(request, "pages/create_update_saida.html", context)


# Função que possibilita a exclusão de uma saída
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
def delete_saida(request, id):
    saida = get_object_or_404(Saida, id=id)

    saida.delete()

    messages.success(request, "Saída excluída com sucesso!")

    return redirect("saida")


# Função que renderiza a página de listagem dos animais (animal.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(
    ["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"]
)
@filtrar_animais_por_setor_usuario
def animal(request, animais):
    COLUNAS_SETOR = {
        "Suínocultura": [],
        "Bovinocultura de Corte": [],
        "Bovinocultura de Leite": [],
    }

    for field in Suino._meta.fields:
        if field.name not in ["animal_ptr", "parto", "setor", "id"]:
            COLUNAS_SETOR["Suínocultura"].append(field.verbose_name)

    for field in BovinoCorte._meta.fields:
        if field.name not in ["animal_ptr", "parto", "setor", "id"]:
            COLUNAS_SETOR["Bovinocultura de Corte"].append(field.verbose_name)

    for field in BovinoLeite._meta.fields:
        if field.name not in ["animal_ptr", "parto", "setor", "id"]:
            COLUNAS_SETOR["Bovinocultura de Leite"].append(field.verbose_name)

    setor_nome = request.user.setor.first().nome
    colunas = COLUNAS_SETOR.get(setor_nome, [])

    for animal in animais:
        animal.data_hora_nascimento = localtime(animal.data_hora_nascimento)

    context = {
        "animais": animais,
        "colunas": colunas,
    }

    return render(request, "pages/animal.html", context)


# Função que renderiza a página de dashboard (dashboard.html)
@login_required
@user_passes_test(is_pecuaria_member)
@verificar_setor_usuario(["Suínocultura", "Bovinocultura de Corte", "Bovinocultura de Leite"])
def dashboard(request):
    return render(request, "pages/dashboard.html")


@login_required
@user_passes_test(is_pecuaria_member)
def gerar_grafico_dinamico(request):
    tipo_grafico = request.GET.get("tipo_grafico")
    periodo = request.GET.get("periodo")

    if tipo_grafico == "partos":
        if periodo == "daily":
            data_partos = (
                Parto.objects.annotate(
                    day=ExtractDay("data_hora_parto"),
                    month=ExtractMonth("data_hora_parto"),
                    year=ExtractYear("data_hora_parto"),
                )
                .values("day", "month", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_partos:
                labels.append(f"{entry['day']}/{entry['month']}/{entry['year']}")
                data.append(entry["count"])
        elif periodo == "weekly":
            data_partos = (
                Parto.objects.annotate(
                    week=ExtractWeek("data_hora_parto"),
                    year=ExtractYear("data_hora_parto"),
                )
                .values("week", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_partos:
                labels.append(f"Semana {entry['week']} de {entry['year']}")
                data.append(entry["count"])
        elif periodo == "monthly":
            data_partos = (
                Parto.objects.annotate(
                    month=ExtractMonth("data_hora_parto"),
                    year=ExtractYear("data_hora_parto"),
                )
                .values("month", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_partos:
                month_name = calendar.month_name[entry["month"]]
                labels.append(f"{month_name} {entry['year']}")
                data.append(entry["count"])
        elif periodo == "yearly":
            data_partos = (
                Parto.objects.annotate(year=ExtractYear("data_hora_parto"))
                .values("year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_partos:
                labels.append(entry["year"])
                data.append(entry["count"])
    elif tipo_grafico == "manejos":
        if periodo == "daily":
            data_manejos = (
                ManejoPecuaria.objects.annotate(
                    day=ExtractDay("data_hora_manejo"),
                    month=ExtractMonth("data_hora_manejo"),
                    year=ExtractYear("data_hora_manejo"),
                )
                .values("day", "month", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_manejos:
                labels.append(f"{entry['day']}/{entry['month']}/{entry['year']}")
                data.append(entry["count"])
        elif periodo == "weekly":
            data_manejos = (
                ManejoPecuaria.objects.annotate(
                    week=ExtractWeek("data_hora_manejo"),
                    year=ExtractYear("data_hora_manejo"),
                )
                .values("week", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_manejos:
                labels.append(f"Semana {entry['week']} de {entry['year']}")
                data.append(entry["count"])
        elif periodo == "monthly":
            data_manejos = (
                ManejoPecuaria.objects.annotate(
                    month=ExtractMonth("data_hora_manejo"),
                    year=ExtractYear("data_hora_manejo"),
                )
                .values("month", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_manejos:
                month_name = calendar.month_name[entry["month"]]
                labels.append(f"{month_name} {entry['year']}")
                data.append(entry["count"])
        elif periodo == "yearly":
            data_manejos = (
                ManejoPecuaria.objects.annotate(year=ExtractYear("data_hora_manejo"))
                .values("year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_manejos:
                labels.append(entry["year"])
                data.append(entry["count"])
    elif tipo_grafico == "saidas":
        if periodo == "daily":
            data_saidas = (
                Saida.objects.annotate(
                    day=ExtractDay("data_hora_saida"),
                    month=ExtractMonth("data_hora_saida"),
                    year=ExtractYear("data_hora_saida"),
                )
                .values("day", "month", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_saidas:
                labels.append(f"{entry['day']}/{entry['month']}/{entry['year']}")
                data.append(entry["count"])
        elif periodo == "weekly":
            data_saidas = (
                Saida.objects.annotate(
                    week=ExtractWeek("data_hora_saida"),
                    year=ExtractYear("data_hora_saida"),
                )
                .values("week", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_saidas:
                labels.append(f"Semana {entry['week']} de {entry['year']}")
                data.append(entry["count"])
        elif periodo == "monthly":
            data_saidas = (
                Saida.objects.annotate(
                    month=ExtractMonth("data_hora_saida"),
                    year=ExtractYear("data_hora_saida"),
                )
                .values("month", "year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_saidas:
                month_name = calendar.month_name[entry["month"]]
                labels.append(f"{month_name} {entry['year']}")
                data.append(entry["count"])
        elif periodo == "yearly":
            data_saidas = (
                Saida.objects.annotate(year=ExtractYear("data_hora_saida"))
                .values("year")
                .annotate(count=Count("id"))
            )
            labels = []
            data = []
            for entry in data_saidas:
                labels.append(entry["year"])
                data.append(entry["count"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )