from django.conf import settings
import json, datetime
from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render

#Import models
from ticketing.models import Ticket 
from parkingLot.models import Lot
from user.models import User
from payment.models import Payment
from booking.models import Booking
from help.models import Help
from disaster.models import Disaster

def CheckInLotAPI(request, *args, **kwargs):
    #API to add or remove capacity per Lot.
    #required parameters: location ID
    if (request.method == 'POST'):
        location_id = request.POST.get('locationID')
        if (location_id):
            lot_obj = Lot.objects.get(lotID = location_id)
            lot_obj.capacity -= 1
            lot_obj.save()
            return HttpResponse(str(lot_obj.lotName)+" capacity -1 to "+str(lot_obj.capacity))
        else:
            return HttpResponseBadRequest("ERR: No locationID is sent.")

    else:
        return HttpResponseForbidden()

def CheckOutLotAPI(request, *args, **kwargs):
    #API to add or remove capacity per Lot.
    #required parameters: location ID
    if (request.method == 'POST'):
        location_id = request.POST.get('locationID')
        if (location_id):
            lot_obj = Lot.objects.get(lotID = location_id)
            lot_obj.capacity += 1
            lot_obj.save()
            return HttpResponse(str(lot_obj.lotName)+" capacity +1 to "+str(lot_obj.capacity))
        else:
            return HttpResponseBadRequest()

    else:
        return HttpResponseForbidden()

def getCapacity(request, *args, **kwargs):
    #required parameters : locationID
    if (request.method == 'GET'):
        lot_id = request.GET.get('locationID')
        l = Lot.objects.get(lotID = lot_id)
        if (l):
            output = {
                'location_name' : str(l.lotName),
                'location_capacity' : str(l.capacity),
            }
            return HttpResponse(json.dumps(output))
        else: 
            return HttpResponseBadRequest("ERR: No location found.")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")
            
def generateReport(request, *args, **kwargs):
    if (request.method == 'GET'):
        category = request.GET.get('category')
    
        start_date   = request.GET.get('startdate')
        end_date     = request.GET.get('enddate')

        if (start_date): 
            startdate   = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        else:
            startdate   = None

        if (end_date):
            enddate     = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        else:
            enddate     = None
        
        if (category=="payment"): 
            print(startdate, enddate)
            obj = Payment.objects.filter(paymentTime__range=(startdate, enddate))
        elif (category=="parking"):
            u   = User.objects.get(userID = request.GET.get('userID')) 
            l   = Lot.objects.get(lotID = request.GET.get('lotID'))
            obj = Ticket.objects.filter(entryTime__range=(startdate, enddate), location=l, user=u)
        else: 
            return HttpResponseBadRequest("ERR: Invalid category")

        if (obj):
            obj_json = serializers.serialize('json', obj)
            return HttpResponse(obj_json, content_type='application/json')
        else: 
            return HttpResponseBadRequest("ERR: Invalid date.")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")


#Yang perlu dikerjain
#1. Location tuh perlu ada koordinat gitu biar bisa dikasih navigasi
#4. Generate Laporan
#5. Add booking
#6. Manage booking
#7. Navigate
