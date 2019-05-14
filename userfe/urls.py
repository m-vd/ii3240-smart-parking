# howdy/urls.py
from django.urls import path
from userfe import views


urlpatterns = [
	path('faq/', views.faq, name='faq'),
	path('book/', views.inputBook),
	path('login/', views.login, name='login'),
	path('help/', views.inputHelp),
	path('navigate/', views.navigate, name='navigate'),
	path('', views.countSlot),
]