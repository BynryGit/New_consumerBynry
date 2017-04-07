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

@csrf_exempt
def verify_new_consumer(request):
    """to get verify_new_consumer"""
    try:
        print 'crmapp|views.py|verify_new_consumer'

        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.POST.get('consumer_no'),
                                                   city=request.POST.get('city_id'))
        print '--------cons no-----',consumer_obj.consumer_no
        if consumer_obj:
            c_obj = ConsumerData(
                consumer_no=consumer_obj,
                name = consumer_obj.name,
                email_id = consumer_obj.email_id,
                contact_no = consumer_obj.contact_no,
                city = consumer_obj.city,
                is_registered = 'True'
            )
            c_obj.save()
            data = {'success': 'true',
                    'consumer_no' : consumer_obj.consumer_no,
                    'consumer_name' : consumer_obj.name,
                    'mobile_number' : consumer_obj.contact_no,
                    'email_id' : consumer_obj.email_id
                    }
        else:
            data = {'success': 'false'}

    except Exception as exe:
        print 'Exception|crmapp|views.py|verify_new_consumer', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_new_consumer(request):
    """to get verify_new_consumer"""
    try:
        print 'crmapp|views.py|save_new_consumer'
        city_objs = City.objects.get(id=request.POST.get('city'))
        c_obj = ConsumerData(
            name = request.POST.get('name'),
            email_id = request.POST.get('email'),
            contact_no = request.POST.get('contact_no'),
            city = city_objs,
            is_registered = 'False'
        )
        c_obj.save()
        data = {'success': 'true'}
    except Exception as exe:
        print 'Exception|crmapp|views.py|save_new_consumer', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')