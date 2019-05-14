from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from ticketing.models import Ticket
from parkingLot.models import Lot

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
	counter_dalam_mobil = 0
	counter_dalam_motor = 0

	capacity_sipil = 0
	capacity_sr_motor = 0
	capacity_sr_mobil = 0
	capacity_dalam_motor = 0
	capacity_dalam_mobil = 0

	tickets = Ticket.objects.all()
	location = Lot.objects.all()

	for l in location:
		if (l.lotID == 'Motor_Sipil'):
			capacity_sipil = l.capacity
		elif (l.lotID == 'Motor_SR'):
			capacity_sr_motor = l.capacity
		elif (l.lotID == 'Mobil_SR'):
			capacity_sr_mobil = l.capacity
		elif (l.lotID == 'Dalam_Motor_LabtekV' or l.lotID == 'Dalam_Motor_LabtekVIII'):
			capacity_dalam_motor = capacity_dalam_motor + l.capacity
		else:
			capacity_dalam_mobil = capacity_dalam_mobil + l.capacity 

	for t in tickets:
		if (t.exitTime == None):
			if (t.location.lotID == 'Motor_Sipil'):
				counter_sipil += 1
			elif (t.location.lotID == 'Motor_SR'):
				counter_sr_motor += 1
			elif (t.location.lotID == 'Mobil_SR'):
				counter_sr_mobil += 1
			elif (t.location.lotID == 'Dalam_Motor_LabtekV' or t.location.lotID == 'Dalam_Motor_LabtekVIII'):
				counter_dalam_motor += 1
			else:
				counter_dalam_mobil += 1

	slot_sipil = capacity_sipil - counter_sipil
	slot_sr_motor = capacity_sr_motor - counter_sr_motor
	slot_sr_mobil = capacity_sr_mobil - counter_sr_mobil
	slot_dalam_motor = capacity_dalam_motor - counter_dalam_motor
	slot_dalam_mobil = capacity_dalam_mobil - counter_dalam_mobil

	slot = {
		'sipil' : slot_sipil,
		'motor_sr' : slot_sr_motor,
		'mobil_sr' : slot_sr_mobil,
		'dalam_motor' : slot_dalam_motor,
		'dalam_mobil' : slot_dalam_mobil,
	}
	return render(request, 'userfe/index.html', {'slot': slot})

def inputHelp(request, *args, **kwargs):
	uname = request.user.username
	return render(request, 'userfe/help.html', {'uname': uname})

def inputBook(request, *args, **kwargs):
	uname = request.user.username
	return render(request, 'userfe/book.html', {'uname': uname})
