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
        complaints = ComplaintDetail.objects.get(
            id=request.GET.get('complaint_id'))
        # complaint image path with server url
        image_address = "http://" + get_current_site(request).domain \
                        + "/" + complaints.complaint_img.url

        # complaint detail result
        complaint_detail = {
            'complaintID' : complaints.complaint_no,
            'complaintType' : complaints.complaint_type_id.complaint_type,
            'complaintConsumerName' : complaints.consumer_id.name,
            'complaintConsumerNo' : complaints.consumer_id.consumer_no,
            'complaintStatus' : complaints.complaint_status,
            'consumerRemark' : complaints.remark,
            'closureRemark' : complaints.closure_remark,
            'complaint_img' : image_address,
        }
        data = {'success' : 'true', 'complaintDetail' : complaint_detail}
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
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|services', exe
        data = {}
    return render(request, 'self_service/services.html', data)


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
