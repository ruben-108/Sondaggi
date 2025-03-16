from django.contrib import admin
from django.http import HttpRequest
from .models import Question, Choice, Vote
from django.utils import timezone


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    readonly_fields = ['voti']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['testo_domanda', 'data_pubblicazione', 'tempo']
    list_editable = ['tempo']
    list_per_page = 10
    
    # Azione per azzerare i voti di tutte le scelte
    def reset_voti(self, request, queryset):
        for question in queryset:
            question.choice_set.update(voti=0)  # Azzera i voti per tutte le scelte di questa domanda
            question.data_pubblicazione = timezone.now()
            question.save()
        self.message_user(request, "I voti sono stati azzerati per tutte le opzioni.")
    
    reset_voti.short_description = "Azzera tutti i voti delle scelte"  # Descrizione dell'azione
    
    # Aggiungiamo l'azione personalizzata
    actions = [reset_voti]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice', 'user']
    list_per_page = 10
    readonly_fields = ['question', 'choice', 'user']

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request, obj=None):
        return False
