from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
import datetime
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

def mostra_errori(request, question, messaggio_errore):
    """Funzione di utilità per gestire la visualizzazione degli errori e il rendering del template"""
    choices = Choice.objects.filter(question=question)
    return render(request, "sondaggi/dettagli.html", {
        'question_id': question.id,
        'question': question,
        'choices': choices,
        'messaggio_errore': messaggio_errore
    })

def voti(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    cookie_name = f'voted_{question_id}'
    if request.COOKIES.get(cookie_name):
        messaggio_errore = "Hai già votato in questo sondaggio!"
        return mostra_errori(request, question, messaggio_errore)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        messaggio_errore = "Opzione non valida!"
        return mostra_errori(request, question, messaggio_errore)
    
    selected_choice.voti = F("voti") + 1
    selected_choice.save()
    
    # Crea un cookie per marcare l'utente come votante
    response = HttpResponseRedirect(reverse("sondaggi:risultati", args=(question_id,)))
    
    # Aggiungi il cookie con il nome `voted_<question_id>` e un valore unico basato sulla domanda
    response.set_cookie(cookie_name, 'true', max_age=datetime.timedelta(days=365))  # Il cookie durerà per un anno

    return response
