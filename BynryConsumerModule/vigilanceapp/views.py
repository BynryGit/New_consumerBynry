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

def vigilance(request):
    try:
        total = VigilanceDetail.objects.filter(is_deleted=False).count()
        open = VigilanceDetail.objects.filter(vigilance_status='Open', is_deleted=False).count()
        closed = VigilanceDetail.objects.filter(vigilance_status='Closed', is_deleted=False).count()
        vigilanceType = VigilanceType.objects.filter(is_deleted=False)
        zone = Zone.objects.filter(is_deleted=False)
        billCycle = BillCycle.objects.filter(is_deleted=False)
        routes = RouteDetail.objects.filter(is_deleted=False)
        data = {
            'total': total,
            'open': open,
            'closed': closed,
            'vigilanceType': vigilanceType,
            'zones': zone,
            'billCycle': billCycle,
            'routes': routes,
        }
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|complaint', e
        print e

    return render(request, 'vigilance_cases.html', data)

def get_vigilance_data(request):
    try:
        vigilance_list = []
        vigilance_obj = VigilanceDetail.objects.all()
        if request.GET.get('vigilance_type'):
            if request.GET.get('vigilance_type') == 'all':
                vigilanceType = VigilanceType.objects.filter(is_deleted=False)
            else:
                vigilanceType = VigilanceType.objects.filter(is_deleted=False, id=request.GET.get('vigilance_type'))
            vigilance_obj = vigilance_obj.filter(vigilance_type_id__in=vigilanceType)

        if request.GET.get('vigilance_status') and request.GET.get('vigilance_status') != "all":
            vigilance_obj = vigilance_obj.filter(vigilance_status=request.GET.get('vigilance_status'))
        if request.GET.get('vigilance_source') and request.GET.get('vigilance_source') != "all":
            vigilance_obj = vigilance_obj.filter(vigilance_source=request.GET.get('vigilance_source'))
        if request.GET.get('zone') and request.GET.get('zone') != "all":
            consumer = ConsumerDetails.objects.filter(zone=request.GET.get('zone'))
            vigilance_obj = vigilance_obj.filter(consumer_id__in=consumer)
        if request.GET.get('bill_cycle') and request.GET.get('bill_cycle') != "all":
            consumer = ConsumerDetails.objects.filter(bill_cycle=request.GET.get('bill_cycle'))
            vigilance_obj = vigilance_obj.filter(consumer_id__in=consumer)
        if request.GET.get('route') and request.GET.get('route') != "all":
            consumer = ConsumerDetails.objects.filter(route=request.GET.get('route'))
            vigilance_obj = vigilance_obj.filter(consumer_id__in=consumer)
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y') + datetime.timedelta(days=1)
            vigilance_obj = vigilance_obj.filter(registered_date__range=[start_date, end_date])

        for vigilance in vigilance_obj:
            vigilance_data = {
                'case_id': '<a onclick="vigilance_details(' + str(
                    vigilance.id) + ')">' + vigilance.case_id + '</a>',
                'vigilance_type': vigilance.vigilance_type_id.vigilance_type,
                'registered_date': vigilance.registered_date.strftime('%d/%m/%Y'),
                'consumer_no': '<a onclick="consumer_details(' + str(
                    vigilance.consumer_id.id) + ')">' + vigilance.consumer_id.consumer_no + '</a>',
                'consumer_name': vigilance.consumer_id.name,
                'vigilance_source': vigilance.vigilance_source,
                'vigilance_status': vigilance.vigilance_status,
            }
            vigilance_list.append(vigilance_data)
        data = {'data': vigilance_list}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_complaint_datatable', e
        data = {'msg': 'error'}
        print e
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


@login_required(login_url='/')
def get_vigilance_details(request):
    try:
        vigilance = VigilanceDetail.objects.get(id=request.GET.get('vigilance_id'))
        vigilanceDetail = {
            'caseID': vigilance.case_id,
            'vigilanceType': vigilance.vigilance_type_id.vigilance_type,
            'registeredDate': vigilance.registered_date.strftime('%d/%m/%Y'),
            'registeredSource': vigilance.vigilance_source,
            'caseStatus': vigilance.vigilance_status,
            'theftFound': vigilance.theft_found,
            'vigilanceRemark': vigilance.vigilance_remark,
            'penaltyAmount': '',
            'paymentStatus': '',
            'paymentMethod': '',
            'courtRemark': '',
            'courtCaseStatus': '',
        }
        try:
            vigilancePenalty = VigilancePenalyDetail.objects.get(vigilance_id=request.GET.get('vigilance_id'))
            vigilanceDetail['penaltyAmount'] = vigilancePenalty.payment
            vigilanceDetail['paymentStatus'] = vigilancePenalty.payment_status
            vigilanceDetail['paymentMethod'] = vigilancePenalty.payment_method
        except:
            pass
        try:
            courtCase = CourtCaseDetail.objects.get(vigilance_id=request.GET.get('vigilance_id'))
            vigilanceDetail['courtRemark'] = courtCase.court_remark
            vigilanceDetail['courtCaseStatus'] = courtCase.case_status
        except:
            pass

        data = {'success': 'true', 'vigilanceDetail': vigilanceDetail}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_complaint_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')