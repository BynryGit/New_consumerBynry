import csv
import traceback
# from bson import json_uti
import json
import sys

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
from serviceapp.models import *
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Zone
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
import datetime
from django.views.decorators.csrf import csrf_exempt

from dateutil.relativedelta import relativedelta

import time

import pdb

# Create your views here.

# @login_required(login_url='/')
def service_request(request):
    try:
        total = ServiceRequest.objects.filter(is_deleted=False).count()
        open = ServiceRequest.objects.filter(status='Open', is_deleted=False).count()
        closed = ServiceRequest.objects.filter(status='Closed', is_deleted=False).count()
        serviceType = ServiceRequest.objects.filter(is_deleted=False)
        zone = Zone.objects.filter(is_deleted=False)
        billCycle = BillCycle.objects.filter(is_deleted=False)
        routes = RouteDetail.objects.filter(is_deleted=False)
        data = {
            'total': total,
            'open': open,
            'closed': closed,
            'ServiceType': serviceType,
            'zones': zone,
            'billCycle': billCycle,
            'routes': routes,
        }
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|service', e
        print e

    return render(request, 'services.html', data)


def get_service_data(request):
    try:
        service_list = []
        service_obj = ServiceRequest.objects.all()
        if request.GET.get('service_type'):
            if request.GET.get('service_type') == 'all':
                serviceType = ServiceRequest.objects.filter(is_deleted=False)
            else:
                serviceType = ServiceRequest.objects.filter(is_deleted=False, id=request.GET.get('service_type'))
            service_obj = serviceType.filter(service_type__id=serviceType)
        if request.GET.get('service_status') and request.GET.get('service_status') != "all":
            service_obj = service_obj.filter(status=request.GET.get('service_status'))
        if request.GET.get('service_source') and request.GET.get('service_source') != "all":
            service_obj = service_obj.filter(source=request.GET.get('service_source'))
        if request.GET.get('zone') and request.GET.get('zone') != "all":
            consumer = ConsumerDetails.objects.filter(zone=request.GET.get('zone'))
            service_obj = service_obj.filter(consumer_id__in=consumer)
        if request.GET.get('bill_cycle') and request.GET.get('bill_cycle') != "all":
            consumer = ConsumerDetails.objects.filter(bill_cycle=request.GET.get('bill_cycle'))
            service_obj = service_obj.filter(consumer_id__in=consumer)
        if request.GET.get('route') and request.GET.get('route') != "all":
            consumer = ConsumerDetails.objects.filter(route=request.GET.get('route'))
            service_obj = service_obj.filter(consumer_id__in=consumer)
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y') + datetime.timedelta(days=1)
            service_obj = service_obj.filter(request_date__range=[start_date, end_date])
        for service in service_obj:
            service_data = {
                'service_no': '<a onclick="service_details(' + str(
                    service.id) + ')">' + service.service_no + '</a>',
                'service_type': service.service_type.request_type,
                'raised_date': service.request_date.strftime('%d/%m/%Y'),
                'consumer_no': '<a onclick="consumer_details(' + str(
                    service.consumer_id.id) + ')">' + service.consumer_id.consumer_no + '</a>',
                'consumer_name': service.consumer_id.name,
                'service_source': service.source,
                'service_status': service.status,
            }
            service_list.append(service_data)
        data = {'data': service_list}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_service_datatable', e
        data = {'msg': 'error'}
        print e
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

@csrf_exempt
def get_service_details(request):
    try:
        service = ServiceRequest.objects.get(id=request.POST.get('service_id'))
        serviceIdDetail = {
            'serviceID': service.service_no,
            'serviceType': service.service_type.request_type,
            'serviceConsumerName': service.consumer_id.name,
            'serviceConsumerNo': service.consumer_id.consumer_no,
            'serviceRequest': service.consumer_remark,
        }

        data = {'success': 'true', 'serviceDetail': serviceIdDetail}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_service_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_consumer_details(request):
    try:
        consumerDetails = ConsumerDetails.objects.get(id=request.POST.get('consumer_id'))
        consumer_address = consumerDetails.address_line_1
        if consumerDetails.address_line_2:
            consumer_address = consumer_address + ', ' + consumerDetails.address_line_2
        if consumerDetails.pin_code:
            consumer_address = consumer_address + ' - ' + consumerDetails.pin_code.pincode + '.'
        getConsumer = {
            'billCycle': consumerDetails.bill_cycle.bill_cycle_code,
            'consumerCity': consumerDetails.city.city,
            'consumerRoute': consumerDetails.route.route_code,
            'consumerZone': consumerDetails.bill_cycle.zone.zone_name,
            'consumerNo': consumerDetails.consumer_no,
            'consumerName': consumerDetails.name,
            'consumerAddress': consumer_address
        }
        data = {'success': 'true', 'consumerDetail': getConsumer}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_consumer_modal', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_service_count(request):
    try:
        print "\n====================================================== In get_service_count ========================================================"
        totals = ServiceRequest.objects.filter(is_deleted=False,
                                                consumer_id__city__city=request.user.userprofile.city.city).count()
        print "\n====================================================== total count ===================================================================", totals
        total = {
            'total': totals,
        }
        data = {'success': 'true', 'total': total}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print "Exception | serviceapp | get_service_count = ", e


def get_bill_cycle(request):
    try:
        bill_cycle_list = []
        if request.GET.get('zone') != 'all':
            bill_cycle_obj = BillCycle.objects.filter(is_deleted=False, zone=request.GET.get('zone'))
        else:
            bill_cycle_obj = BillCycle.objects.filter(is_deleted=False)
        for bill_cycle in bill_cycle_obj:
            bill_cycle_data = {
                'bill_cycle_id': bill_cycle.id,
                'bill_cycle': bill_cycle.bill_cycle_code
            }
            bill_cycle_list.append(bill_cycle_data)
        data = {'success': 'true', 'bill_cycle': bill_cycle_list}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print "Exception | serviceapp | get_bill_cycle = ", e


def get_route(request):
    try:
        route_list = []
        if request.GET.get('bill_cycle') != 'all':
            route_obj = RouteDetail.objects.filter(is_deleted=False, billcycle=request.GET.get('bill_cycle'))
        else:
            route_obj = RouteDetail.objects.filter(is_deleted=False)
        for route in route_obj:
            route_data = {
                'route_id': route.id,
                'route': route.route_code
            }
            route_list.append(route_data)
        data = {'success': 'true', 'route_list': route_list}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print "Exception | serviceapp | get_service_count = ", e