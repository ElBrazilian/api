from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .checkcorrect import isCorrect, getIp

# Rappel : Sortie de debug => L'ip nest plus donnée par le 
# client mais par le "meta" : HTTP_X_FORWARDED_FOR
# donc modifier fichier scorehashgame.py
# et changer la ligne avec payload['ip'] = ip => La supprimer

# Create your views here.
@csrf_exempt
def postScore(request):
	# first check if token is valid
	try:
		token = request.POST.get('token').strip()
		username = request.POST.get('username').strip()
		score = request.POST.get('score').strip()

		ip = request.POST.get('ip').strip()#getIp() # For debug, then => request.META.get('HTTP_X_FORWARDED_FOR')
		payload = {
			'token':token,
			'username':username,
			'score':int(score)
		}
		if not ip or not score or not username or not token:
			raise

	except:
		response = 'Invalid request'
	else:
		if isCorrect(payload, ip):
			response = 'Enterring score to db'
		else:
			response = 'Invalid token'

	return HttpResponse(response)