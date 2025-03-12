from django.contrib import admin
from .models import Question, Choice, Vote

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 2

class QuestionAdmin(admin.ModelAdmin):
	fieldset = [
		(None, {'fields': ['testo_domanda']}),
		("Informazioni data", {'fields': ['pub_data'], }),
	]
	exclude = ('votes',)
	inlines = [ChoiceInline]
	list_display = ['testo_domanda', 'data pubblicazione']

class VoteAdmin(admin.ModelAdmin):
    # Mostra i campi da visualizzare nell'admin
    list_display = ('question', 'user_ip', 'get_question_text')
    
    # Aggiungi un campo aggiuntivo che mostri il testo della domanda
    def get_question_text(self, obj):
        return obj.question.testo_domanda
    get_question_text.short_description = 'Testo della domanda'
    
    # Rendi i campi solo in lettura
    readonly_fields = ('question', 'user_ip')

    # Disabilita la possibilità di aggiungere, modificare o eliminare oggetti
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False 

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote)