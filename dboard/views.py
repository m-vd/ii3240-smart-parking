from django.shortcuts import render
import json, re
from django.http import HttpResponse
from ticketing.models import Ticket 
from user.models import User
from payment.models import Payment
from disaster.models import Disaster
from django.views.generic import TemplateView
from datetime import datetime, timedelta

# Create your views here.


class HomeView(TemplateView):
	template_name = 'api/index.html'
	

def countTicket(request, *args, **kwargs):
    counter_sipil = 0
    counter_sr_motor = 0
    counter_sr_mobil = 0
    counter_dalam = 0
    tickets = Ticket.objects.all()
    if (request.method == 'POST'):
	#query untuk setelah mengisi form
        date = request.POST.get('dt')
        if (date == None):
		#date kosong bakal nampilin ...
            for t in tickets:
                if (t.location.lotID == 'Motor_Sipil'):
                    counter_sipil += 1
                elif (t.location.lotID == 'Motor_SR'):
                    counter_sr_motor += 1
                elif (t.location.lotID == 'Mobil_SR'):
                    counter_sr_mobil += 1
                else:
                    counter_dalam +=1
            counter = {
		        'sipil' : counter_sipil,
		        'motor_sr'	: counter_sr_motor,
		        'mobil_sr'	: counter_sr_mobil,
		        'dalam' : counter_dalam,
		        'date' : "Ini semuanya",
	        }	        
            return render(request, 'api/index.html', {'counter': counter })
        else:
		#untuk date terisi
            #ini code untuk mengubah input html form menjadi datetime
            date_str = date + " 00:00:00.0"
            date_time_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
            d1 = date_time_obj + timedelta(days=1)
            #sampai sini
            for t in tickets:
                if (date_time_obj<t.entryTime and t.entryTime < d1):
                    if (t.location.lotID == 'Motor_Sipil'):
                        counter_sipil += 1
                    elif (t.location.lotID == 'Motor_SR'):
                        counter_sr_motor += 1
                    elif (t.location.lotID == 'Mobil_SR'):
                        counter_sr_mobil += 1
                    else:
                        counter_dalam +=1
            counter = {
		        'sipil' : counter_sipil,
		        'motor_sr'	: counter_sr_motor,
		        'mobil_sr'	: counter_sr_mobil,
		        'dalam' : counter_dalam,
		        'date' :  date,
	        }
            return render(request, 'api/index.html', {'counter': counter })
    else:   
	#default menampilkan yang sedang terparkir
        for t in tickets:
            if (t.exitTime == None):
                if (t.location.lotID == 'Motor_Sipil'):
                    counter_sipil += 1
                elif (t.location.lotID == 'Motor_SR'):
                    counter_sr_motor += 1
                elif (t.location.lotID == 'Mobil_SR'):
                    counter_sr_mobil += 1
                else:
                    counter_dalam += 1
        counter = {
			'sipil' : counter_sipil,
			'motor_sr'	: counter_sr_motor,
			'mobil_sr'	: counter_sr_mobil,
			'dalam' : counter_dalam,
			'date' : "Kendaraan yang Terparkir Saat Ini",
		}	        
        return render(request, 'api/index.html', {'counter': counter })

