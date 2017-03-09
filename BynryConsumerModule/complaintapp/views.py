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
from .models import ComplaintType, ComplaintDetail
from BynryConsumerModuleapp.models import *
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
import datetime

from dateutil.relativedelta import relativedelta

import time

import pdb


# Create your views here.

# @login_required(login_url='/')
def complaint(request):
    try:
        total = ComplaintDetail.objects.filter(is_deleted=False).count()
        # ,consumer_id__city__city=request.user.userprofile.city.city
        open = ComplaintDetail.objects.filter(complaint_status='Open', is_deleted=False).count()
        closed = ComplaintDetail.objects.filter(complaint_status='Closed', is_deleted=False).count()
        complaintType = ComplaintType.objects.filter(is_deleted=False)
        zone = Zone.objects.filter(is_deleted=False)
        billCycle = BillCycle.objects.filter(is_deleted=False)
        routes = RouteDetail.objects.filter(is_deleted=False)
        data = {
            'total': total,
            'open': open,
            'closed': closed,
            'complaintType': complaintType,
            'zones': zone,
            'billCycle': billCycle,
            'routes': routes,
        }
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|complaint', e
        print e

    return render(request, 'complaints.html', data)


def get_complaint_data(request):
    try:
        complaint_list = []
        complaint_obj = ComplaintDetail.objects.all()
        if request.GET.get('complaint_type'):
            if request.GET.get('complaint_type') == 'all':
                complaintType = ComplaintType.objects.filter(is_deleted=False)
            else:
                complaintType = ComplaintType.objects.filter(is_deleted=False, id=request.GET.get('complaint_type'))
            complaint_obj = complaint_obj.filter(complaint_type_id__in=complaintType)
        if request.GET.get('complaint_status') and request.GET.get('complaint_status') != "all":
            complaint_obj = complaint_obj.filter(complaint_status=request.GET.get('complaint_status'))
        if request.GET.get('complaint_source') and request.GET.get('complaint_source') != "all":
            complaint_obj = complaint_obj.filter(complaint_source=request.GET.get('complaint_source'))
        if request.GET.get('consumer_id'):
            complaint_obj = complaint_obj.filter(consumer_id=request.GET.get('consumer_id'))
        else:
            if request.GET.get('zone') and request.GET.get('zone') != "all":
                consumer = ConsumerDetails.objects.filter(zone=request.GET.get('zone'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
            if request.GET.get('bill_cycle') and request.GET.get('bill_cycle') != "all":
                consumer = ConsumerDetails.objects.filter(bill_cycle=request.GET.get('bill_cycle'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
            if request.GET.get('route') and request.GET.get('route') != "all":
                consumer = ConsumerDetails.objects.filter(route=request.GET.get('route'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y') + datetime.timedelta(days=1)
            complaint_obj = complaint_obj.filter(complaint_date__range=[start_date, end_date])
        for complaint in complaint_obj:
            complaint_data = {
                'complaint_no': '<a onclick="complaint_details(' + str(
                    complaint.id) + ')">' + complaint.complaint_no + '</a>',
                'complaint_type': complaint.complaint_type_id.complaint_type,
                'raised_date': complaint.complaint_date.strftime('%d/%m/%Y'),
                'consumer_no': '<a onclick="consumer_details(' + str(
                    complaint.consumer_id.id) + ')">' + complaint.consumer_id.consumer_no + '</a>',
                'consumer_name': complaint.consumer_id.name,
                'complaint_source': complaint.complaint_source,
                'complaint_status': complaint.complaint_status,
            }
            complaint_list.append(complaint_data)
        data = {'data': complaint_list}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_complaint_datatable', e
        data = {'msg': 'error'}
        print e
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


@login_required(login_url='/')
def get_complaint_details(request):
    try:
        complaint = ComplaintDetail.objects.get(id=request.GET.get('complaint_id'))
        image_address = "http://" + get_current_site(request).domain + "/" + complaint.complaint_img.url

        complaintIdDetail = {
            'complaintID': complaint.complaint_no,
            'complaintType': complaint.complaint_type_id.complaint_type,
            'complaintConsumerName': complaint.consumer_id.name,
            'complaintConsumerNo': complaint.consumer_id.consumer_no,
            'complaintStatus': complaint.complaint_status,
            'consumerRemark': complaint.remark,
            'closureRemark': complaint.closure_remark,
            'complaint_img': image_address,
        }

        data = {'success': 'true', 'complaintDetail': complaintIdDetail}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_complaint_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/')
def get_consumer_details(request):
    print 'Complaint ID Column Detail---', request.GET
    try:
        consumerDetails = ConsumerDetails.objects.get(id=request.GET.get('consumer_id'))
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


def get_complaint_count(request):
    try:
        print "\n====================================================== In get_complaint_count ========================================================"
        totals = ComplaintDetail.objects.filter(is_deleted=False,
                                                consumer_id__city__city=request.user.userprofile.city.city).count()
        print "\n====================================================== total count ===================================================================", totals
        total = {
            'total': totals,
        }
        data = {'success': 'true', 'total': total}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print "Exception | complaintapp | get_complaint_count = ", e


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
        print "Exception | complaintapp | get_bill_cycle = ", e


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
        print "Exception | complaintapp | get_complaint_count = ", e
