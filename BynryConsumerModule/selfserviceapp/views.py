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
from selfserviceapp.models import WebUserProfile
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
        complaint_obj = ComplaintDetail(
            complaint_no=request.GET.get('id'),
            complaint_type_id=complaint_type_obj,
            consumer_id=request.GET.get('consumer_id'),
            remark=request.GET.get('remark'),
            complaint_img=request.GET.get('complaint_img'),
            complaint_source="Web Portal",
            complaint_date=datetime.now()
        )
        complaint_obj.save()

        attachment_list = request.GET.get('attachments')
        save_attachments(attachment_list, complaint_obj)

        data = {'success' : 'true'}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|save_consumer_complaint_details', exe
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
            'complaintID': complaints.complaint_no,
            'complaintType': complaints.complaint_type_id.complaint_type,
            'complaintStatus': complaints.complaint_status,
            'complaintDate': complaints.created_on.strftime('%B %d, %Y %I:%M %p'),
            'closureRemark': complaints.closure_remark,
        }
        data = {'success': 'true', 'complaintDetail': complaint_detail}
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


def save_attachments(attachment_list, complaint_obj):
    print '--------attachment----------',attachment_list
    print '--------complaint_obj----------',complaint_obj
    try:
        print 'selfserviceapp|views.py|save_attachments'
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        for attached_id in attachment_list:
            attachment_obj = ComplaintImages.objects.get(id=attached_id)
            attachment_obj.consumer_id = complaint_obj
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception|selfserviceapp|views.py|save_attachments', e
    return HttpResponse(json.dumps(data), content_type='application/json')




def services(request):
    """To view services page"""
    try:
        print 'selfserviceapp|views.py|services'
        serviceType = ServiceRequestType.objects.filter(is_deleted=False)  # Service Types
        data = {'serviceType': serviceType}
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

        data = {'success': 'true', 'service_no': service_no}
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|service_request', exe
        data = {'success': 'false', 'error': 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def log_in(request):
    print 'selfserviceapp|views.py|login'
    return render(request, 'self_service/login.html')


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
        meter_obj = MeterReadingDetail.objects.filter(consumer_id = consumer_obj).last()
        try:
            meter_payment_obj = PaymentDetail.objects.get(meter_reading_id = meter_obj,bill_status = 'Unpaid')
            data = {
                'con_number': consumer_obj.consumer_no,
                'con_name': consumer_obj.name,
                'con_bill_cycle': consumer_obj.bill_cycle.bill_cycle_code,
                'con_bill_month': meter_obj.bill_month + ' ' + str(meter_obj.bill_months_year),
                'current_amount': str(meter_payment_obj.bill_amount),
                'prev_due': str(meter_payment_obj.due_amount),
                'net_amount': str(meter_payment_obj.net_amount),
                'due_date': meter_payment_obj.due_date.strftime('%B %d, %Y'),
                'prompt_date': meter_payment_obj.prompt_date.strftime('%B %d, %Y'),
                'prompt_amount': str(meter_payment_obj.prompt_amount),
                'success': 'true',
            }
        except:
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
        if consumer_obj.consumer_otp == request.POST.get('otp_no'):
            consumer_data = {
                'name': consumer_obj.name,
                'meter_category': consumer_obj.meter_category,
                'bill_cycle':consumer_obj.bill_cycle.bill_cycle_name,
                'address_line_1': consumer_obj.address_line_1,
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