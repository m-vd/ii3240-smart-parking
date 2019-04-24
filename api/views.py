import json, datetime
from django.http import HttpResponse
from django.shortcuts import render
from ticketing.models import Ticket 
from user.models import User


# Create your views here.
def CheckInAPI(request, *args, **kwargs):
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        if (User.objects.filter(userID=user_id)):
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
            return HttpResponse("You're not allowed to park here")
    else:
        return HttpResponse("Hello")

def CheckOutAPI(request, *args, **kwargs):
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        if (Ticket.objects.filter(userID=user_id, exitTime__isnull=True)):
            t = Ticket.objects.get(userID=user_id, exitTime__isnull=True)
            t.exitTime = datetime.datetime.now()
            t.save()    
            u = User.objects.get(userID=user_id)
            PaymentAPI(t.ticketID)
            return HttpResponse("Goodbye, " + str(u.userName))
        else: 
            return HttpResponse("You have not checked in yet")
    else:
        return HttpResponse("Denied")

def PaymentAPI(ticket_id, *args, **kwargs):
    t = Ticket.objects.get(ticketID=ticket_id)
    u = User.objects.get(userID = t.userID)
    #insert balance calculator
    amount = 2000
    if (u.userBalance >= amount):
        u.userBalance -= amount
        #p = Payment()
        return HttpResponse("Payment successfull, you has IDR" + str(u.userBalance) + " left")
    else:
        return HttpResponse("Balance not sufficient, Amount = " + str(amount))


    