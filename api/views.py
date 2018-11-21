from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def postScore(request):
	# first check if token is valid
	token = request.POST.get('token')
	username = request.POST.get('username')
	score = request.POST.get('score')


	return HttpResponse(request.META.get('REMOTE_ADDR'))