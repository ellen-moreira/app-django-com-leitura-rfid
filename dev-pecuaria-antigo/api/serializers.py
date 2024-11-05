from apps.pecuaria.models import *
from django.contrib.auth.models import User
from rest_framework import serializers

class AnimalSerializer(serializers.ModelSerializer):
    especie = serializers.SlugRelatedField(slug_field='nome', queryset=Especie.objects.all())
    raca = serializers.SlugRelatedField(slug_field='nome', queryset=Raca.objects.all())
    tipo = serializers.SlugRelatedField(slug_field='nome', queryset=Tipo.objects.all())

    class Meta:
        model = Animal
        fields = '__all__'