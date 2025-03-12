from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.db.models import F
from django.urls import reverse
from .models import Question, Choice, Vote

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
    
    user_ip = request.META.get('REMOTE_ADDR')
    
    if question.votes.filter(user_ip=user_ip).exists():
        messaggio_errore = "Hai già votato in questo sondaggio!"
        choices = Choice.objects.filter(question=question_id)
        lista_domande_opzioni = {'question_id': question_id, 'question': question, 'choices': choices, 'messaggio_errore': messaggio_errore}
        return render(request, "sondaggi/dettagli.html", lista_domande_opzioni)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Ridisplay della domanda di voto
        choices = Choice.objects.filter(question=question_id)
        lista_domande_opzioni = {'question_id': question_id, 'question': question, 'choices': choices}
        return render(request, "sondaggi/dettagli.html", lista_domande_opzioni)
    
    selected_choice.voti = F("voti") + 1
    selected_choice.save()
    
    # Salva l'IP dell'utente come già votante
    question.votes.create(user_ip=user_ip, question=question)

    # Redirect alla pagina dei risultati
    return HttpResponseRedirect(reverse("sondaggi:risultati", args=(question_id, )))
