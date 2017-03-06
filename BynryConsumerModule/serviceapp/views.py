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
def service_request(request):
    try:
        # total = ComplaintDetail.objects.filter(is_deleted=False,consumer_id__city__city=request.user.userprofile.city.city).count()
        # open = ComplaintDetail.objects.filter(complaint_status = 'Open', is_deleted=False).count()
        # closed = ComplaintDetail.objects.filter(complaint_status = 'Closed', is_deleted=False).count()
        # WIP = ComplaintDetail.objects.filter(complaint_status = 'WIP', is_deleted=False).count()
        # complaintType = ComplaintType.objects.filter(is_deleted=False)
        # data = {'total':total,'open':open,'closed':closed,'WIP':WIP,'complaintType':complaintType}
        data = {}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|service', e
        print e

    return render(request, 'complaints.html', data)
