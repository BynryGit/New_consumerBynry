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
from vigilanceapp.models import VigilanceType, VigilanceDetail
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
        request.session['consumer_no'] = ''
        request.session['consumer_data_id'] = ''
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
        request.session['consumer_no'] = consumer_obj.consumer_no
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
    return HttpResponse(json.dumps(data), content_type='application/json')


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
        consumer_id = ConsumerDetails.objects.get(consumer_no=request.session['consumer_no'])
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
        consumer_data_obj = c_obj.id
        request.session['consumer_data_id'] = consumer_data_obj

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
        consumer_id = ConsumerDetails.objects.get(consumer_no=request.session['consumer_no'])# if request.session[
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
        serviceType = ServiceRequestType.objects.filter(is_deleted=False)  # Service Types
        data = {'serviceType': serviceType}
    except Exception as exe:
        print 'Exception|crmapp|views.py|services', exe
        data = {}
    return render(request, 'crmapp/services.html', data)


def service_request(request):
    """to get service details"""
    try:
        print 'crmapp|views.py|service_request'
        # filter complaint by service id

        consumer_id = ConsumerDetails.objects.get(consumer_no=request.session['consumer_no'])

        service_type = ServiceRequestType.objects.get(id=request.GET.get('service_type'))
        chars = string.digits
        pwdSize = 5
        password = ''.join(random.choice(chars) for _ in range(pwdSize))

        service_obj = ServiceRequest(
            service_no="SERVICE" + str(password),
            service_type=service_type,
            consumer_id=consumer_id,
            consumer_remark=request.GET.get('service_remark'),
            source="CTI",
            request_date=datetime.now(),
            created_date=datetime.now()
        )
        service_obj.save()
        service_no = service_obj.service_no

        data = {'success': 'true', 'service_no': service_no}
    except Exception as exe:
        print 'Exception|crmapp|views.py|service_request', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


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


def bills(request):
    """To view bills page"""
    data = {}
    try:
        print 'crmapp|views.py|bills'
    except Exception as exe:
        print 'Exception|crmapp|views.py|bills', exe
    return render(request, 'crmapp/bills.html', data)


