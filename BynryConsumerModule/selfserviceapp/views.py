__auther__ = "Vikas Kumawat"
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from BynryConsumerModuleapp.models import Zone, BillCycle, RouteDetail, Branch
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
from consumerapp.views import get_city, get_billcycle
from consumerapp.models import *
from complaintapp.models import ComplaintType, ComplaintDetail
from serviceapp.models import ServiceRequestType, ServiceRequest
from django.views.decorators.csrf import csrf_exempt
import urllib2
import random


def home_screen(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|home_screen'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|home_screen', exe
        data = {}
    return render(request, 'self_service/home_screen.html', data)


def register_new_user(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|register_new_user'
        data = {
            'city_list': get_city(request)
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|register_new_user', exe
        data = {}
    return render(request, 'self_service/register_new_user.html', data)


def my_bills(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|my_bills'
        
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|my_bills', exe
        data = {}
    return render(request, 'self_service/my_bills.html', data)


def manage_accounts(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|manage_accounts'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|manage_accounts', exe
        data = {}
    return render(request, 'self_service/manage_accounts.html', data)


def add_new_account(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|add_new_account'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|add_new_account', exe
        data = {}
    return render(request, 'self_service/add_new_account.html', data)


def complaints(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|complaints'
        complaint_type =  ComplaintType.objects.filter(is_deleted=False)
        data={'complaint_type':complaint_type}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|complaints', exe
        data = {}
    return render(request, 'self_service/complaints.html', data)



@login_required(login_url='/')
def save_consumer_complaint_details(request):
    """to get complaint details"""
    try:
        print 'selfserviceapp|views.py|get_complaint_details'
        # filter complaint by complaint id
        complaint_obj = ComplaintDetail(
            complaint_no=request.GET.get('id'),
            complaint_type_id=request.GET.get('complaint_type'),
            consumer_id=request.GET.get('consumer_id'),
            remark=request.GET.get('remark'),
            complaint_img=request.GET.get('complaint_img'),
            complaint_source="Web Portal",
            complaint_date=datetime.now()
            )
        complaint_obj.save()

        data = {'success' : 'true'}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_complaint_details', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_consumer_complaint_details(request):
    """to get complaint details"""
    try:
        print 'selfserviceapp|views.py|get_consumer_complaint_details'
        # filter complaint by complaint id
        complaints = ComplaintDetail.objects.get(consumer_id=request.GET.get('consumer_id'))

        # complaint detail result
        complaint_detail = {
            'complaintID' : complaints.complaint_no,
            'complaintType' : complaints.complaint_type_id.complaint_type,
            'complaintStatus' : complaints.complaint_status,
            'complaintDate' : complaints.created_on.strftime('%B %d, %Y %I:%M %p'),
            'closureRemark' : complaints.closure_remark,
        }
        data = {'success' : 'true', 'complaintDetail' : complaint_detail}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_consumer_complaint_details', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def services(request):
    """To view services page"""
    try:
        print 'selfserviceapp|views.py|services'
        serviceType = ServiceRequestType.objects.filter(is_deleted=False) # Service Types
        data={'serviceType':serviceType}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|services', exe
        data = {}
    return render(request, 'self_service/services.html', data)

def service_request(request):
    """to get complaint details"""
    try:
        print 'selfserviceapp|views.py|service_request'
        # filter complaint by complaint id
        service = ServiceRequest.objects.get(consumer_id=request.GET.get('consumer_id'))

        service_obj = ServiceRequest(
            service_no=request.GET.get('id'),
            service_type=request.GET.get('service_type'),
            consumer_id=request.GET.get('consumer_id'),
            remark=request.GET.get('remark'),
            service_source="Web Portal",
            service_date=datetime.now()
            )
        service_obj.save()

        service_no = service_obj.service_no

        data = {'success' : 'true', 'service_no' : service_no}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|service_request', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def login(request):
    print 'selfserviceapp|views.py|login'
    return render(request, 'self_service/login.html')


def contact_us(request):
    print 'selfserviceapp|views.py|contact_us'
    return render(request, 'self_service/contact_us.html')


def quick_pay(request):
    print 'selfserviceapp|views.py|quick_pay'
    data = {
        'bill_cycle_list': get_billcycle(request)
    }
    return render(request, 'self_service/quick_pay.html', data)


def my_tariff(request):
    print 'selfserviceapp|views.py|my_tariff'
    return render(request, 'self_service/my_tariff.html')


def get_consumer_bill_data(request):
    try:
        consumer_no = request.GET.get('consumer_number')
        consumer_type = request.GET.get('consumer_type')
        bill_cycle = BillCycle.objects.get(id = request.GET.get('bill_cycle'))
        consumer_obj = ConsumerDetails.objects.get(consumer_no=consumer_no,bill_cycle=bill_cycle,meter_category=consumer_type)
        data = {
            'con_number': consumer_obj.consumer_no,
            'con_name': consumer_obj.name,
            'con_bill_cycle': consumer_obj.bill_cycle.bill_cycle_code,
            'con_bill_month': 'March 2017',
            'current_amount': '500.00',
            'prev_due': '0.00',
            'net_amount': '500',
            'due_date': '26/03/2017',
            'prompt_date': '23/03/2017',
            'prompt_amount': '490.00',
            'success': 'true',
        }
    except Exception, e:
        print 'Exception|selfserviceapp|views.py|get_consumer_bill_data', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

def FAQS(request):
    """To view FAQS page"""
    try:
        print 'selfserviceapp|views.py|FAQS'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|FAQS', exe
        data = {}
    return render(request, 'self_service/FAQS.html', data)


@csrf_exempt
def verify_new_consumer(request):
    """to get verify_new_consumer"""
    try:
        print 'selfserviceapp|views.py|verify_new_consumer'

        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.POST.get('consumer_no'),city=request.POST.get('city_id'))
        if consumer_obj:
            ret = u''
            ret = ''.join(random.choice('0123456789ABCDEF') for i in range(6))
            OTP = ret
            consumer_registration_sms(consumer_obj, OTP)

            consumer_obj.consumer_otp = OTP
            consumer_obj.save()
            data = {'success': 'true', 'message': 'SMS Sent Successfully','contact_no':consumer_obj.contact_no}
        else:
            data = {'success': 'false', 'message': 'Invalid Username'}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|verify_new_consumer', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def consumer_registration_sms(consumer_obj, OTP):
    # pdb.set_trace()

    # authkey = "118994AIG5vJOpg157989f23"

    # mobiles = str(consumer_obj.user_contact_no)

    # message = "Dear " + str(
    #     consumer_obj.user_first_name) + ", \n\n" + "Greetings from CityHoopla !!! \n\n" + "Click on the link below to reset your password!!!" + "\n" + SERVER_URL + "/reset-password/?user_id=" + str(
    #     consumer_obj.user_id) + "\n\n" + "Best Wishes," + '\n' + "Team CityHoopla "
    # sender = "CTHPLA"
    # route = "4"
    # country = "91"
    # values = {
    #     'authkey': authkey,
    #     'mobiles': mobiles,
    #     'message': message,
    #     'sender': sender,
    #     'route': route,
    #     'country': country
    # }

    # url = "http://api.msg91.com/api/sendhttp.php"
    # postdata = urllib.urlencode(values)
    # req = urllib2.Request(url, postdata)
    # response = urllib2.urlopen(req)
    # output = response.read()
    # print output
    return 1
