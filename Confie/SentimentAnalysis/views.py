from __future__ import division
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.http import HttpResponse
from django.template import RequestContext
import httpconnection
from django.db import IntegrityError
from django.core.context_processors import csrf
from blog.models import posts
import requests
import json
import sys
import nltk
from nltk.corpus import stopwords
from twython import Twython, TwythonError,TwythonStreamer


def my_view(request):
    c = {}
    c.update(csrf(request))
    # ... view code here
    return render_to_response("index.html", c)


def index(request):
	try:
            if request.POST:
            	strConference = request.POST.get('keyword')  
		return render_to_response('index.html')

	    else:
                	return render_to_response('index.html')
	except IntegrityError,e:
        		return render_to_response('error.html')
