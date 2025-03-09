from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from .models import Question, Choice

def index(request):
	lista_domande = Question.objects.order_by('data pubblicazione')
	return render(request, "sondaggi/index.html", {'domande': lista_domande})

def dettagli(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	choices = Choice.objects.filter(question=question_id)
	lista_domande_opzioni = {'question_id': question_id, 'question': question, 'choices': choices}
	return render(request, 'sondaggi/dettagli.html', lista_domande_opzioni)

def risultati(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    lista_domande_opzioni = {'question_id': question_id, 'question': question}
    return render(request, 'sondaggi/risultati.html', lista_domande_opzioni)

def voti(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        choices = Choice.objects.filter(question=question_id)
        lista_domande_opzioni = {'question_id': question_id, 'question': question, 'choices': choices}
        return render(request, "sondaggi/dettagli.html", lista_domande_opzioni)
    selected_choice.voti = F("voti") + 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("sondaggi:risultati", args=(question_id, )))