from django.shortcuts import render

def home(request):
	return render(request, 'primo_sito_web/home.html')