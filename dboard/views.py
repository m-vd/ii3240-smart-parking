from django.shortcuts import render
import json, datetime
from django.http import HttpResponse
from ticketing.models import Ticket 
from user.models import User
from payment.models import Payment
from django.views.generic import TemplateView

# Create your views here.
def getTicket(request, *args, **kwargs):
	if (request.method == 'GET'):
		tickets = Ticket.objects.all()
		return render(request, 'templates/api/index.html', {'tickets':tickets})
    
def countTicket(request, *args, **kwargs):
	counter_sipil = 0
	counter_sr = 0
	counter_dalam = 0
	tickets = Ticket.objects.all()
	for t in tickets:
		if (t.location.lotID == 'Motor_Sipil'):
			counter_sipil += 1
		elif (t.location.lotID == "Motor_SR" or t.location.lotID == "Mobil_SR"):
			counter_sr += 1
		else:
			counter_dalam +=1
	counter = {
		'sipil' : counter_sipil,
		'sr'	: counter_sr,
		'dalam' : counter_dalam,
	}
	return render(request, '../templates/api/index.html', {'counter': counter })


class HomeView(TemplateView):
	template_name = 'api/index.html'
	
class AccidentView(TemplateView):
	template_name = 'api/accident.html'
