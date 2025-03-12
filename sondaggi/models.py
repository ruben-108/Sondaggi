from django.db import models

class Question(models.Model):
	testo_domanda = models.CharField(max_length=200)
	pub_data = models.DateTimeField(name='data pubblicazione')
	votes = models.ManyToManyField('Vote', related_name='voted_questions', blank=True)

	def __str__(self):
		return self.testo_domanda


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	testo_opzione = models.CharField(max_length=200)
	voti = models.IntegerField(default=0)

	def __str__(self):
		return self.testo_opzione


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField()

    def __str__(self):
        return f"IP Utente: {self.user_ip}, Domanda: {self.question}"
