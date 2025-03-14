from django.urls import path
from . import views

app_name = 'sondaggi'
urlpatterns = [
	path('', views.index, name='index'),
	path('<int:question_id>/', views.dettagli, name='dettagli'),
	path('<int:question_id>/risultati/', views.voti, name='voti'),
	path('<int:question_id>/voti/', views.risultati, name='risultati'),
	path('autenticazione/<int:question_id>/', views.login_view, name='login'),
	path('nuovo_account/<int:question_id>/', views.nuovo_account, name='account')
]