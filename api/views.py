import json, datetime
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render

#Import models
from ticketing.models import Ticket 
from parkingLot.models import Lot
from user.models import User
from payment.models import Payment
from help.models import Help

def CheckInAPI(request, *args, **kwargs):
    #API to check in to park
    #Needed parameters: userID and location
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        if (User.objects.filter(userID=user_id)):
            if (Ticket.objects.filter(userID=user_id, exitTime__isnull=True)):
                return HttpResponse("You are already in")
            else: 
                parkloc = request.POST.get('location')
                lot = Lot.objects.get(lotName=parkloc)
                t = Ticket(userID = User.objects.get(userID=user_id), location = lot)
                
                if (lot.lotName == "Sipil" or lot.lotName == "SR"):
                    lot.capacity -= 1
                    lot.save()
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
        return HttpResponseForbidden()

def CheckOutAPI(request, *args, **kwargs):
    #API to checkout
    #Needed parameters: userID
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        if (Ticket.objects.filter(userID=user_id, exitTime__isnull=True)):
            t = Ticket.objects.get(userID=user_id, exitTime__isnull=True)
            t.exitTime = datetime.datetime.now()
            t.save()
            print(t)
            resp = __PaymentAPI(t)
            return resp
        else: 
            return HttpResponse("You have not checked in yet")
    else:
        return HttpResponseForbidden()

def __PaymentAPI(ticket, *args, **kwargs):
    u   = User.objects.get(userID = ticket.userID.userID)
    if (not u):
        return HttpResponse("error")
    else:
        price   = 2000
        dur     = (ticket.exitTime-ticket.entryTime).seconds//3600 
        remain  = (ticket.exitTime-ticket.entryTime).seconds%3600 

        print(dur)
        total = dur*price 

        if (remain):
            total += price
        if (u.userBalance >= total):
            u.userBalance = u.userBalance - total
            u.save()
            p = Payment(userID = ticket.userID, ticketID=Ticket.objects.get(ticketID = ticket.ticketID), duration=dur, amount=total)
            loc_obj = ticket.location
            loc_obj.capacity += 1
            loc_obj.save()
            p.save()
            return HttpResponse("Payment successfull, you have IDR" + str(u.userBalance) + " left")
        else:
            ticket.exitTime = None
            ticket.save()
            return HttpResponse("Your balance is not sufficient, Amount = " + str(total))

def AskHelpAPI(request, *args, **kwargs):
    # API to handle POST Request asking a question or help
    if (request.method == 'POST'):
        question = request.POST.get('question')
        if (question):
            try:
                u = User.objects.get(userID = request.POST.get('userID'))
                h = Help(user = u, question = question)
                h.save()
                output = {
                    'helpID' : str(h.helpID),
                    'userID' : str(h.user.userID),
                    'question' : str(h.question),
                }
                return HttpResponse(json.dumps(output))
            except:
                return HttpResponseBadRequest("User not registered")
        else:
            return HttpResponseBadRequest("No questions asked")
    else:
        return HttpResponseForbidden()

def AnswerHelpAPI(request, *args, **kwargs):
    #API to handle POST Request answering a question or help
    if (request.method == 'POST'):
        answer = request.POST.get('answer')
        help_id = request.POST.get('helpID')
        if (answer):
            try:
                h = Help.objects.get(helpID = help_id)
                h.answer = answer
                h.answerTime = datetime.datetime.now()
                h.save()
                output = {
                    'helpID' : str(h.helpID),
                    'question' : str(h.question),
                    'answer' : str(h.answer),
                }
                return HttpResponse(json.dumps(output))
            except: 
                return HttpResponseBadRequest("Help ID not valid")
        else:
            return HttpResponseBadRequest("No answer is given")
    else:
        return HttpResponse("Hello")

def CheckInLotAPI(request, *args, **kwargs):
    #API to add or remove capacity per Lot.
    if (request.method == 'POST'):
        location_id = request.POST.get('locationID')
        if (location_id):
            lot_obj = Lot.objects.get(lotID = location_id)
            lot_obj.capacity -= 1
            lot_obj.save()
        else:
            return HttpResponseBadRequest()

    else:
        return HttpResponseForbidden()
