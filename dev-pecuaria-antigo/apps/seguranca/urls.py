from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', index_seguranca, name='index_seguranca'),
    path('iniciar_ronda/', views.iniciar_ronda, name='iniciar_ronda'),
    path('encerrar_ronda/', views.encerrar_ronda, name='encerrar_ronda'),
    path('registrar_ocorrencia/', views.registrar_ocorrencia, name='registrar_ocorrencia'),
]