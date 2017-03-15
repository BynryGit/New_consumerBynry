from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from consumerapp.views import get_city, get_pincode
from nscapp.models import NewConsumerRequest
from BynryConsumerModuleapp.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from consumerapp.models import ConsumerDetails
from nscapp.models import *

# Create your views here.
def new_connection_list(request):
    try:
        print 'nscapp|views.py|new_connection'
    except Exception, e:
        print 'Exception|nscapp|views.py|new_connection', e
    return render(request, 'nsc_template/new_connection_list.html')


def add_new_consumer(request):
    try:
        print 'nscapp|views.py|add_new_consumer'
        data = {'city_list': get_city(request),
                'pincode_list': get_pincode(request)
            }
    except Exception, e:
        print 'Exception|nscapp|views.py|add_new_consumer', e
    return render(request, 'nsc_template/add_new_consumer.html',data)


def get_nsc_data(request):
    try:
        nsc_list = []
        nsc_obj = NewConsumerRequest.objects.all()
        for nsc in nsc_obj:
            if nsc.closed_date:
                closed_date = nsc.closed_date.strftime('%d/%m/%Y')
            else:
                closed_date = ''
            nsc_data = {
                'registration_id': nsc.registration_no,
                'applicant_name': nsc.applicant_name,
                'aadhar_no': nsc.aadhar_no,
                'contact_no': nsc.meter_mobile_no,
                'category': nsc.consumer_category,
                'sub_category': nsc.consumer_subcategory,
                'supply_type': nsc.supply_type,
                'registration_date': nsc.date_of_registration.strftime('%d/%m/%Y'),
                'status': nsc.status,
                'closed_date': closed_date,
                'actions': '<a class="icon-note" title="Review" href="/nscapp/review-consumer-form/?nsc_id='+str(nsc.id)+'"></a>&nbsp;' + '&nbsp;<a class="fa fa-print" title="Print"></a>'
            }
            nsc_list.append(nsc_data)
        print 'nscapp|views.py|get_nsc_data'
        data = {'data': nsc_list}
    except Exception, e:
        print 'Exception|nscapp|views.py|get_nsc_data', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


def review_consumer_form(request):
    try:
        print 'nscapp|views.py|review_consumer_form'
        data = {
            'consumer_category': 'LT-Supply',
            'service_requested': '001-New Connection',
            'supply_type': 'Sigle Phase',
            'consumer_sub_category': 'Residential',
            'registration_number': 'NSC1025',
            'registration_date': '12/03/2017',
            'applicant_name': 'Steve Smith',
            'aadhar_number': '4567820124',
            'occupation': 'Self Employed',
            'other_details': '',
            'house_details': 'Flat 201, Primrose',
            'address_line_1': 'Right Bhusari Colony',
            'address_line_2': 'Kothrud',
            'landmark': 'Oppo. Borse Hospital',
            'city': 'Pune',
            'pincode': '411038',
            'email_id': 'steve.smith@gamil.com',
            'mobile_no': '9567820124',
            'phone_no': '',
            'new_exst_cons_no': '',
            'billing_house_details': 'Flat 201, Primrose',
            'billing_address_line_1': 'Right Bhusari Colony',
            'billing_address_line_2': 'Kothrud',
            'billing_landmark': 'Oppo. Borse Hospital',
            'billing_city': 'Pune',
            'billing_pincode': '411038',
            'billing_email_id': 'steve.smith@gamil.com',
            'billing_mobile_no': '9567820124',
            'billing_phone_no': '',
            'billing_new_exst_cons_no': '',
            'billing_premises': 'Supply',
            'billing_other_details': '',
            'requested_load': '440',
            'requested_load_type': 'KW',
            'contract_demand': '',
            'contract_demand_type': '',
            'pan_card': 'CTIPK0124K',
            'aadhar_card': '4567820124',
            'passport': ''
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|review_consumer_form', e
        data = {}
    return render(request, 'nsc_template/review_consumer_form.html', data)


#@csrf_exempt
def save_new_consumer(request):
    try:
        print 'nscapp|views.py|save_new_consumer'
        new_consumer_obj = NewConsumerRequest(
            applicant_name=request.POST.get('applicant_name'),
            aadhar_no=request.POST.get('applicant_aadhar_no'),
            occupation=request.POST.get('applicant_occupation'),
            other_occupation=request.POST.get('applicant_other_details'),
            consumer_category=request.POST.get('consumer_category'),
            service_requested=request.POST.get('consumer_service'),
            supply_type=request.POST.get('consumer_supply_type'),
            consumer_subcategory=request.POST.get('consumer_subcategory'),
            registration_no='111',  # Need to change logic
            date_of_registration=datetime.now(),
            meter_building_name=request.POST.get('flat_no'),
            meter_address_line_1=request.POST.get('address_line1'),
            meter_address_line_2=request.POST.get('address_line2'),
            meter_landmark=request.POST.get('landmark'),

            meter_city = City.objects.get(
                id=request.POST.get('city')) if request.POST.get(
                'city') else None ,
            meter_pin_code = Pincode.objects.get(
                id=request.POST.get('pincode')) if request.POST.get(
                'pincode') else None ,                


            meter_email_id=request.POST.get('email'),
            meter_mobile_no=request.POST.get('mobile'),
            meter_phone_no=request.POST.get('phone_no'),
            meter_nearest_consumer_no=request.POST.get('existing_consumer_no'),
            #is_same_address=request.POST.get('user_role'),
            billing_building_name=request.POST.get('bill_flat_no'),
            billing_address_line_1=request.POST.get('bill_address_line1'),
            billing_address_line_2=request.POST.get('bill_address_line2'),
            billing_landmark=request.POST.get('bill_landmark'),

            billing_city = City.objects.get(
                id=request.POST.get('bill_city')) if request.POST.get(
                'bill_city') else None ,
            billing_pin_code = Pincode.objects.get(
                id=request.POST.get('bill_pincode')) if request.POST.get(
                'bill_pincode') else None , 

            billing_email_id=request.POST.get('bill_email'),
            billing_mobile_no=request.POST.get('bill_mobile'),
            billing_phone_no=request.POST.get('bill_phone_no'),
            billing_nearest_consumer_no=request.POST.get('bill_existing_consumer_no'),
            type_of_premises=request.POST.get('premises_type'),
            other_premises=request.POST.get('bill_other_data'),
            requested_load=request.POST.get('requested_load'),
            requested_load_type=request.POST.get('load_type'),
            contarct_demand=request.POST.get('contract_demand'),
            contarct_demand_type=request.POST.get('contract_demand_type'),
            created_on=datetime.now(),
            #created_by=request.session['login_user'],
        );
        new_consumer_obj.save();
        data = {
            'success': 'true',
            'message': 'Consumer created successfully.'
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|save_new_consumer', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    print '..aadarta',data
    return HttpResponse(json.dumps(data), content_type='application/json')


