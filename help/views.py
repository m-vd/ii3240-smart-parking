from django.shortcuts import render
from django.conf import settings
import json, datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render

#Import models
from user.models import User
from payment.models import Payment
from help.models import Help

# Create your views here.
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
                subject = 'Answer to your question'
                message = 'Regarding your question: '+str(h.question)+' \nResponse: '+str(h.answer)
                to_list=[h.user.userEmail]
                send_mail(subject,message,settings.EMAIL_HOST_USER,to_list,fail_silently=True)
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
