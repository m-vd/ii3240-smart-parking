from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import ParkRecord
import time

def index(request):
	return render(request, 'park/index.html')

def checkIn(request, parkID):
	localtime = time.asctime(time.localtime(time.time()))
	
	response = "Hello, %s. You're checking in to our parking lot\n\n {}".format(localtime)

	return HttpResponse(response % parkID)

def checkOut(request, parkID):
	localtime = time.asctime(time.localtime(time.time()))
	response = "Hello, %s. You're checking out from our parking lot\n\n {}".format(localtime)
	return HttpResponse(response % parkID)

def detail(request, parkID):
	response = "Hello, %s. Your Vehicle status is Tertimpa Pohon"
	return HttpResponse(response % parkID)

def record(request):
	response = ""

	park_record_list = ParkRecord.objects.order_by('parkID')

	for item in park_record_list:
		response += "ID 			: {} <br>".format(item.parkID)
		response += "Lokasi			: {} <br>".format(item.location)
		response += "Waktu Masuk	: {} <br>".format(item.checkInTime)
		response += "status 		: {} <br>".format(item.status)
		response += "<br>"
	return HttpResponse(response)