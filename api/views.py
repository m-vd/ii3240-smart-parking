import json, datetime
from django.http import HttpResponse
from django.shortcuts import render
from ticketing.models import Ticket 


# Create your views here.
def CheckInAPI(request, *args, **kwargs):
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        if (Ticket.objects.filter(userID=user_id, exitTime__isnull=True)):
            return HttpResponse("You are already in")
        else: 
            parkloc = request.POST.get('location')
            t = Ticket(userID = user_id, location = parkloc)
            t.save()
            output = {
                'ticketID' : str(t.ticketID),
                'entryTime' : str(t.entryTime),
                'exitTime' : str(t.exitTime),
            }
            return HttpResponse(json.dumps(output))
    else:
        return HttpResponse("Hello")

def CheckOutAPI(request, *args, **kwargs):
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        t = Ticket.objects.get(userID=user_id, exitTime__isnull=True)
        t.exitTime = datetime.datetime.now()
        t.save()    
        return HttpResponse("Hello again")
    else:
        return HttpResponse("Denied")
