from django.shortcuts import render
import traceback
import csv
import pdb
import json
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import sys
from django.http import HttpResponse
from consumerapp.models import ConsumerDetails
from serviceapp.models import ServiceRequest, ServiceRequestType
from complaintapp.models import ComplaintDetail, ComplaintType
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from decorator import role_required
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.sites.shortcuts import get_current_site

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from collections import OrderedDict
from django.contrib.sites.shortcuts import get_current_site

# SHUBHAM
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Pincode, Zone, Utility
from datetime import datetime

Months = {
    1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR',
    5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG',
    9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DEC'}


def consumer_list(request):
    try:
        data = {'city_list': get_city(request),
                'zone_list': get_zone(request),
                'billcycle_list': get_billcycle(request),
                'route_list': get_RouteDetail(request),
                'pincode_list': get_pincode(request)}
    except Exception, e:
        print 'Exception|views.py|consumerapp', e
    return render(request, 'consumer_list.html', data)


def get_city(request):
    city_list = []
    try:
        city_objs = City.objects.filter(is_deleted=False)
        for city in city_objs:
            city_list.append({'city_id': city.id, 'city': city.city})
            data = city_list
            return data
    except Exception, ke:
        print ke
        data = {'city_list': 'none', 'message': 'No city available'}
        return data


def get_zone(request):
    zone_list = []
    try:
        zone_objs = Zone.objects.filter(is_deleted=False)
        for zone in zone_objs:
            zone_list.append({'zone_id': zone.id, 'zone_name': zone.zone_name})
        data = zone_list
        return data
    except Exception, ke:
        print ke
        data = {'zone_list': 'none', 'message': 'No zone available'}
        return data


def get_billcycle(request):
    billcycle_list = []
    try:
        bill_objs = BillCycle.objects.filter(is_deleted=False)
        for bill in bill_objs:
            billcycle_list.append({'bill_cycle_id': bill.id, 'bill_cycle_code': bill.bill_cycle_code})
        data = billcycle_list
        return data
    except Exception, ke:
        print ke
        data = {'billcycle_list': 'none', 'message': 'No billcycle available'}
        return data


def get_RouteDetail(request):
    route_list = []
    try:
        route_objs = RouteDetail.objects.filter(is_deleted=False)
        for route in route_objs:
            route_list.append({'route_id': route.id, 'route_code': route.route_code})
        data = route_list
        return data
    except Exception, ke:
        print ke
        data = {'route_list': 'none', 'message': 'No route available'}
        return data


def get_pincode(request):
    pincode_list = []
    try:
        pincode_objs = Pincode.objects.filter(is_deleted=False)
        for pincode in pincode_objs:
            pincode_list.append({'pincode_id': pincode.id, 'pincode': pincode.pincode})
        data = pincode_list
        return data
    except Exception, ke:
        print ke
        data = {'pincode_list': 'none', 'message': 'No pincode available'}
        return data


def get_consumer_list(request):
    try:
        filter_zone = request.GET.get('filter_zone')
        filter_bill = request.GET.get('filter_bill')
        filter_route = request.GET.get('filter_route')
        filter_category = request.GET.get('filter_category')
        filter_service = request.GET.get('filter_service')
        filter_from = request.GET.get('filter_from')
        filter_to = request.GET.get('filter_to')

        data = {}
        final_list = []
        try:
            consumer_obj_list = ConsumerDetails.objects.all()
            if filter_zone != 'all':
                consumer_obj_list = consumer_obj_list.filter(zone=filter_zone)
            if filter_bill != 'all':
                consumer_obj_list = consumer_obj_list.filter(bill_cycle=filter_bill)
            if filter_route != 'all':
                consumer_obj_list = consumer_obj_list.filter(route=filter_route)
            if filter_category:
                consumer_obj_list = consumer_obj_list.filter(meter_category=filter_category)
            if filter_service:
                consumer_obj_list = consumer_obj_list.filter(connection_status=filter_service)
            if filter_from != '' and filter_to != '':
                filter_from = datetime.strptime(filter_from, "%d/%m/%Y")
                filter_from = filter_from.strftime("%Y-%m-%d")
                filter_to = datetime.strptime(filter_to, "%d/%m/%Y")
                filter_to = filter_to.strftime("%Y-%m-%d")
                consumer_obj_list = consumer_obj_list.filter(register_date__range=[filter_from, filter_to])

            for consumer_obj in consumer_obj_list:
                consumer_no = consumer_obj.consumer_no
                consumer_no1 = '<a href="/consumerapp/consumer-details/?consumer_no=' + consumer_no + '">' + consumer_no + '</a>'
                consumer_name = consumer_obj.name
                contact_no = consumer_obj.contact_no
                email_id = consumer_obj.email_id
                servicerequest = ServiceRequest.objects.filter(consumer_id=consumer_obj.id).count()
                complaintrequest = ComplaintDetail.objects.filter(consumer_id=consumer_obj.id).count()
                connection_status = consumer_obj.connection_status
                action = '<a> <i class="fa fa-pencil" aria-hidden="true" onclick="edit_consumer(' + consumer_no + ')"></i> </a>'

                consumer_data = {
                    'consumer_no': consumer_no1,
                    'consumer_name': consumer_name,
                    'contact_no': contact_no,
                    'email_id': email_id,
                    'servicerequest': servicerequest,
                    'complaintrequest': complaintrequest,
                    'connection_status': connection_status,
                    'action': action
                }
                final_list.append(consumer_data)
            data = {'success': 'true', 'data': final_list}
        except Exception as e:
            print "==============Exception===============================", e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_consumer(request):
    try:
        data = {}
        final_list = []
        try:
            consumer_obj = ConsumerDetails.objects.get(consumer_no=request.GET.get('consumer_no'))
            consumer_no = consumer_obj.consumer_no
            name = consumer_obj.name
            name = name + ' (' + consumer_no + ') '
            utility = consumer_obj.Utility.utility
            contact_no = consumer_obj.contact_no
            email_id = consumer_obj.email_id
            aadhar_no = consumer_obj.aadhar_no
            address_line_1 = consumer_obj.address_line_1
            address_line_2 = consumer_obj.address_line_2
            city_id = str(consumer_obj.city.id)
            pincode_id = str(consumer_obj.pin_code.id)
            zone_id = str(consumer_obj.zone.id)
            meter_no = consumer_obj.meter_no
            meter_category = consumer_obj.meter_category
            sanction_load = consumer_obj.sanction_load

            consumer_data = {
                'name': name,
                'consumer_no': consumer_no,
                'utility': utility,
                'contact_no': contact_no,
                'aadhar_no': aadhar_no,
                'email_id': email_id,
                'address_line_1': address_line_1,
                'address_line_2': address_line_2,
                'city_id': city_id,
                'pincode_id': pincode_id,
                'zone_id': zone_id,
                'meter_no': meter_no,
                'meter_category': meter_category,
                'sanction_load': sanction_load
            }
            data = {'success': 'true', 'data': consumer_data}
        except Exception as e:
            print "==============Exception===============================", e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_consumer_profile(request):
    try:
        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.POST.get('consumer_no'))
        print '............SSS.........', request.POST.get('edit_contact')
        consumer_obj.contact_no = request.POST.get('edit_contact')
        consumer_obj.email_id = request.POST.get('edit_email')
        consumer_obj.aadhar_no = request.POST.get('edit_aadhar')
        consumer_obj.address_line_1 = request.POST.get('edit_address1')
        consumer_obj.address_line_2 = request.POST.get('edit_address2')
        consumer_obj.meter_no = request.POST.get('edit_meter_no')
        consumer_obj.sanction_load = request.POST.get('edit_sanction_load')
        consumer_obj.pin_code = Pincode.objects.get(
            id=request.POST.get('edit_pincode')) if request.POST.get(
            'edit_pincode') else None
        consumer_obj.zone = Zone.objects.get(
            id=request.POST.get('edit_zone')) if request.POST.get(
            'edit_zone') else None
        consumer_obj.updated_on = datetime.now()
        consumer_obj.save();

        data = {
            'success': 'true',
            'message': 'User Updated Successfully.'
        }
    except Exception, e:
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


