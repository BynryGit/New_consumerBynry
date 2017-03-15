from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
from BynryConsumerModuleapp.models import *
from consumerapp.models import ConsumerDetails
from nscapp.models import *
import datetime


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
    except Exception, e:
        print 'Exception|nscapp|views.py|add_new_consumer', e
    return render(request, 'nsc_template/add_new_consumer.html')


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
