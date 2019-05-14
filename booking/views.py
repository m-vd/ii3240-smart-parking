from django.conf import settings
import json, datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
import requests

#Import models
from ticketing.models import Ticket 
from parkingLot.models import Lot
from user.models import User
from booking.models import Booking
from payment.models import Payment

def Book(request, *args, **kwargs):
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
                message = 'Congratulations! \nYour booking at ' + str(b.location.lotName) + ' is reserved from ' + str(b.bookingTime) + ' until 1 hour after that. \nThe booking will cost you IDR 5,000 exclude parking fees.'        
                to_list = [b.user.userEmail]
                send_mail(subject,message,settings.EMAIL_HOST_USER,to_list,fail_silently=True)

                #Generate output               
                output = {
                    'bookingID' : str(b.bookingID),
                    'bookingTime' : str(b.bookingTime),
                    'location' : str(b.location.lotName),
                }

                return JsonResponse(output)
            else:
                return HttpResponseBadRequest("ERR: Booking failed")
        else:
            return HttpResponseBadRequest("ERR: You are not allowed to book")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")

def CheckInBooking(request, *args, **kwargs):
    #API to checkout
    #Needed parameters: userID
    if (request.method == 'POST'):
        user_id = request.POST.get('userID')
        
        #Find booking and set status
        if (Booking.objects.filter(user=user_id, status="Reserved")):
            b = Booking.objects.get(user=user_id, status="Reserved")
            b.status = "Checked In"
            b.checkInTime = datetime.datetime.now()
            b.save()

            #Create ticket by calling CheckInAPI from Ticketing.
            #But first add back the location capacity so it won't be reduced twice since CheckInAPI also decreases it.
            lot = b.location
            if (lot.lotID == "Motor_Sipil" or lot.lotID == "Motor_SR" or lot.lotID == "Mobil_SR"):
                lot.capacity += 1
                lot.save()

            #Send a request to CheckInAPI
            url = "http://0.0.0.0:8000/check-in"
            userID = b.user.userID
            lotID = b.location.lotID
            payload = "userID="+str(userID)+"&locationID="+str(lotID)
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
            }

            requests.request("POST", url, data=payload, headers=headers)

            #Generate Output
            output = {
                'bookingID'     : str(b.bookingID),
                'bookingTime'   : str(b.bookingTime),
                'location'      : str(b.location.lotName),
                'status'        : str(b.status),
                'checkInTime'   : str(b.checkInTime),
            }

            return JsonResponse(output)
        else: 
            return HttpResponseBadRequest("ERR: You have not booked yet.")
    else:
        return HttpResponseForbidden("ERR: You are not allowed to access this endpoint.")

