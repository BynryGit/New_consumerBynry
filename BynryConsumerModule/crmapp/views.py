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
import string


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


def complaints(request):
    """To view complaints page"""
    try:
        print 'crmapp|views.py|complaints'
        complaint_type = ComplaintType.objects.filter(is_deleted=False)
        data = {
            'complaint_type': complaint_type
        }

    except Exception as exe:
        print 'Exception|crmapp|views.py|home', exe
        data = {}
    return render(request, 'crmapp/complaints.html', data)


def get_consumer_complaints(request):
    """to get complaint details"""
    try:
        complaint_list = []
        print 'crmapp|views.py|get_consumer_complaint_details'
        # filter complaint by complaint id
        consumer_id = ConsumerDetails.objects.get(consumer_no='100000123000')
        print '---------consumer------', consumer_id
        complaints_list = ComplaintDetail.objects.filter(consumer_id=consumer_id)
        # complaint detail result
        for complaints in complaints_list:
            complaint_data = {
                'complaintID': '<a onclick="complaint_details(' + str(
                    complaints.id) + ')">' + complaints.complaint_no + '</a>',
                'complaintType': complaints.complaint_type_id.complaint_type,
                'closureRemark': complaints.remark,
                'complaintDate': complaints.created_on.strftime('%B %d, %Y %I:%M %p'),
                'complaintStatus': complaints.complaint_status
            }
            complaint_list.append(complaint_data)
        data = {'success': 'true', 'data': complaint_list}

    except Exception as exe:
        print 'Exception|crmapp|views.py|get_consumer_complaint_details', exe
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


def get_complaint_details(request):
    """to get complaint details"""
    try:
        print 'crmapp|views.py|get_complaint_details'
        # filter complaint by complaint id
        complaints = ComplaintDetail.objects.get(
            id=request.GET.get('complaint_id'))

        # complaint detail result
        complaint_detail = {
            'complaintID' : complaints.complaint_no,
            'complaintType' : complaints.complaint_type_id.complaint_type,
            'complaintConsumerName' : complaints.consumer_id.name,
            'complaintConsumerNo' : complaints.consumer_id.consumer_no,
            'complaintStatus' : complaints.complaint_status if complaints.complaint_status else '',
            'consumerRemark' : complaints.remark if complaints.remark else '',
            'closureRemark' : complaints.closure_remark,
        }
        data = {'success' : 'true', 'complaintDetail' : complaint_detail}
    except Exception as exe:
        print 'Exception|crmapp|views.py|get_complaint_details', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_complaint_details(request):
    """to get complaint details"""
    try:
        print 'selfserviceapp|views.py|save_consumer_complaint_details'
        complaint_type_obj = ComplaintType.objects.get(id=request.GET.get('complaint_type'))
        # filter complaint by complaint id
        chars = string.digits
        pwdSize = 5
        password = ''.join(random.choice(chars) for _ in range(pwdSize))
        consumer_id = ConsumerDetails.objects.get(consumer_no='100000123000')# if request.session[
            #'consumer_id'] else None

        complaint_obj = ComplaintDetail(
            complaint_no="COMP" + str(password),
            complaint_type_id=complaint_type_obj,
            consumer_id=consumer_id,
            remark=request.GET.get('complaint_remark'),
            complaint_img=request.GET.get('complaint_img'),
            complaint_source="CTI",
            complaint_status="Open",
            complaint_date=datetime.now()
        )
        complaint_obj.save()

        data = {'success': 'true', 'complaint_id': str(complaint_obj)}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|save_consumer_complaint_details', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def services(request):
    """To view services page"""
    try:
        print 'crmapp|views.py|services'
        consumer_id = request.session['consumer_id']
        serviceType = ServiceRequestType.objects.filter(is_deleted=False)  # Service Types
        data = {'serviceType': serviceType, 'consumer_id': consumer_id}
    except Exception as exe:
        print 'Exception|crmapp|views.py|services', exe
        data = {}
    return render(request, 'crmapp/services.html', data)


def vigilance(request):
    """To view vigilance page"""
    try:
        print 'crmapp|views.py|vigilance'
        vigilance_type = VigilanceType.objects.filter(is_deleted=False)
        data = {'vigilance_type': vigilance_type, 'city_list': get_city(request), 'pincode_list': get_pincode(request)}

    except Exception as exe:
        print 'Exception|crmapp|views.py|vigilance', exe
        data = {}
    return render(request, 'crmapp/vigilance.html', data)    
