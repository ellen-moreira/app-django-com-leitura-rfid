from django.shortcuts import render
from .models import *
from django.db.models import Max, Count
from django.http import Http404
import json
from django.http import JsonResponse
from django.db import connection


def teste(request):
    return render(
        request,
        "teste.html",
    )

def home(request, code):
    try:
        # Tente buscar pelo campo 'link'
        u_questionario = Questionario.objects.get(link=code)
        template_name = "form.html"  # Usar template para link
    except Questionario.DoesNotExist:
        try:
            # Se não encontrado, tente buscar pelo campo 'link_resposta'
            u_questionario = Questionario.objects.get(link_resposta=code)
            
            # Filtra as respostas pelo questionário especificado
            respostas = Answer.objects.filter(questionario_id=u_questionario).order_by('questao_id')

            # Anota as respostas agrupadas por questão, tipo e valor
            respostas_agrupadas = respostas.values('questao_id__title', 'questao_id__tipo__tipo', 'answer').annotate(count=Count('answer'))

            # Transforma o QuerySet em uma estrutura de dados que pode ser iterada no template
            resultados = {}
            for resposta in respostas_agrupadas:
                questao = resposta['questao_id__title']
                tipo = resposta['questao_id__tipo__tipo']
                answer = resposta['answer']
                count = resposta['count']
                if questao in resultados:
                    resultados[questao].append({'tipo': tipo, 'answer': answer, 'count': count})
                else:
                    resultados[questao] = [{'tipo': tipo, 'answer': answer, 'count': count}]

            # Renderiza o template HTML com os resultados
            return render(request, 'resposta.html', {'u_questionario': u_questionario,'resultados': resultados})

        except Questionario.DoesNotExist:
            raise Http404("Questionário não encontrado")

    quests = Questao.objects.filter(questionario_id=u_questionario)
    return render(
        request,
        template_name,
        {"u_questionario": u_questionario, "quests": quests},
    )

def salvarAnswer(request):
    try:
        # Crie um objeto Questionario com o nome
        questionario = Questionario.objects.get(
            id=int(request.POST.get("idQuestionario"))
        )

        # Decodificar os arrays do JSON
        array_pergunta = json.loads(request.POST.get("arrayP"))
        # array_pergunta = request.POST.get("arrayP")

        print(array_pergunta)
        # Itere pelas perguntas e crie objetos Questao associados ao questionário
        for a in array_pergunta:
            resp = request.POST.get(a)
            questao = Questao.objects.get(id=a)

            # Crie a pergunta
            resposta = Answer(
                questionario_id=questionario, questao_id=questao, answer=resp
            )
            resposta.save()

        # Redirecione para a página de sucesso ou faça o que for necessário
        return render(request, "answer.html")

    except Exception as e:
        # Em caso de erro, redirecione para uma página de erro
        # return HttpResponse(
        # '<script>alert("Não foi possível responder, tente novamente - - - error_message"); window.location.href = "javascript:history.back()";</script>'
        # )
        error_message = f"Erro ao salvar o questionário: {str(e)}"
        return render(request, "form.html", {"error_message": error_message})