def get_bill_history(request):
    try:
        print 'crmapp|views.py|get_bill_history'
        final_list = []
        month_list1 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_list2 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

        try:
            consumer_obj = ConsumerDetails.objects.get(consumer_no=request.session['consumer_no'])
            pay_list = PaymentDetail.objects.filter(consumer_id=consumer_obj)
            for pay_obj in pay_list:
                bill_month = pay_obj.meter_reading_id.bill_month
                bill_month = month_list1[
                                 month_list2.index(bill_month)] + '-' + pay_obj.meter_reading_id.bill_months_year
                action = '<a target="_blank" href="/cti-crm/view-bill/?meter_reading_id=' + str(
                    pay_obj.id) + '"> <i class="fa fa-eye" aria-hidden="true"></i> </a>'
                data_list = {
                    'bill_month': bill_month,
                    'unit_consumed': pay_obj.meter_reading_id.unit_consumed,
                    'net_amount': str(pay_obj.net_amount),
                    'bill_amount_paid': str(pay_obj.bill_amount_paid),
                    'payment_date': pay_obj.payment_date.strftime("%d %b %Y"),
                    'action': action
                }
                final_list.append(data_list)
        except Exception, e:
            print 'Exception|crmapp|views.py|get_bill_history', e
            pass
        data = {'success': 'true', 'data': final_list}

    except Exception as exe:
        print 'Exception|crmapp|views.py|get_bill_history', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def view_bill(request):
    """To view FAQS page"""
    try:
        print 'crmapp|views.py|view_bill'
        last_receipt_date = '--'
        last_receipt_amount = '0.00'
        month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        meter_obj = MeterReadingDetail.objects.get(id=request.GET.get('meter_reading_id'))
        consumer_obj = ConsumerDetails.objects.get(consumer_no=meter_obj.consumer_id.consumer_no)
        meter_object = MeterReadingDetail.objects.filter(consumer_id=consumer_obj)
        if meter_object.count() > 1:
            prev_meter_obj = meter_object[0]
            try:
                payment_obj = PaymentDetail.objects.get(meter_reading_id=prev_meter_obj)
                last_receipt_date = payment_obj.created_on.strftime('%d %b %Y')
                last_receipt_amount = payment_obj.bill_amount_paid
            except:
                pass

        if meter_obj.bill_unit and meter_obj.adjusted_unit:
            total_reading = int(meter_obj.bill_unit) - int(meter_obj.adjusted_unit)
        else:
            total_reading = meter_obj.bill_unit

        total_charges = meter_obj.fixed_charges + meter_obj.energy_charges + meter_obj.electricity_duty + meter_obj.wheeling_charges + meter_obj.fuel_adjustment_charges + meter_obj.additional_supply_charges + meter_obj.tax_on_sale - meter_obj.previous_bill_credit + meter_obj.current_interest + meter_obj.capacitor_penalty + meter_obj.other_charges
        total_arrears = meter_obj.net_arrears + meter_obj.adjustments_arrears + meter_obj.interest_arrears
        net_bill_amount = total_charges + total_arrears

        if meter_obj.meter_reading_image:
            image_address = "http://" + get_current_site(request).domain + meter_obj.meter_reading_image.url
        else:
            image_address = ''

        data = {
            'con_number': consumer_obj.consumer_no,
            'con_name': consumer_obj.name,
            'con_address': consumer_obj.name,
            'con_bill_cycle': consumer_obj.bill_cycle.bill_cycle_code,
            'route': consumer_obj.route.route_code,
            'category': consumer_obj.meter_category,
            'sanct_load': consumer_obj.sanction_load,
            'conn_load': consumer_obj.connection_load if consumer_obj.connection_load else '0 KW',
            'pole_no': consumer_obj.pole_no,
            'dtc': consumer_obj.dtc,
            'supply_date': consumer_obj.meter_connection_date.strftime('%d %b %Y'),
            'meter_no': consumer_obj.meter_no,
            'meter_image': image_address,
            'current_reading': meter_obj.current_month_reading,
            'previous_reading': meter_obj.previous_month_reading,
            'total_reading': total_reading,
            'bill_date': meter_obj.created_on.strftime('%d %b %Y'),
            'con_bill_month': month_list[int(meter_obj.bill_month) - 1] + ' ' + str(meter_obj.bill_months_year),
            'current_amount': str(meter_obj.bill_amount),
            'prev_due': str(meter_obj.due_amount),
            'net_amount': str(meter_obj.net_amount),
            'due_date': meter_obj.due_date.strftime('%d %b %Y'),
            'prompt_date': meter_obj.prompt_date.strftime('%d %b %Y'),
            'prompt_amount': str(meter_obj.prompt_amount),
            'processing_cycle': meter_obj.processing_cycle,
            'meter_reader': meter_obj.meter_reader,
            'tariff': meter_obj.tariff,
            'bill_unit': meter_obj.bill_unit,
            'adjusted_unit': meter_obj.adjusted_unit,
            'bill_amount_after_due_date': meter_obj.bill_amount_after_due_date,
            'fixed_charges': meter_obj.fixed_charges,
            'energy_charges': meter_obj.energy_charges,
            'electricity_duty': meter_obj.electricity_duty,
            'wheeling_charges': meter_obj.wheeling_charges,
            'fuel_adjustment_charges': meter_obj.fuel_adjustment_charges,
            'additional_supply_charges': meter_obj.additional_supply_charges,
            'tax_on_sale': meter_obj.tax_on_sale,
            'previous_bill_credit': meter_obj.previous_bill_credit,
            'current_interest': meter_obj.current_interest,
            'capacitor_penalty': meter_obj.capacitor_penalty,
            'other_charges': meter_obj.other_charges,
            'net_arrears': meter_obj.net_arrears,
            'adjustments_arrears': meter_obj.adjustments_arrears,
            'interest_arrears': meter_obj.interest_arrears,
            'bill_period': meter_obj.previous_month_reading_date.strftime(
                '%d %b %Y') + ' - ' + meter_obj.current_reading_date.strftime('%d %b %Y'),
            'total_charges': total_charges,
            'total_arrears': total_arrears,
            'net_bill_amount': net_bill_amount,
            'rounded_bill_amount': str(round(net_bill_amount, 0)) + '0',
            'bill_status': meter_obj.bill_status,
            'last_receipt_date': last_receipt_date,
            'last_receipt_amount': last_receipt_amount,
        }
    except Exception as exe:
        print 'Exception|crmapp|views.py|view_bill', exe
        data = {}
    return render(request, 'crmapp/view_bill.html', data)

@csrf_exempt
def save_vigilance_complaint(request):
    try:
        print 'crmapp|views.py|save_vigilance_complaint'
        chars = string.digits
        pwdSize = 5
        password = ''.join(random.choice(chars) for _ in range(pwdSize))
        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.POST.get('consumer_no'))
    
        new_vigilance_obj = VigilanceDetail(
            case_id="CASE" + str(password),
            consumer_id=ConsumerDetails.objects.get(
                id=consumer_obj.id) if consumer_obj.id else None,
            vigilance_type_id=VigilanceType.objects.get(
                id=request.POST.get('vigilance_type')) if request.POST.get(
                'vigilance_type') else None,
            theft_name=request.POST.get('consumer_name'),
            address=request.POST.get('consumer_address'),
            city=City.objects.get(
                id=request.POST.get('city')) if request.POST.get(
                'city') else None,
            pin_code=Pincode.objects.get(
                id=request.POST.get('pincode')) if request.POST.get(
                'pincode') else None,
            vigilance_remark=request.POST.get('vigilance_remark'),  # Need to change logic
            vigilance_source='CTI',
            vigilance_status='Open',
            created_on=datetime.now(),
            created_by='CTI',
        );
        new_vigilance_obj.save();

        data = {
            'success': 'true',
            'message': 'Vigilance complaint created successfully.'
        }
    except Exception, e:
        print 'Exception|crmapp|views.py|save_vigilance_complaint', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')
