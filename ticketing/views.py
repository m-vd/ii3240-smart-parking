from django.conf import settings
import json, datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

#Import models
from ticketing.models import Ticket 
from parkingLot.models import Lot
from user.models import User
from payment.models import Payment
from booking.models import Booking
from help.models import Help
from disaster.models import Disaster
from booking.views import CheckInBooking

def CheckLot(lot):
    if (lot.lotID == "Motor_Sipil" or lot.lotID == "Motor_SR" or lot.lotID == "Mobil_SR"):
        lot.capacity -= 1
        lot.save()
    
def CheckInAPI(request, *args, **kwargs):
    #API to check in to park
    #Needed parameters: userID and locationID
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        location_id = request.POST.get('locationID')
        lot = Lot.objects.get(lotID=location_id)
        if (User.objects.filter(userID=user_id)):
            u=User.objects.get(userID = user_id)
            if (Ticket.objects.filter(user=user_id, exitTime__isnull=True)):
                return HttpResponseBadRequest("ERR: You have already checked in.")
            elif (u.userType>=lot.auth):              
                t = Ticket(user = u, location = lot)               
                if (not CheckInBooking(user_id)):
                    CheckLot(lot)
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
                return JsonResponse(output)
            else:
                return HttpResponse("ERR: You are not allowed to park here")
        else:
            return HttpResponseBadRequest("ERR: You are not registered.")
    else:
        return HttpResponseForbidden("ERR: You're not allowed to access this endpoint.")


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
            CheckLot(loc_obj)

            #Change booking status if the lot was booked
            if (Booking.objects.filter(user=user_id, status="Checked In")):
                b = Booking.objects.get(user=user_id, status="Checked In")
                b.status = "Checked Out"
                b.save()
            
            resp = __Payment(t)
            return resp
        else: 
            return HttpResponseBadRequest("ERR: You are not checked in.")
    else:
        return HttpResponseForbidden("ERR: You're not allowed to access this endpoint.")

def __Payment(ticket, *args, **kwargs):
    u   = User.objects.get(userID = ticket.user.userID)
    if (not u):
        return HttpResponse("error")
    else:
        #Set daily price
        if (ticket.location.lotID == "Motor_Sipil" or ticket.location.lotID == "Motor_SR"):        
            dailyPrice  = 2000
        elif (ticket.location.lotID == "Mobil_SR"):
            dailyPrice = 5000
        else: 
            dailyPrice = 0
        #Duration is defined as days that the parking lot is utilized
        dur     = (ticket.exitTime-ticket.entryTime).days 
        #Duration + 1 since the price is counted since day 0
        total   = (dur+1)*dailyPrice

        if (u.userBalance >= total):
            u.userBalance = u.userBalance - total
            u.save()
            p = Payment(userID = ticket.user, ticketID=Ticket.objects.get(ticketID = ticket.ticketID), duration=dur, amount=total)
            p.save()
            return HttpResponse(("You paid IDR {:,} \n Payment successfull, you have IDR {:,} left").format(total, u.userBalance))
        else:
            ticket.exitTime = None
            ticket.save()
            return HttpResponse("Your balance is not sufficient, Amount = " + str(total))