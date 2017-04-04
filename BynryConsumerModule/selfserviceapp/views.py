__auther__ = "Vikas Kumawat"
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
from selfserviceapp.models import WebUserProfile, UserAccount
from serviceapp.models import ServiceRequestType, ServiceRequest
from vigilanceapp.models import VigilanceType, VigilanceDetail, ConsumerVigilanceImage
from django.views.decorators.csrf import csrf_exempt
import urllib2
import random

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

def bill_calculator(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|bill_calculator'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|bill_calculator', exe
        data = {}
    return render(request, 'self_service/bill_calculator.html', data)

def consumption_calculator(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|consumption_calculator'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|consumption_calculator', exe
        data = {}
    return render(request, 'self_service/consumption_calculator.html', data)

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

def add_NSC(request):
    """To view NSC page"""
    try:
        print 'selfserviceapp|views.py|add_NSC'
        data = {

            'city_list': get_city(request),
            'pincode_list': get_pincode(request)
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|add_NSC', exe
        data = {}
    return render(request, 'self_service/add_NSC.html', data)    


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

        consumer_obj = MeterReadingDetail.objects.filter(consumer_id=request.session['consumer_id']).latest('created_on')
        if consumer_obj.bill_status == 'Paid' :
            payment_date = PaymentDetail.objects.get(meter_reading_id=consumer_obj.id).payment_date
        else :
            payment_date = ''
        data = {
            'consumer_no':consumer_obj.consumer_id.consumer_no,
            'name':consumer_obj.consumer_id.name,
            'bill_cycle':consumer_obj.consumer_id.bill_cycle.bill_cycle_name,
            'unit_consumed':consumer_obj.unit_consumed,
            'bill_amount':consumer_obj.bill_amount,
            'arrears':consumer_obj.arrears,
            'net_amount':consumer_obj.net_amount,
            'payment_date':payment_date,
            'prompt_date':consumer_obj.prompt_date,
            'due_date':consumer_obj.due_date
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|my_bills', exe
        data = {}
    return render(request, 'self_service/my_bills.html', data)

def get_graph1_data(request):
    try:
        print 'selfserviceapp|views.py|get_graph1_data'
        data_list = []
        ss = ['Month', 'Units']
        data_list.append(ss)

        month_list1 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_list2 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        pre_Date = datetime.now()
        pre_Month = pre_Date.month
        pre_Year = pre_Date.year
        for i in range(6):
            last_Year = pre_Year
            last_Month = pre_Month - i
            if last_Month <= 0:
                last_Month = 12 + last_Month
                last_Year = pre_Year -1
            try:
                reading_obj = MeterReadingDetail.objects.get(consumer_id=request.session['consumer_id'],bill_month=month_list2[last_Month-1],bill_months_year=last_Year)
                ss = [month_list1[last_Month-1], reading_obj.unit_consumed]
                data_list.append(ss)
            except Exception, e:
                ss = [month_list1[last_Month-1], 0]
                data_list.append(ss)
                pass
            
        data = {'success': 'true','data_list':data_list}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_graph1_data', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_graph2_data(request):
    try:
        print 'selfserviceapp|views.py|get_graph2_data'
        data_list = []
        ss = ['Month', 'Rs.']
        data_list.append(ss)

        month_list1 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_list2 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        pre_Date = datetime.now()
        pre_Month = pre_Date.month
        pre_Year = pre_Date.year
        for i in range(6):
            last_Year = pre_Year
            last_Month = pre_Month - i
            if last_Month <= 0:
                last_Month = 12 + last_Month
                last_Year = pre_Year -1
            try:
                reading_obj = MeterReadingDetail.objects.get(consumer_id=request.session['consumer_id'],bill_month=month_list2[last_Month-1],bill_months_year=last_Year)
                pay_obj = PaymentDetail.objects.get(meter_reading_id=reading_obj.id)
                if pay_obj.bill_status == 'Paid':
                    ss = [month_list1[last_Month-1], pay_obj.net_amount]
                    data_list.append(ss)
            except Exception, e:
                ss = [month_list1[last_Month-1], 0]
                data_list.append(ss)
                pass
            
        data = {'success': 'true','data_list':data_list}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_graph2_data', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_bill_history(request):
    try:
        print 'selfserviceapp|views.py|get_bill_history'
        final_list = []
        month_list1 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_list2 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

        try:
            pay_list = PaymentDetail.objects.filter(consumer_id=request.session['consumer_id'])
            for pay_obj in pay_list:
                bill_month = pay_obj.meter_reading_id.bill_month
                bill_month = month_list1[month_list2.index(bill_month)] + '-' + pay_obj.meter_reading_id.bill_months_year       
                action = '<a target="_blank" href="/self-service/view-bill/?meter_reading_id='+str(pay_obj.id)+'"> <i class="fa fa-eye" aria-hidden="true"></i> </a>'
                data_list = {
                    'bill_month':bill_month,
                    'unit_consumed':pay_obj.meter_reading_id.unit_consumed,
                    'net_amount':str(pay_obj.net_amount),
                    'bill_amount_paid':str(pay_obj.bill_amount_paid),
                    'payment_date':pay_obj.payment_date.strftime("%d %b %Y"),
                    'action':action
                }
                final_list.append(data_list)
        except Exception, e:
            print 'Exception|selfserviceapp|views.py|get_bill_history',e
            pass
        data = {'success': 'true','data':final_list}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_bill_history', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_pay_history(request):
    try:
        print 'selfserviceapp|views.py|get_pay_history'
        final_list = []
        try:
            pay_list = PaymentDetail.objects.filter(consumer_id=request.session['consumer_id'])
            for pay_obj in pay_list:                
                data_list = {
                    'bank_id':pay_obj.bank_id,
                    'reference_no':pay_obj.reference_no,
                    'due_date':pay_obj.due_date.strftime("%d %b %Y"),
                    'payment_date':pay_obj.payment_date.strftime("%d %b %Y"),
                    'bill_amount_paid':str(pay_obj.bill_amount_paid)
                }
                final_list.append(data_list)
        except Exception, e:
            print 'Exception|selfserviceapp|views.py|get_pay_history',e
            pass
        data = {'success': 'true','data':final_list}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_pay_history', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


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

def get_my_accounts(request):
    """To view complaints page"""
    try:
        users_list = []
        print 'selfserviceapp|views.py|get_my_accounts'
        consumer_id = ConsumerDetails.objects.get(id=request.session['consumer_id'])
        cons_id = request.session['consumer_id']
        print '-----consumer id------',consumer_id
        parent_consumer_obj = WebUserProfile.objects.get(username=consumer_id)
        users_obj = UserAccount.objects.filter(parent_consumer_no=parent_consumer_obj,is_deleted=False)
        print '--------user obj---------',users_obj
        parent_user_data = {
            'name': parent_consumer_obj.consumer_id.name,
            'user_no': parent_consumer_obj.consumer_id.consumer_no,
            'address': parent_consumer_obj.consumer_id.address_line_1+' '+parent_consumer_obj.consumer_id.address_line_2,
            'actions': '<input type="radio" onclick="select_user_account(\''+str(parent_consumer_obj.consumer_id.consumer_no)+'\',\''+str(parent_consumer_obj.consumer_id.name)+'\');" name="Select User" value=' + str(parent_consumer_obj.id) + ' > &nbsp;' + '&nbsp;<a>'
        }
        users_list.append(parent_user_data)
        for users in users_obj:
            users_data = {
                'name': users.consumer_id.name,
                'user_no': users.consumer_no,
                'address': users.consumer_id.address_line_1+' '+users.consumer_id.address_line_2,
                'actions': '<input type="radio" onclick="select_user_account(\''+str(users.consumer_no)+'\',\''+str(users.consumer_id.name)+'\');" name="Select User" value=' + str(users.id) + ' > &nbsp;' + '&nbsp;<a> <i class="fa fa-trash" aria-hidden="true" onclick="delete_user_account(' + str(users.id) + ');"></i> </a>'
            }
            users_list.append(users_data)
        data = {'success': 'true','data':users_list}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_my_accounts', exe
        data = {}
    return HttpResponse(json.dumps(data), content_type='application/json')

def activate_user_account(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|activate_user_account'
        user_obj = UserAccount.objects.get(consumer_no=request.GET.get('consumer_no'))
        print '--------user obj---------',user_obj.consumer_id.consumer_no
        request.session['consumer_id'] = user_obj.consumer_id.consumer_id
        request.session['consumer_no'] = user_obj.consumer_id.consumer_no

        data = {'success': 'true'}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|activate_user_account', exe
        data = {}
    return HttpResponse(json.dumps(data), content_type='application/json')

def delete_user_account(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|delete_user_account'
        user_obj = UserAccount.objects.get(id=request.GET.get('consumer_no'))
        print '--------user obj---------',user_obj
        user_obj.is_deleted='True'
        user_obj.save()

        data = {'success': 'true'}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|delete_user_account', exe
        data = {}
    return HttpResponse(json.dumps(data), content_type='application/json')

def add_new_account(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|add_new_account'
        data = {
            'bill_cycle_list': get_billcycle(request)
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|add_new_account', exe
        data = {}
    return render(request, 'self_service/add_new_account.html', data)


def complaints(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|complaints'
        complaint_type = ComplaintType.objects.filter(is_deleted=False)
        data = {'complaint_type': complaint_type}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|complaints', exe
        data = {}
    return render(request, 'self_service/complaints.html', data)

def vigilance(request):
    """To view vigilance page"""
    try:
        print 'selfserviceapp|views.py|vigilance'
        vigilance_type =  VigilanceType.objects.filter(is_deleted=False)
        data={'vigilance_type':vigilance_type,'city_list': get_city(request),'pincode_list': get_pincode(request)}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|vigilance', exe
        data = {}
    return render(request, 'self_service/vigilance.html', data)

@login_required(login_url='/')
def save_consumer_complaint_details(request):
    """to get complaint details"""
    try:
        print 'selfserviceapp|views.py|save_consumer_complaint_details'
        complaint_type_obj = ComplaintType.objects.get(id=request.GET.get('complaint_type'))
        # filter complaint by complaint id
        chars = string.digits
        pwdSize = 5
        password = ''.join(random.choice(chars) for _ in range(pwdSize))
        consumer_id = ConsumerDetails.objects.get(id=request.session['consumer_id']) if request.session['consumer_id'] else None

        complaint_obj = ComplaintDetail(
            complaint_no= "COMP" + str(password),
            complaint_type_id=complaint_type_obj,
            consumer_id=consumer_id,
            remark=request.GET.get('remark'),
            complaint_img=request.GET.get('complaint_img'),
            complaint_source="Web",
            complaint_date=datetime.now()
        )
        complaint_obj.save()

        attachment_list = request.GET.get('attachments')
        save_attachments1(attachment_list, complaint_obj)

        data = {'success' : 'true','complaint_id':str(complaint_obj)}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|save_consumer_complaint_details', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}

    return HttpResponse(json.dumps(data), content_type='application/json')


def get_consumer_complaint_details(request):
    """to get complaint details"""
    try:
        complaint_list = []
        print 'selfserviceapp|views.py|get_consumer_complaint_details'
        # filter complaint by complaint id
        consumer_id = ConsumerDetails.objects.get(id=request.session['consumer_id']) if request.session['consumer_id'] else None
        print '---------consumer------',consumer_id
        complaints_list = ComplaintDetail.objects.filter(consumer_id=consumer_id)
        # complaint detail result
        for complaints in complaints_list:
            complaint_data = {
                'complaintID': complaints.complaint_no,
                'complaintType': complaints.complaint_type_id.complaint_type,
                'complaintStatus': complaints.complaint_status,
                'complaintDate': complaints.created_on.strftime('%B %d, %Y %I:%M %p'),
                'closureRemark': complaints.closure_remark,
            }
            complaint_list.append(complaint_data)
        data = {'success': 'true','data':complaint_list}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|get_consumer_complaint_details', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def upload_complaint_img(request):
    try:
        print 'selfserviceapp|views.py|upload_complaint_img'
        if request.method == 'POST':
            attachment_file = ComplaintImages()
            attachment_file.save()

            request.FILES['file[]'].name = 'complaintImgID_' + str(attachment_file.id) + '_' + request.FILES[
                'file[]'].name
            attachment_file.document_files = request.FILES['file[]']
            attachment_file.save()
            data = {'success': 'true', 'attachid': attachment_file.id}
        else:
            data = {'success': 'false'}
    except MySQLdb.OperationalError, e:
        print 'Exception|selfserviceapp|views.py|upload_complaint_img', e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def remove_complaint_img(request):
    try:
        print 'selfserviceapp|views.py|remove_complaint_img'
        image_id = request.GET.get('image_id')
        image = ComplaintImages.objects.get(id=image_id)
        image.delete()

        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        print 'Exception|selfserviceapp|views.py|remove_complaint_img', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_attachments1(attachment_list, complaint_obj):
    try:
        print 'selfserviceapp|views.py|save_attachments'
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        for attached_id in attachment_list:
            attachment_obj = ComplaintImages.objects.get(id=attached_id)
            attachment_obj.consumer_id = complaint_obj.consumer_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception|selfserviceapp|views.py|save_attachments', e
    return HttpResponse(json.dumps(data), content_type='application/json')




def services(request):
    """To view services page"""
    try:
        print 'selfserviceapp|views.py|services'
        consumer_id = request.session['consumer_id']
        serviceType = ServiceRequestType.objects.filter(is_deleted=False)  # Service Types
        data = {'serviceType': serviceType,'consumer_id':consumer_id}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|services', exe
        data = {}
    return render(request, 'self_service/services.html', data)


def service_request(request):
    """to get complaint details"""
    try:
        print 'selfserviceapp|views.py|service_request'
        # filter complaint by complaint id
        consumer_id = ConsumerDetails.objects.get(id=request.GET.get('consumer_id'))
        print '----request-----',request.GET.get('service_type')
        service_type = ServiceRequestType.objects.get(id=request.GET.get('service_type'))
        chars = string.digits
        pwdSize = 5
        password = ''.join(random.choice(chars) for _ in range(pwdSize))

        service_obj = ServiceRequest(
            service_no="SERVICE" + str(password),
            service_type=service_type,
            consumer_id=consumer_id,
            consumer_remark=request.GET.get('service_remark'),
            source="Web",
            request_date=datetime.now(),
            created_date=datetime.now()
        )
        service_obj.save()
        service_no = service_obj.service_no
        print '------service no-----',service_no

        data = {'success': 'true', 'service_no': service_no}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|service_request', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def log_in(request):
    logout(request)
    print 'selfserviceapp|views.py|login'
    return render(request, 'self_service/login.html')

def log_out(request):
    logout(request)
    print 'selfserviceapp|views.py|logout'
    return render(request, 'self_service/home_screen.html')

@csrf_exempt
def signin(request):
    data = {}
    try:
        if request.POST:
            print 'logs: login request with: ', request.POST
            username = request.POST['username']
            password = request.POST['password']
            try:
                user_obj = WebUserProfile.objects.get(username=username)
                try:
                    user = authenticate(username=username, password=password)
                    if user:
                        if user.is_active:
                            user_profile_obj = WebUserProfile.objects.get(username=username)
                            # request.session['user_role'] = user_profile_obj.user_role.role_name
                            try:
                                request.session['login_user'] = user_profile_obj.consumer_id.name
                                request.session['consumer_id'] = int(user_profile_obj.consumer_id.id)
                                request.session['consumer_no'] = user_profile_obj.consumer_id.consumer_no
                                login(request, user)
                            except Exception as e:
                                print e
                            data = {'success': 'true'}
                        else:
                            data = {'success': 'false', 'message': 'User Is Not Active'}
                            return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        data = {'success': 'Invalid Password', 'message': 'Invalid Password'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except Exception as e:
                    print e
                    data = {'success': 'Invalid Username', 'message': 'Invalid Username'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            except Exception as e:
                print e
                data = {'success': 'Invalid Username', 'message': 'Invalid Username'}
                return HttpResponse(json.dumps(data), content_type='application/json')

    except MySQLdb.OperationalError, e:
        print e
        data = {'success': 'false', 'message': 'Internal server'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false', 'message': 'Invalid Username or Password'}
    return HttpResponse(json.dumps(data), content_type='application/json')


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
        bill_cycle = BillCycle.objects.get(id=request.GET.get('bill_cycle'))
        consumer_obj = ConsumerDetails.objects.get(consumer_no=consumer_no, bill_cycle=bill_cycle,
                                                   meter_category=consumer_type)
        meter_obj = MeterReadingDetail.objects.filter(consumer_id = consumer_obj,bill_status = 'Unpaid').last()
        if meter_obj:
            total_charges = meter_obj.fixed_charges + meter_obj.energy_charges + meter_obj.electricity_duty + meter_obj.wheeling_charges + meter_obj.fuel_adjustment_charges + meter_obj.additional_supply_charges + meter_obj.tax_on_sale - meter_obj.previous_bill_credit + meter_obj.current_interest + meter_obj.capacitor_penalty + meter_obj.other_charges
            total_arrears = meter_obj.net_arrears + meter_obj.adjustments_arrears + meter_obj.interest_arrears
            net_bill_amount = total_charges + total_arrears
            data = {
                'con_number': consumer_obj.consumer_no,
                'con_name': consumer_obj.name,
                'con_bill_cycle': consumer_obj.bill_cycle.bill_cycle_code,
                'con_bill_month': meter_obj.bill_month + ' ' + str(meter_obj.bill_months_year),
                'current_amount': str(total_charges),
                'prev_due': str(total_arrears),
                'net_amount': str(net_bill_amount),
                'due_date': meter_obj.due_date.strftime('%B %d, %Y'),
                'prompt_date': meter_obj.prompt_date.strftime('%B %d, %Y'),
                'prompt_amount': str(meter_obj.prompt_amount),
                'success': 'true',
            }
        else:
            data = {
                'success':'no bill',
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

        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.POST.get('consumer_no'),
                                                   city=request.POST.get('city_id'))
        if consumer_obj:
            ret = u''
            ret = ''.join(random.choice('0123456789ABCDEF') for i in range(6))
            OTP = ret
            consumer_registration_sms(consumer_obj, OTP)

            consumer_obj.consumer_otp = OTP
            consumer_obj.save()
            data = {'success': 'true', 'message': 'SMS Sent Successfully', 'contact_no': consumer_obj.contact_no}
        else:
            data = {'success': 'false', 'message': 'Invalid Username'}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|verify_new_consumer', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
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


@csrf_exempt
def verify_OTP(request):
    """to verify_OTP"""
    try:
        print 'selfserviceapp|views.py|verify_OTP'
        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.POST.get('consumer_no'))
        print '---------consumer obj---------',consumer_obj
        if consumer_obj.consumer_otp == request.POST.get('otp_no'):
            consumer_data = {
                'name': consumer_obj.name,
                'consumer_no': consumer_obj.consumer_no,
                'meter_category': consumer_obj.meter_category,
                'bill_cycle':consumer_obj.bill_cycle.bill_cycle_name,
                'address': consumer_obj.address_line_1 +' '+consumer_obj.address_line_2,
                'address_line_1': consumer_obj.address_line_1 ,
                'address_line_2': consumer_obj.address_line_2,
                'city': consumer_obj.city.city,
                'pin_code': consumer_obj.pin_code.pincode,
                'contact_no': consumer_obj.contact_no,
                'email_id': consumer_obj.email_id,
            }
            data = {'success': 'true', 'consumer_data': consumer_data}
        else:
            data = {'success': 'false'}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|verify_OTP', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    print '------data--------',data
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_consumer(request):
    try:
        print 'selfserviceapp|views.py|save_consumer'

        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.POST.get('consumer_no'))
        new_consumer_obj = WebUserProfile(
            consumer_id=ConsumerDetails.objects.get(
                consumer_no=request.POST.get('consumer_no')) if request.POST.get('consumer_no') else None,
            username=request.POST.get('consumer_no'),
            status='Active',
            created_on=datetime.now(),
        );
        new_consumer_obj.save();
        new_consumer_obj.set_password(request.POST.get('password'))
        new_consumer_obj.save();

        data = {
            'success': 'true',
            'message': 'Consumer created successfully.'
        }
    except Exception, e:
        print 'Exception|selfserviceapp|views.py|save_consumer', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_vigilance_complaint(request):
    try:
        print 'selfserviceapp|views.py|save_vigilance_complaint'
        chars = string.digits
        pwdSize = 5
        password = ''.join(random.choice(chars) for _ in range(pwdSize))

        new_vigilance_obj = VigilanceDetail(
            case_id= "CASE" + str(password),
            consumer_id=ConsumerDetails.objects.get(
                id=request.session['consumer_id']) if request.session['consumer_id'] else None,            
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
            created_on=datetime.now(),
            created_by=request.session['login_user'],
        );
        new_vigilance_obj.save();

        attachment_list = request.POST.get('attachments')
        save_attachments(attachment_list, new_vigilance_obj)

        data = {
            'success': 'true',
            'message': 'Consumer created successfully.'
        }
    except Exception, e:
        print 'Exception|selfserviceapp|views.py|save_vigilance_complaint', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def upload_vigilance_image(request):
    try:
        print 'selfserviceapp|views.py|upload_vigilance_image'
        if request.method == 'POST':
            attachment_file = ConsumerVigilanceImage()
            attachment_file.save()

            request.FILES['file[]'].name = 'consumerDocsID_' + str(attachment_file.id) + '_' + request.FILES[
                'file[]'].name
            attachment_file.document_files = request.FILES['file[]']
            attachment_file.save()
            data = {'success': 'true', 'attachid': attachment_file.id}
        else:
            data = {'success': 'false'}
    except MySQLdb.OperationalError, e:
        print 'Exception|selfserviceapp|views.py|upload_vigilance_image', e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def save_attachments(attachment_list, vigilance_id):
    try:
        print 'selfserviceapp|views.py|save_attachments'
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        for attached_id in attachment_list:
            attachment_obj = ConsumerVigilanceImage.objects.get(id=attached_id)
            attachment_obj.vigilance_id = vigilance_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception|selfserviceapp|views.py|save_attachments', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def view_bill(request):
    """To view FAQS page"""
    try:
        print 'selfserviceapp|views.py|view_bill'
        last_receipt_date = '--'
        last_receipt_amount = '0.00'
        month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

        if request.GET.get('meter_reading_id'):
            meter_obj = MeterReadingDetail.objects.get(id=request.GET.get('meter_reading_id'))
            consumer_obj = ConsumerDetails.objects.get(consumer_no=meter_obj.consumer_id.consumer_no)
        else:
            if request.GET.get('consumer_no'):
                consumer_no = request.GET.get('consumer_no')
            else:
                consumer_no = request.session['consumer_no']
            consumer_obj = ConsumerDetails.objects.get(consumer_no=consumer_no)

            meter_obj = MeterReadingDetail.objects.filter(consumer_id=consumer_obj).last()

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
            'con_bill_month': month_list[int(meter_obj.bill_month)-1] + ' ' + str(meter_obj.bill_months_year),
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
            'rounded_bill_amount': str(round(net_bill_amount,0))+'0',
            'bill_status': meter_obj.bill_status,
            'last_receipt_date': last_receipt_date,
            'last_receipt_amount': last_receipt_amount,
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|view_bill', exe
        data = {}
    return render(request, 'self_service/view_bill.html', data)

@csrf_exempt
def verify_consumer(request):
    """to get verify_new_consumer"""
    try:
        print 'selfserviceapp|views.py|verify_consumer'
        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.GET.get('consumer_no'),
                                                   bill_cycle=request.GET.get('bill_cycle'))
        if consumer_obj:
            ret = u''
            ret = ''.join(random.choice('0123456789ABCDEF') for i in range(6))
            OTP = ret
            print '--------OTP---------',OTP
            consumer_obj.consumer_otp = OTP
            consumer_obj.save()
            contact_no = consumer_obj.contact_no
            contact_no = contact_no[0:2]+8*'x'

            data = {'success': 'true', 'message': 'SMS Sent Successfully', 'contact_no': contact_no}
        else:
            data = {'success': 'false', 'message': 'Invalid Username'}

    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|verify_consumer', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def add_new_user(request):
    try:
        print 'selfserviceapp|views.py|add_new_user'
        new_user_obj = UserAccount(
            consumer_no = request.GET.get('consumer_no'),
            parent_consumer_no = WebUserProfile.objects.get(username=request.session['consumer_no']),
            consumer_id = ConsumerDetails.objects.get(consumer_no=request.GET.get('consumer_no')),
            created_on = datetime.now(),
            created_by = request.session['login_user'],
        );
        new_user_obj.save();

        data = {
            'success': 'true',
            'message': 'Account added successfully.'
        }
    except Exception, e:
        print 'Exception|selfserviceapp|views.py|add_new_user', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

