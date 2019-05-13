"""SmartPark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import CheckInAPI
from api.views import CheckOutAPI
from api.views import AskHelpAPI
from api.views import AnswerHelpAPI
from api.views import AddDisaster
from api.views import UpdateDisaster
from api.views import getCapacity
from api.views import CheckInLotAPI
from api.views import generateReport
from api.views import AddBookingAPI
from api.views import updateBookingAPI
from dboard.views import countTicketSipil
from dboard.views import countTicketSR
from dboard.views import HomeView
from dboard.views import AccidentView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView


urlpatterns = [
    path('checkin', CheckInAPI),
    path('checkout', CheckOutAPI),
    path('admin/', admin.site.urls),
    path('askhelp', AskHelpAPI),
    path('answerhelp', AnswerHelpAPI),
    path('lot/checkin', CheckInLotAPI),
    path('adddisaster', AddDisaster),
    path('updatedisaster', UpdateDisaster),
    path('capacity', getCapacity),
    path('generatereport', generateReport),
    path('addBooking', AddBookingAPI),
    path('updateBooking', updateBookingAPI),
    path('get',countTicketSipil),
    path('get',countTicketSR),
    path('admin/', admin.site.urls),
    path('home', HomeView.as_view()),
    path('accident', AccidentView.as_view()), 
    path('userfe/', include('userfe.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    

]
