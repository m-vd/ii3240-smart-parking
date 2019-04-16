import json
from django.http import HttpResponse
from django.shortcuts import render
from ticketing.models import Ticket 

# Create your views here.
def TicketAPI(request, *args, **kwargs):
    if (request.method == 'POST'):
        t = Ticket()
        t.save()

        output = {
            'ticketID' : str(t.ticketID),
            'entryTime' : str(t.entryTime),
            'exitTime' : str(t.exitTime),
        }

        return HttpResponse(json.dumps(output))
    else:
        return HttpResponse("Hello")