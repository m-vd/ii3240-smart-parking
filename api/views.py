import json
from django.http import HttpResponse
from django.shortcuts import render
from ticketing.models import Ticket 

# Create your views here.
def TicketAPI(request, *args, **kwargs):
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        t = Ticket(userID = user_id)
        t.save()
        output = {
            'ticketID' : str(t.ticketID),
            'entryTime' : str(t.entryTime),
            'exitTime' : str(t.exitTime),
        }

        return HttpResponse(json.dumps(output))
    else:
        return HttpResponse("Hello")