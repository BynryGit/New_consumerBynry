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
        data = {
            'total': NewConsumerRequest.objects.all().count(),
            'open': NewConsumerRequest.objects.filter(status='Open').count(),
            'closed': NewConsumerRequest.objects.filter(status='Closed').count(),
        }
        print 'nscapp|views.py|new_connection'
    except Exception, e:
        data = {}
        print 'Exception|nscapp|views.py|new_connection', e
    return render(request, 'nsc_template/new_connection_list.html',data)


def add_new_consumer(request):
    try:
        print 'nscapp|views.py|add_new_consumer'
        data = {

            'city_list': get_city(request),
            'pincode_list': get_pincode(request)
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|add_new_consumer', e
    return render(request, 'nsc_template/add_new_consumer.html',data)


def get_nsc_data(request):
    try:
        nsc_list = []
        nsc_obj = NewConsumerRequest.objects.all()

        # filter complaint data by nsc category
        if request.GET.get('consumer_category') and request.GET.get('consumer_category') != "All":
            nsc_obj = nsc_obj.filter(consumer_category=request.GET.get('consumer_category'))

        # filter complaint data by nsc sub category
        if request.GET.get('consumer_sub_category') and request.GET.get('consumer_sub_category') != "All":
            nsc_obj = nsc_obj.filter(consumer_subcategory=request.GET.get('consumer_sub_category'))

        # filter complaint data by nsc supply type
        if request.GET.get('supply_type') and request.GET.get('supply_type') != "All":
            nsc_obj = nsc_obj.filter(supply_type=request.GET.get('supply_type'))

        # filter complaint data by nsc status
        if request.GET.get('nsc_status') and request.GET.get('nsc_status') != "All":
            nsc_obj = nsc_obj.filter(status=request.GET.get('nsc_status'))

        # filter complaint data by nsc registration date
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59,
                                                                                                   second=59)
            nsc_obj = nsc_obj.filter(date_of_registration__range=[start_date, end_date])

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
        nsc_id = request.GET.get('nsc_id')
        nsc_obj = NewConsumerRequest.objects.get(id = nsc_id)
        data = {
            'consumer_category': nsc_obj.consumer_category,
            'service_requested': nsc_obj.service_requested,
            'supply_type': nsc_obj.supply_type,
            'consumer_sub_category': nsc_obj.consumer_subcategory,
            'registration_number': nsc_obj.registration_no,
            'registration_date': nsc_obj.date_of_registration.strftime('%d/%m/%Y'),
            'applicant_name': nsc_obj.applicant_name,
            'aadhar_number': nsc_obj.aadhar_no,
            'occupation': nsc_obj.occupation,
            'other_details': nsc_obj.other_occupation,
            'house_details': nsc_obj.meter_building_name,
            'address_line_1': nsc_obj.meter_address_line_1,
            'address_line_2': nsc_obj.meter_address_line_2,
            'landmark': nsc_obj.meter_landmark,
            'city': nsc_obj.meter_city,
            'pincode': nsc_obj.meter_pin_code,
            'email_id': nsc_obj.meter_email_id,
            'mobile_no': nsc_obj.meter_mobile_no,
            'phone_no': nsc_obj.meter_phone_no,
            'new_exst_cons_no': nsc_obj.meter_nearest_consumer_no,
            'is_same_address': nsc_obj.is_same_address,
            'billing_house_details': nsc_obj.billing_building_name,
            'billing_address_line_1': nsc_obj.billing_address_line_1,
            'billing_address_line_2': nsc_obj.billing_address_line_2,
            'billing_landmark': nsc_obj.billing_landmark,
            'billing_city': nsc_obj.billing_city,
            'billing_pincode': nsc_obj.billing_pin_code,
            'billing_email_id': nsc_obj.billing_email_id,
            'billing_mobile_no': nsc_obj.billing_mobile_no,
            'billing_phone_no': nsc_obj.billing_phone_no,
            'billing_new_exst_cons_no': nsc_obj.billing_nearest_consumer_no,
            'billing_premises': nsc_obj.type_of_premises,
            'billing_other_details': nsc_obj.other_premises,
            'requested_load': nsc_obj.requested_load,
            'requested_load_type': nsc_obj.requested_load_type,
            'contract_demand': nsc_obj.contarct_demand,
            'contract_demand_type': nsc_obj.contarct_demand_type,
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|review_consumer_form', e
        data = {}
    return render(request, 'nsc_template/review_consumer_form.html', data)


@csrf_exempt
def save_new_consumer(request):
    try:
        print 'nscapp|views.py|save_new_consumer'        
        # Address Proof List
        a1 = ''
        if request.POST.get('checkbox1_1') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_1')
        if request.POST.get('checkbox1_2') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_2')
        if request.POST.get('checkbox1_3') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_3')
        if request.POST.get('checkbox1_4') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_4')
        if request.POST.get('checkbox1_5') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_5')
        if request.POST.get('checkbox1_6') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_6')
        if request.POST.get('checkbox1_7') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_7')
        if request.POST.get('checkbox1_9') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_9')
        if request.POST.get('checkbox1_10') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_10')
        if request.POST.get('checkbox1_11') != None:
            a1 = a1 + ',' +request.POST.get('checkbox1_11')
        # Identity Proof List
        a2 = ''
        if request.POST.get('checkbox1_12') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_12')
        if request.POST.get('checkbox1_13') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_13')
        if request.POST.get('checkbox1_14') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_14')
        if request.POST.get('checkbox1_15') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_15')
        if request.POST.get('checkbox1_16') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_16')
        if request.POST.get('checkbox1_17') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_17')
        if request.POST.get('checkbox1_18') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_18') 
        if request.POST.get('checkbox1_19') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_19')
        if request.POST.get('checkbox1_20') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_20')
        if request.POST.get('checkbox1_21') != None:
            a2 = a2 + ',' +request.POST.get('checkbox1_21')                                                                                                                  

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
            address_proof_list=a1,
            identity_proof_list=a2,
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
    return HttpResponse(json.dumps(data), content_type='application/json')