def consumer_details(request):
    try:
        data = {}
        final_list = []
        try:
            consumer_obj = ConsumerDetails.objects.get(consumer_no=request.GET.get('consumer_no'))
            consumer_no = consumer_obj.consumer_no
            name = consumer_obj.name
            utility = consumer_obj.Utility.utility
            contact_no = consumer_obj.contact_no
            email_id = consumer_obj.email_id
            aadhar_no = consumer_obj.aadhar_no
            address_line_1 = consumer_obj.address_line_1
            address_line_2 = consumer_obj.address_line_2
            address = address_line_1 + ', ' + address_line_2
            zone_name = str(consumer_obj.zone.zone_name)
            meter_no = consumer_obj.meter_no
            meter_category = consumer_obj.meter_category
            sanction_load = consumer_obj.sanction_load

            consumer_data = {
                'name': name,
                'consumer_no': consumer_no,
                'utility': utility,
                'contact_no': contact_no,
                'aadhar_no': aadhar_no,
                'email_id': email_id,
                'address': address,
                'zone_name': zone_name,
                'meter_no': meter_no,
                'meter_category': meter_category,
                'sanction_load': sanction_load
            }
            data = {'success': 'true', 'data': consumer_data}
        except Exception as e:
            print "==============Exception===============================", e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return render(request, 'consumer_details.html')
