from app.models import *
from django.shortcuts import redirect
from functools import wraps

# Decorator para restringir o acesso a uma view com base nos setores permitidos
def restringir_acesso(setores_permitidos):
    """
    Decorator que restringe o acesso a uma view com base nos setores permitidos.

    Args:
        setores_permitidos (list): Lista de setores permitidos a acessar a view.

    Returns:
        function: View decorada que restringe o acesso a usuários com setores específicos.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            usuario = request.user

            # Obtém todos os setores associados ao usuário
            setores_usuario = usuario.setor_usuarios.all()

            # Verifica se o usuário está associado a algum setor
            if not setores_usuario.exists():
                # Redireciona para a página de erro 404 se o usuário não tiver setores associados
                request.session['status_code'] = 404
                request.session['message'] = 'Você não está associado a nenhum setor.'
                return redirect('pecuaria:error_page')

            # Verifica se o usuário tem acesso a algum dos setores permitidos
            if not any(setor.nome in setores_permitidos for setor in setores_usuario):
                # Redireciona para a página de erro 403 se o usuário não tiver permissão
                request.session['status_code'] = 403
                request.session['message'] = 'Você não tem permissão para acessar esta página.'
                return redirect('pecuaria:error_page')

            # Chama a view original se o usuário tiver permissão
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# Decorator para filtrar os lotes de acordo com o setor do usuário
def filtrar_lotes_por_setor(view_func):
    """
    Decorator que filtra os lotes disponíveis com base no setor do usuário.

    Args:
        view_func (function): A view a ser decorada.

    Returns:
        function: View decorada que filtra os lotes pelo setor do usuário.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        usuario = request.user

        # Obtém o primeiro setor associado ao usuário
        setor_usuario = usuario.setor_usuarios.first()

        # Filtra os lotes de acordo com o setor do usuário
        if setor_usuario:
            lotes = Lote.objects.filter(setor=setor_usuario)
        else:
            lotes = Lote.objects.none()

        # Passa os lotes filtrados para a view via kwargs
        kwargs['lotes'] = lotes

        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Decorator para filtrar os partos de acordo com o setor do usuário
def filtrar_partos_por_setor(view_func):
    """
    Decorator que filtra os partos disponíveis com base no setor do usuário.

    Args:
        view_func (function): A view a ser decorada.

    Returns:
        function: View decorada que filtra os partos pelo setor do usuário.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        usuario = request.user

        # Obtém o primeiro setor associado ao usuário
        setor_usuario = usuario.setor_usuarios.first()

        # Filtra os partos de acordo com o setor do usuário
        if setor_usuario:
            partos = Parto.objects.filter(setor=setor_usuario)
        else:
            partos = Parto.objects.none()

        # Passa os partos filtrados para a view via kwargs
        kwargs['partos'] = partos

        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Decorator para filtrar os manejos de acordo com o setor do usuário
def filtrar_manejos_por_setor(view_func):
    """
    Decorator que filtra os manejos disponíveis com base no setor do usuário.

    Args:
        view_func (function): A view a ser decorada.

    Returns:
        function: View decorada que filtra os manejos pelo setor do usuário.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        usuario = request.user

        # Obtém o primeiro setor associado ao usuário
        setor_usuario = usuario.setor_usuarios.first()

        # Filtra os manejos de acordo com o setor do usuário
        if setor_usuario:
            manejos = Manejo.objects.filter(setor=setor_usuario)
        else:
            manejos = Manejo.objects.none()

        # Passa os manejos filtrados para a view via kwargs
        kwargs['manejos'] = manejos

        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Decorator para filtrar as saídas de acordo com o setor do usuário
def filtrar_saidas_por_setor(view_func):
    """
    Decorator que filtra as saídas disponíveis com base no setor do usuário.

    Args:
        view_func (function): A view a ser decorada.

    Returns:
        function: View decorada que filtra as saídas pelo setor do usuário.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        usuario = request.user

        # Obtém o primeiro setor associado ao usuário
        setor_usuario = usuario.setor_usuarios.first()

        # Filtra as saídas de acordo com o setor do usuário
        if setor_usuario:
            saidas = Saida.objects.filter(setor=setor_usuario)
        else:
            saidas = Saida.objects.none()

        # Passa as saídas filtradas para a view via kwargs
        kwargs['saidas'] = saidas

        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Decorator para filtrar os animais de acordo com o setor do usuário
def filtrar_animais_por_setor(view_func):
    """
    Decorator que filtra os animais disponíveis com base no setor do usuário.

    Args:
        view_func (function): A view a ser decorada.

    Returns:
        function: View decorada que filtra os animais pelo setor do usuário.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Obtém o primeiro setor associado ao usuário
        setor_usuario = request.user.setor_usuarios.first()

        # Define o modelo de animal de acordo com o setor
        MODELOS_ANIMAIS = {
            "Suinocultura": Suino,
            "Bovinocultura de Corte": BovinoCorte,
            "Bovinocultura de Leite": BovinoLeite,
        }

        # Filtra os animais de acordo com o setor do usuário
        if setor_usuario:
            animais = MODELOS_ANIMAIS.get(setor_usuario.nome).objects.filter(setor=setor_usuario)
            print(setor_usuario)
        else:
            animais = MODELOS_ANIMAIS.get(setor_usuario.nome).objects.none()
            
        # Passa os animais filtrados para a view via kwargs
        kwargs["animais"] = animais

        return view_func(request, *args, **kwargs)

    return _wrapped_view