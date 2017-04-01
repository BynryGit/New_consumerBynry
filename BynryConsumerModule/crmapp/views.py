__auther__ = "Swapnil Kadu"
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from BynryConsumerModuleapp.models import Zone, BillCycle, RouteDetail, Branch
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
from consumerapp.views import get_city, get_billcycle, get_pincode
from consumerapp.models import *
from complaintapp.models import ComplaintType, ComplaintDetail, ComplaintImages
from selfserviceapp.models import WebUserProfile
from serviceapp.models import ServiceRequestType, ServiceRequest
from vigilanceapp.models import VigilanceType
from django.views.decorators.csrf import csrf_exempt
import urllib2
import random
from crmapp import *

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
# importing mysqldb and system packages
import MySQLdb, sys
from .models import *
from paymentapp.models import *


def home(request):
    """To view complaints page"""
    try:
        print 'crmapp|views.py|home'
        data = {
            'city_list': get_city(request)
        }

    except Exception as exe:
        print 'Exception|crmapp|views.py|home', exe
        data = {}
    return render(request, 'crmapp/home.html', data)

