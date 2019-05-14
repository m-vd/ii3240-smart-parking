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

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.urls import path, include

#Ticketing 
from ticketing.views import CheckInAPI
from ticketing.views import CheckOutAPI
from api.views import CheckInLotAPI
#Help
from help.views import AskHelpAPI
from help.views import AnswerHelpAPI
#Disaster
from disaster.views import AddDisaster
from disaster.views import UpdateDisaster
#Others
from api.views import getCapacity
from api.views import generateReport
#Booking
from booking.views import AddBookingAPI
from booking.views import UpdateBookingAPI
#Website
from dboard.views import HomeView
from dboard.views import AccidentView

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
    path('updateBooking', UpdateBookingAPI),
    path('home', HomeView.as_view()),
    path('accident', AccidentView.as_view()), 
    path('userfe/', include('userfe.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
