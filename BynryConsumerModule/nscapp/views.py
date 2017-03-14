from django.shortcuts import render
from consumerapp.views import get_city, get_pincode

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
    return render(request, 'nsc_template/review_consumer_form.html',data)