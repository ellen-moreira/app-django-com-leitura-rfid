from django.urls import path
from .views import * 

urlpatterns = [
    path('feedback/<str:code>', home, name="index"),
    path('feedback/salvarAnswer/', salvarAnswer, name="salvarAnswer"),
]