from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    testo_domanda = models.CharField(max_length=200)
    data_pubblicazione = models.DateTimeField()

    def __str__(self):
        return f'{self.testo_domanda}'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    testo_opzione = models.CharField(max_length=200)
    voti = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.testo_opzione}'

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Utente {self.user} ha votato per {self.question}'