from django.conf import settings
import json, datetime
from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render

#Import models
from ticketing.models import Ticket 
from parkingLot.models import Lot
from user.models import User
from payment.models import Payment
from help.models import Help
from disaster.models import Disaster


def CheckInAPI(request, *args, **kwargs):
    #API to check in to park
    #Needed parameters: userID and locationID
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        if (User.objects.filter(userID=user_id)):
            if (Ticket.objects.filter(user=user_id, exitTime__isnull=True)):
                return HttpResponse("You are already in")
            else: 
                location_id = request.POST.get('locationID')
                lot = Lot.objects.get(lotID=location_id)
                t = Ticket(user = (User.objects.get(userID = user_id)), location = lot)
                
                if (lot.lotID == "Motor_Sipil" or lot.lotID == "Motor_SR" or lot.lotID == "Mobil_SR"):
                    lot.capacity -= 1
                    lot.save()
                t.save()

                #Send Check In Notification
                subject = 'You just check In!'
                message = 'Welcome to ITB! \n You just parked your ride at ' + str(t.location.lotName) + '\n The parking will cost you IDR 2,000 perhour'        
                to_list = [t.user.userEmail]
                send_mail(subject,message,settings.EMAIL_HOST_USER,to_list,fail_silently=True)

                #Generate output               
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
        
        #Find ticket and set exit time
        if (Ticket.objects.filter(user=user_id, exitTime__isnull=True)):
            t = Ticket.objects.get(user=user_id, exitTime__isnull=True)
            t.exitTime = datetime.datetime.now()
            t.save()
            
            # Add back capacity for Sipil or SR 
            loc_obj = t.location
            if (loc_obj.lotID == "Motor_Sipil" or loc_obj.lotID == "Motor_SR" or loc_obj.lotID == "Mobil_SR"):
                loc_obj.capacity += 1
                loc_obj.save()
                
            resp = __PaymentAPI(t)
            return resp
        else: 
            return HttpResponse("You have not checked in yet")
    else:
        return HttpResponseForbidden()

def __PaymentAPI(ticket, *args, **kwargs):
    u   = User.objects.get(userID = ticket.user.userID)
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
            p = Payment(userID = ticket.user, ticketID=Ticket.objects.get(ticketID = ticket.ticketID), duration=dur, amount=total)
            p.save()
            return HttpResponse("Payment successfull, you have IDR " + str(u.userBalance) + " left")
        else:
            ticket.exitTime = None
            ticket.save()
            return HttpResponse("Your balance is not sufficient, Amount = " + str(total))

def AskHelpAPI(request, *args, **kwargs):
    # API to handle POST Request asking a question or help
    # required parameters : userID, question
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
    # required parameters : helpID, answer
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
    #required parameters: location ID
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
        return HttpResponse(json.dumps(output))
    else:
        return HttpResponse("Hello")

def UpdateDisaster(request, *args, **kwargs):
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
                'status' : str(d.user.userID),
                'location' : str(d.location),
                'description' : str(d.description),
            }
            return HttpResponse(json.dumps(output))
        else: 
            return HttpResponse("Disaster ID not valid")
    else:
        return HttpResponse("Hello")

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
            return HttpResponse("Lot Name not valid")
    else:
        return HttpResponse("Hello")
            
#blm jadi nih wkwk
def paymentReport(request, *args, **kwargs):
    if (request.method == 'GET'):
        startdate   = datetime.datetime.strptime(request.GET.get('startdate'), '%Y-%m-%d')
        enddate     = datetime.datetime.strptime(request.GET.get('enddate'), '%Y-%m-%d')
        p = Payment.objects.filter(paymentTime__range=(startdate, enddate))
        if (p):
            p_json = serializers.serialize('json', p)
            return HttpResponse(p_json, content_type='application/json')
        else: 
            return HttpResponse("Date Name not valid")
    else:
        return HttpResponse("Hello")

#Yang perlu dikerjain
#1. Location tuh perlu ada koordinat gitu biar bisa dikasih navigasi
#4. Generate Laporan
#5. Add booking
#6. Manage booking
#7. Navigate
