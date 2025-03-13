from django.contrib import admin
from .models import Question, Choice
from django.utils import timezone


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['testo_domanda']}),
        ("Informazioni data", {'fields': ['data_pubblicazione'], }),
    ]
    inlines = [ChoiceInline]
    list_display = ['testo_domanda', 'data_pubblicazione']
    
    # Azione per azzerare i voti di tutte le scelte
    def reset_voti(self, request, queryset):
        for question in queryset:
            question.choice_set.update(voti=0)  # Azzera i voti per tutte le scelte di questa domanda
            question.data_pubblicazione = timezone.now()
            print(f'\n{timezone.now()}\n')
            question.save()
        self.message_user(request, "I voti sono stati azzerati per tutte le opzioni.")
    
    reset_voti.short_description = "Azzera tutti i voti delle scelte"  # Descrizione dell'azione
    
    # Aggiungiamo l'azione personalizzata
    actions = [reset_voti]

admin.site.register(Question, QuestionAdmin)
