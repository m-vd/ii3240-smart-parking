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
		tickets = Tickets.objects.all()
		return render(request, 'templates/api/index.html', {'tickets':tickets})
    
def countTicketSipil(request, *args, **kwargs):
	counter = 0
	tickets = Tickets.object.all()
	for tickets.location in tickets:
		if (tickets.location == 'Sipil'):
			counter += 1
	return render(request, 'templates/api/index.html', {'counter':counter})

def countTicketSR(request, *args, **kwargs):
	counter = 0
	tickets = Tickets.object.all()
	for tickets.location in tickets:
		if (tickets.location == 'SR'):
			counter += 1
	return render(request, 'templates/api/index.html', {'counter':counter})

class HomeView(TemplateView):
	template_name = 'api/index.html'
	
class AccidentView(TemplateView):
	template_name = 'api/accident.html'
