from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
#	return HttpResponse("Hello")
	context = None;
	return render(request, 'userfe/index.html', context)
def faq(request):
	context = None;
	return render(request, 'userfe/faq.html', context)
	
def book(request):
	context = None;
	return render(request, 'userfe/book.html', context)
	
def login(request):
	context = None;
	return render(request, 'userfe/login.html', context)
	
def help(request):
	context = None;
	return render(request, 'userfe/help.html', context)
	
def navigate(request):
	context = None;
	return render(request, 'userfe/navigate.html', context)