import json, datetime
from django.http import HttpResponse
from django.shortcuts import render
from ticketing.models import Ticket 
from user.models import User
from payment.models import Payment


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
            resp = PaymentAPI(t.ticketID)
            return resp
        else: 
            return HttpResponse("You have not checked in yet")
    else:
        return HttpResponse("Denied")

def PaymentAPI(ticket_id, *args, **kwargs):
    t = Ticket.objects.get(ticketID=ticket_id)
    u = User.objects.get(userID = t.userID)
    price = 2000
    dur = (t.exitTime-t.entryTime).seconds//3600 
    remain = (t.exitTime-t.entryTime).seconds%3600 
    print(dur)
    total = dur*price 
    if (remain):
        total += price
    if (u.userBalance >= total):
        u.userBalance = u.userBalance - total
        u.save()
        p = Payment(userID = t.userID, ticketID=ticket_id, duration=dur, amount=total)
        p.save()
        return HttpResponse("Payment successfull, you have IDR" + str(u.userBalance) + " left")
    else:
        t.exitTime = None
        t.save()
        return HttpResponse("Your balance is not sufficient, Amount = " + str(total))

