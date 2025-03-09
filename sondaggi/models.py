from django.db import models

class Question(models.Model):
	testo_domanda = models.CharField(max_length=200)
	pub_data = models.DateTimeField(name='data pubblicazione')

	def __str__(self):
		return self.testo_domanda

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	testo_opzione = models.CharField(max_length=200)
	voti = models.IntegerField(default=0)

	def __str__(self):
		return self.testo_opzione
