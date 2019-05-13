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

def CheckLot(lot):
    if (lot.lotID == "Motor_Sipil" or lot.lotID == "Motor_SR" or lot.lotID == "Mobil_SR"):
        lot.capacity -= 1
        lot.save()
    

def CheckInAPI(request, *args, **kwargs):
    #API to check in to park
    #Needed parameters: userID and locationID
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        if (User.objects.filter(userID=user_id)):
            if (Ticket.objects.filter(user=user_id, exitTime__isnull=True)):
                return HttpResponseBadRequest("ERR: You have already checked in.")
            else: 
                location_id = request.POST.get('locationID')
                lot = Lot.objects.get(lotID=location_id)
                t = Ticket(user = (User.objects.get(userID = user_id)), location = lot)
                
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
                return HttpResponse(json.dumps(output))
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
            if (Booking.objects.filter(user=user_id, status="Check In")):
                b = Booking.objects.get(user=user_id, status="Check In")
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
                return HttpResponseBadRequest("ERR: You are not registered")
        else:
            return HttpResponseBadRequest("ERR: You did not ask any questions")
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
                return HttpResponseBadRequest("ERR: No such help entry.")
        else:
            return HttpResponseBadRequest("ERR: No answer is given.")
    else:
        return HttpResponse()

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
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")

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
            return HttpResponseBadRequest("ERR: No disaster found.")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")

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
            
#blm jadi nih wkwk
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

def AddBookingAPI(request, *args, **kwargs):
    #API to check in to park
    #Needed parameters: userID and locationID
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        u = User.objects.get(userID=user_id)

        if (User.objects.filter(userID=user_id) and not Booking.objects.filter(user=u, status = "Reserved")):
            location_id = request.POST.get('locationID')
            lot = Lot.objects.get(lotID=location_id)
            time = request.POST.get('bookingTime')
            bookingPrice = 5000

            if (u.userBalance >= bookingPrice) and (lot.capacity>0):
                b = Booking(user = (User.objects.get(userID = user_id)), location = lot, bookingTime= time, status="Reserved")
                if (lot.lotID == "Motor_Sipil" or lot.lotID == "Motor_SR" or lot.lotID == "Mobil_SR"):
                    lot.capacity -= 1
                    lot.save()
                b.save()
                u.userBalance = u.userBalance - bookingPrice
                u.save()

                #Send Check In Notification
                subject = 'Your booking are reserved!'
                message = 'Congratulations! \nYour booking at ' + str(b.location.lotName) + ' is reserved from ' + b.bookingTime + ' until 1 hour after that. \nThe booking will cost you IDR 5,000 exclude parking fees.'        
                to_list = [b.user.userEmail]
                send_mail(subject,message,settings.EMAIL_HOST_USER,to_list,fail_silently=True)

                #Generate output               
                output = {
                    'ticketID' : str(b.bookingID),
                    'bookingTime' : str(b.bookingTime),
                    'location' : str(b.location.lotName),
                }

                return HttpResponse(json.dumps(output))
            else:
                return HttpResponseBadRequest("ERR: Booking failed")
        else:
            return HttpResponseBadRequest("ERR: You are not allowed to book")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")

def updateBookingAPI(request, *args, **kwargs):
    #API to checkout
    #Needed parameters: userID
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        
        #Find booking and set status
        if (Booking.objects.filter(user=user_id, status="Reserved")):
            b = Booking.objects.get(user=user_id, status="Reserved")
            b.status = "Check In"
            b.save()
            return HttpResponse("Booking status updated!") 
        else: 
            return HttpResponseBadRequest("ERR: You have not booked yet.")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")


#Yang perlu dikerjain
#1. Location tuh perlu ada koordinat gitu biar bisa dikasih navigasi
#4. Generate Laporan
#5. Add booking
#6. Manage booking
#7. Navigate
