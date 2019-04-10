from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:parkID>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:parkID>/checkin/', views.checkIn, name='checkIn'),
    # ex: /polls/5/vote/
    path('<int:parkID>/checkout/', views.checkOut, name='checkOut'),
    path('record', views.record, name='record')
]