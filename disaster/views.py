from django.conf import settings
import json, datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

#Import models
from ticketing.models import Ticket 
from parkingLot.models import Lot
from user.models import User
from disaster.models import Disaster

def AddDisaster(request, *args, **kwargs):
    #required parameter: locationID, status, description
    if (request.method == 'POST'):
        location_id = request.POST.get('locationID')
        status = request.POST.get('status')
        description = request.POST.get('description')
        d = Disaster(location=Lot.objects.get(lotID = location_id), status=status, description=description)
        d.save()

        # Find all who park at the disaster location and send notifications
        to_list = []
        disasterQuery = Ticket.objects.filter(location = location_id, exitTime__isnull=True)
        for ticket in (disasterQuery):
            to_list.append(ticket.user.userEmail)
        subject = 'Please check your ride'
        message = 'We are sorry to inform that ' + description + ' has happened at ' + Lot.objects.get(lotID = location_id).lotName + '\n Please check your vehicle to ensure.' 

        send_mail(subject,message,settings.EMAIL_HOST_USER,to_list,fail_silently=True)

        output = {
            'disasterID' : str(d.disasterID),
            'status' : str(d.status),
            'location' : str(d.location),
            'description' : str(d.description),
        }
        return JsonResponse(output)
    else:
        return render(request, 'api/add-disaster.html')

def UpdateDisaster(request, *args, **kwargs):
    #required parameter: disasterID, 
    if (request.method == 'POST'):
        disaster_id = request.POST.get('disasterID')
        status = request.POST.get('status')
        description = request.POST.get('description')
        d = Disaster.objects.get(disasterID = disaster_id)

        if (d):
            d.status = status
            d.updateTime = datetime.datetime.now()
            d.description = description
            d.save()
            output = {
                'disasterID' : str(d.disasterID),
                'status' : str(d.status),
                'location' : str(d.location),
                'description' : str(d.description),
            }
            return JsonResponse(output)
        else: 
            return HttpResponseBadRequest("ERR: No disaster found.")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")
