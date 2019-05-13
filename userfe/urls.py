# howdy/urls.py
from django.urls import path
from userfe import views


urlpatterns = [
	path('faq/', views.faq, name='faq'),
	path('book/', views.book, name='book'),
	path('login/', views.login, name='login'),
	path('help/', views.help, name='help'),
	path('navigate/', views.navigate, name='navigate'),
	path('', views.countSlot),
]