
from django.urls import path
from django.views.generic import TemplateView

from .views import *


urlpatterns = [
    path("", index_base, name="index_base"),
    path("amem/", amem, name="amem"),
    path("dashboard_info/", salas_tecnologia_informacao, name='dashboard_info'), 
    path("dashboard_predioh/", salas_predio_h, name='dashboard_predioh'),
    path("dashboard_veterinaria/", salas_vet, name='dashboard_veterinaria'),
    path("Allocation_Info/", Allocation_Info, name='Allocation_Info'),
    # path("Allocation_H/", Allocation_H, name='Allocation_H'),
    path("Allocation_Vet/", Allocation_Vet, name='Allocation_Vet'),

  
]