from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login
import datetime
from .models import Question, Choice

def index(request):
	lista_domande = Question.objects.order_by('data_pubblicazione')
	return render(request, "sondaggi/index.html", {'domande': lista_domande})

def dettagli(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	choices = Choice.objects.filter(question=question_id)
	lista_domande_opzioni = {'question_id': question_id, 'question': question, 'choices': choices}
	return render(request, 'sondaggi/dettagli.html', lista_domande_opzioni)

def risultati(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    choices = question.choice_set.all()
    total_votes = sum(choice.voti for choice in choices)

    # Creo un nuovo dizionario per ogni scelta con la percentuale calcolata
    choices_with_percentage = []
    for choice in choices:
        percentuale = f'{(choice.voti / total_votes) * 100 if total_votes > 0 else 0:.2f}'
        choices_with_percentage.append({
            'choice': choice,
            'percentuale': percentuale
        })

    lista_domande_opzioni = {'question_id': question_id, 'question': question, 'choices_with_percentage': choices_with_percentage}
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
    timestamp_name = f'timestamp_{question_id}'
    if request.COOKIES.get(cookie_name) and request.COOKIES.get(timestamp_name) > str(question.data_pubblicazione):
        messaggio_errore = "Hai già votato in questo sondaggio!"
        return mostra_errori(request, question, messaggio_errore)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        messaggio_errore = "Opzione non valida!"
        return mostra_errori(request, question, messaggio_errore)
    
    selected_choice.voti = F("voti") + 1
    selected_choice.save()
    
    response = HttpResponseRedirect(reverse("sondaggi:risultati", args=(question_id,)))
    
    response.set_cookie(cookie_name, 'true', max_age=datetime.timedelta(days=100))
    response.set_cookie(timestamp_name, timezone.now(), max_age=datetime.timedelta(days=100))

    return response

def login_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    lista_domande_opzioni = {
        'question_id': question_id, 
        'question': question, 
        'choices': choices
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticazione dell'utente
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Se l'utente esiste e la password è corretta
            login(request, user)
            lista_domande_opzioni['accesso_valido'] = "True"
            return render(request, 'sondaggi/dettagli.html', lista_domande_opzioni)
    # Se il login fallisce
    messaggio_errore = "Credenziali errate. Riprova."
    lista_domande_opzioni['messaggio_errore_login'] = messaggio_errore
    lista_domande_opzioni['mostra_modal'] = True
    lista_domande_opzioni['accesso_valido'] = "False"
    return render(request, 'sondaggi/dettagli.html', lista_domande_opzioni)
