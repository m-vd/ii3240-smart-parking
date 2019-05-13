from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from ticketing.models import Ticket

def index(request):
#	return HttpResponse("Hello")
	context = None;
	return render(request, 'userfe/index.html', context)
def faq(request):
	context = None;
	return render(request, 'userfe/faq.html', context)
	
def book(request):
	context = None;
	return render(request, 'userfe/book.html', context)
	
def login(request):
	context = None;
	return render(request, 'userfe/login.html', context)
	
def help(request):
	context = None;
	return render(request, 'userfe/help.html', context)
	
def navigate(request):
	context = None;
	return render(request, 'userfe/navigate.html', context)

def countSlot(request, *args, **kwargs):
	counter_sipil = 0
	counter_sr_mobil = 0
	counter_sr_motor = 0
	tickets = Ticket.objects.all()
	for t in tickets:
		if (t.exitTime == None):
			if (t.location.lotID == 'Motor_Sipil'):
				counter_sipil += 1
			elif (t.location.lotID == 'Motor_SR'):
				counter_sr_motor += 1
			elif (t.location.lotID == 'Mobil_SR'):
				counter_sr_mobil += 1
	slot_sipil = 300 - counter_sipil
	slot_sr_motor = 200 - counter_sr_motor
	slot_sr_mobil = 14 - counter_sr_mobil

	slot = {
		'sipil' : slot_sipil,
		'motor_sr' : slot_sr_motor,
		'mobil_sr' : slot_sr_mobil,
	}
	return render(request, 'userfe/index.html', {'slot': slot})