from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
import datetime
from .models import Question, Choice, Vote

COOKIE_NAME_LOGIN = 'logged_in'

def index(request):
	lista_domande = Question.objects.order_by('data_pubblicazione')
	return render(request, "sondaggi/index.html", {'domande': lista_domande})

def dettagli(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question_id)

    lista_domande_opzioni = {
        'question_id': question_id,
        'question': question, 'choices': choices,
        'tempo': question.tempo,
    }
    if request.COOKIES.get(COOKIE_NAME_LOGIN):
        lista_domande_opzioni['accesso_valido'] = "True"

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
    if request.COOKIES.get(cookie_name):
        if request.COOKIES.get(timestamp_name) > str(question.data_pubblicazione):
            messaggio_errore = "Hai già votato in questo sondaggio!"
            return mostra_errori(request, question, messaggio_errore)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        messaggio_errore = "Opzione non valida!"
        return mostra_errori(request, question, messaggio_errore)
    
    selected_choice.voti = F("voti") + 1
    selected_choice.save()

    user = User.objects.get(pk=int(request.COOKIES.get(COOKIE_NAME_LOGIN)))
    vote = Vote(question=question, choice=selected_choice, user=user)
    vote.save()
    
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
            response = render(request, 'sondaggi/dettagli.html', lista_domande_opzioni)
            response.set_cookie(COOKIE_NAME_LOGIN, user.pk, max_age=datetime.timedelta(days=100))
            return response
    # Se il login fallisce
    messaggio_errore = "Credenziali errate. Riprova."
    lista_domande_opzioni['messaggio_errore_login'] = messaggio_errore
    lista_domande_opzioni['mostra_modal'] = True
    lista_domande_opzioni['accesso_valido'] = "False"
    return render(request, 'sondaggi/dettagli.html', lista_domande_opzioni)

class UserCreateForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise ValidationError("Le password non corrispondono.")
        return cleaned_data


def nuovo_account(request, question_id):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # Creazione dell'utente

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                User.objects.create_user(username=username, password=password)
            except IntegrityError:
                return render(request, 'sondaggi/account.html', {'question_id': question_id, 'username_presente': "L'username inserito è già in uso. Scegline un altro."})

            question = get_object_or_404(Question, pk=question_id)
            choices = question.choice_set.all()
            lista_domande_opzioni = {
                'question_id': question_id,
                'question': question, 
                'choices': choices,
                'accesso_valido': "True"
            }
            response = render(request, 'sondaggi/dettagli.html', lista_domande_opzioni)
            response.set_cookie(COOKIE_NAME_LOGIN, 'true', max_age=datetime.timedelta(days=100))
            return response
    elif request.method == 'GET':
        return render(request, 'sondaggi/account.html', {'question_id': question_id})
    lista = {
        'question_id': question_id,
        'messaggio_errore_username': '150 caratteri o meno. Solo lettere, cifre e @/./+/-/_.',
        'messaggio_errore_psw': '''
La password non può essere troppo simile alle altre informazioni personali.<br />
La password deve contenere almeno 8 caratteri.<br />
La password non può essere una password comunemente usata.<br />
La password non può essere interamente numerica.''',
        'messaggio_errore_psw_conferma': 'Inserire la stessa password di prima, per la verifica.'
    }
    return render(request, 'sondaggi/account.html', lista)