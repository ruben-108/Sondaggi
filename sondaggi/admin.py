from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 2

class QuestionAdmin(admin.ModelAdmin):
	fieldset = [
		(None, {'fields': ['testo_domanda']}),
		("Informazioni data", {'fields': ['pub_data'], }),
	]
	inlines = [ChoiceInline]
	list_display = ['testo_domanda', 'data pubblicazione']


admin.site.register(Question, QuestionAdmin)