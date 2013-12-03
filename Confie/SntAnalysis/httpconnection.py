import sys
import requests
import json
from requests import session

#url = "http://127.0.0.1:8000/"

def Home_Connect(data):
   print "HomeConnect"
   return requests.post(url, data)
