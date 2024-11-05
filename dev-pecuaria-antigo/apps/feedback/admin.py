from django.contrib import admin
from .models import *


import nested_admin
import random
import string


class AlternativaInline(nested_admin.NestedStackedInline):
    model = Alternativa
    extra = 0

class QuestaoInline(nested_admin.NestedStackedInline):
    model = Questao
    extra = 1
    inlines = [AlternativaInline]
    
def link_form(obj):
    return f'https://campusinteligentetest.ifsuldeminas.edu.br/feedback/{obj.link}'

def link_resposta(obj):
    return f'https://campusinteligentetest.ifsuldeminas.edu.br/feedback/{obj.link_resposta}'

class QuestionarioAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'nome', link_form, link_resposta)
    list_editable = ('nome',)
    exclude = ('link', 'link_resposta')
    
    inlines = [QuestaoInline]
    
    # readonly_fields = ('link',)  # Define 'link' como somente leitura

    def save_model(self, request, obj, form, change):
        if not obj.link:
            # Gere um código aleatório de 25 caracteres
            obj.link = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))
        obj.save()
        if not obj.link_resposta:
            # Gere um código aleatório de 25 caracteres
            obj.link_resposta = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(25))
        obj.save()

class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'questao_id', 'questionario_id')

admin.site.register(Questionario, QuestionarioAdmin)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Type)
admin.site.register(Alternativa)
admin.site.register(Answer, AnswerAdmin)