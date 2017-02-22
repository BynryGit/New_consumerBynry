from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
import urllib
import smtplib
from smtplib import SMTPException
from django.shortcuts import *

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb

# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect



def dashboard(request):
    return render(request, 'dashboard.html')

def consumer_list(request):
    print '---------hi---------'
    return render(request, 'consumer_list.html')    

def complaints(request):
    print '---------hi---------'
    return render(request, 'complaints.html')

def services(request):
    print '---------hi---------'
    return render(request, 'services.html')

#vigilance_cases
def vigilance_cases(request):
    print '---------hi---------'
    return render(request, 'vigilance_cases.html')

