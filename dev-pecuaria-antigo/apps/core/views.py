from django.shortcuts import render, redirect
from .models import *


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('home')
        elif request.user.groups.filter(name='Pecuaria').exists():
            return redirect('pecuaria/')
        elif request.user.groups.filter(name='Edificios').exists():
            return redirect('edificios/')
        elif request.user.groups.filter(name='Seguranca').exists():
            return redirect('seguranca/')
        elif request.user.groups.filter(name='Industria').exists():
            return redirect('industria/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('home')
            elif user.groups.filter(name='Pecuaria').exists():
                return redirect('pecuaria/')
            elif user.groups.filter(name='Edificios').exists():
                return redirect('edificios/')
            elif user.groups.filter(name='Seguranca').exists():
                return redirect('seguranca/')
            elif user.groups.filter(name='Industria').exists():
                return redirect('industria/')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'login.html', {})
            # return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    else:
        return render(request, 'login.html', {})

@login_required
def home(request):
    context = {}
    return render(request, 'home.html', context)