def countPayment(request, *args, **kwargs):
    amount_sipil = 0
    amount_sr_motor = 0
    amount_sr_mobil = 0
    amount_dalam = 0
    payment = Payment.objects.all()
    if (request.method == 'POST'):
	#query untuk setelah mengisi form
        date = request.POST.get('dt')
        #ini code untuk mengubah input html form menjadi datetime
        date_str = date + " 00:00:00.0"
        date_time_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        d1 = date_time_obj + timedelta(days=1)
        #sampai sini
        for p in payment:         
            if (date_time_obj<p.paymentTime and p.paymentTime < d1):
                if (p.ticketID.location.lotID == 'Motor_Sipil'):
                    amount_sipil += p.amount
                elif (p.ticketID.location.lotID == 'Motor_SR'):
                    amount_sr_motor += p.amount
                elif (p.ticketID.location.lotID == 'Mobil_SR'):
                    amount_sr_mobil += p.amount
                else:
                    amount_dalam += p.amount
        counter = {
		    'sipil' : amount_sipil,
		    'motor_sr'	: amount_sr_motor,
		    'mobil_sr'	: amount_sr_mobil,
		    'dalam' : amount_dalam,
		    'date' :  date,
	    }
        return render(request, 'api/payment.html', {'counter': counter })
    else:   
	#default menampilkan pemasukan hari ini saat ini
        #today = datetime.now()
        #print(today)
        #tomorow = today + timedelta(days=1)
        #print(tomorow)
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d") + " 00:00:00.01"
        today = datetime.strptime(today_str, '%Y-%m-%d %H:%M:%S.%f')
        tomorow = today + timedelta(days=1)
        for p in payment:
            if(today < p.paymentTime and p.paymentTime < tomorow):
                #ini code buat mencari tickets.ticketID yang sama dengan p.ticketID dan mendapatkan tickets.location.lotID
                #pid = p.ticketID
                #tickets = Ticket.objects.raw('SELECT * FROM Payments WHERE ticketID = %s', [pid])
                #ploc = tickets.location.lotID
                if (p.ticketID.location.lotID == 'Motor_Sipil'):
                    amount_sipil += p.amount
                elif (p.ticketID.location.lotID == 'Motor_SR'):
                    amount_sr_motor += p.amount
                elif (p.ticketID.location.lotID == 'Mobil_SR'):
                    amount_sr_mobil += p.amount
                else:
                    amount_dalam += p.amount
        counter = {
		    'sipil' : amount_sipil,
		    'motor_sr'	: amount_sr_motor,
		    'mobil_sr'	: amount_sr_mobil,
		    'dalam' : amount_dalam,
		    'date' :  "Total pemasukan hari ini: ",
	    }
        return render(request, 'api/payment.html', {'counter': counter })

def countDisaster(request, *args, **kwargs):
   
    if (request.method == 'POST'):
        date = request.POST.get('dt')
        date_str = date + " 00:00:00.0"
        date_time_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        d1 = date_time_obj + timedelta(days=1)
        #disaster = Disaster.objects.raw('SELECT * FROM Disaster WHERE disasterTime > VALUES(?) AND disasterTime < VALUES(?)', (date_time_obj, d1))
        disaster = Disaster.objects.filter(disasterTime__range=(date_time_obj,d1))    
        return render(request, 'api/disaster.html', {'disaster': disaster })
    else:   
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d") + " 00:00:00.01"
        today = datetime.strptime(today_str, '%Y-%m-%d %H:%M:%S.%f')
        tomorow = today + timedelta(days=1)

        #disaster = Disaster.objects.raw('SELECT * FROM Disaster WHERE disasterTime > VALUES(?) AND disasterTime < VALUES(?)', (today, tomorow))
        # disaster = Disaster.objects.filter(disasterTime__range=(today,tomorow))
        disaster = Disaster.objects.all()
        return render(request, 'api/disaster.html', {'disaster': disaster})

def getUnanswered(request, *args, **kwargs):
   
    if (request.method == 'POST'):
        date = request.POST.get('dt')
        date_str = date + " 00:00:00.0"
        date_time_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        d1 = date_time_obj + timedelta(days=1)
        #disaster = Disaster.objects.raw('SELECT * FROM Disaster WHERE disasterTime > VALUES(?) AND disasterTime < VALUES(?)', (date_time_obj, d1))
        disaster = Disaster.objects.filter(disasterTime__range=(date_time_obj,d1))    
        return render(request, 'api/disaster.html', {'disaster': disaster })
    else:   
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d") + " 00:00:00.01"
        today = datetime.strptime(today_str, '%Y-%m-%d %H:%M:%S.%f')
        tomorow = today + timedelta(days=1)

        #disaster = Disaster.objects.raw('SELECT * FROM Disaster WHERE disasterTime > VALUES(?) AND disasterTime < VALUES(?)', (today, tomorow))
        # disaster = Disaster.objects.filter(disasterTime__range=(today,tomorow))
        disaster = Disaster.objects.all()
        return render(request, 'api/disaster.html', {'disaster': disaster})

class ReportView(TemplateView):
	template_name = 'api/report.html'
