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
        #,consumer_id__city__city=request.user.userprofile.city.city
        open = ComplaintDetail.objects.filter(complaint_status = 'Open', is_deleted=False).count()
        closed = ComplaintDetail.objects.filter(complaint_status = 'Closed', is_deleted=False).count()
        complaintType = ComplaintType.objects.filter(is_deleted=False)
        zone = Zone.objects.filter(is_deleted=False)
        billCycle = BillCycle.objects.filter(is_deleted=False)
        routes = RouteDetail.objects.filter(is_deleted=False)
        data = {
            'total': total,
            'open': open,
            'closed': closed,
            'complaintType': complaintType,
            'zones':zone,
            'billCycle':billCycle,
            'routes':routes,
        }
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|complaint', e
        print e

    return render(request, 'complaints.html', data)


# def complaints(request):
#     return render(request, 'complaints.html')

# @login_required(login_url='/')
def get_complaint_data(request):
    try:
        complaint_list = []
        complaint_obj = ComplaintDetail.objects.all()
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
        getConsumer = {
            'billCycle': consumerDetails.bill_cycle.bill_cycle_code,
            'consumerCity': consumerDetails.city.city,
            'consumerRoute': consumerDetails.bill_cycle.bill_cycle_code,
            'consumerZone': consumerDetails.bill_cycle.zone.zone_name,
            'consumerNo': consumerDetails.consumer_no,
            'consumerName': consumerDetails.name,
            'consumerAddress': consumerDetails.address_line_1 + '  ' + consumerDetails.address_line_2 + '  ' + consumerDetails.address_line_3,
        }
        data = {'success': 'true', 'consumerDetail': getConsumer}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_consumer_modal', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/')
def complaint_reading_export(request):
    try:

        selectedStatus = request.GET.get('summaryValue')
        # print "\n Sumaaaaarrryyyyyy VAaaaaaaalllllue ", selectedStatus

        Status = ComplaintDetail.objects.filter()
        # print "\n Status Hereeeeeeeeeeeeeeee ", Status

        selectedComplaintValue = request.GET.get('selectedComplaintType')
        # print "\n Selecetd Complaint Value ", selectedComplaintValue
        # print "+++++++++++++++++++++++++++++++++++"
        selectedFromDate = request.GET.get('selectedFromDate')
        # print selectedFromDate
        selectedToDate = request.GET.get('selectedToDate')
        # print selectedToDate
        complaintDetail = ''
        # total_record = ''

        # Complaint_Type = All and No Dates

        try:

            if selectedComplaintValue == 'All':
                print "here yeah Export"
                try:
                    if (selectedFromDate == "None" and selectedToDate == "None") or (
                                    selectedFromDate == '' and selectedToDate == ''):
                        # if selectedFromDate == '' and selectedToDate == '' :
                        print "\nNo Dates Total All Export"
                        # print selectedFromDate
                        # print selectedToDate
                        complaintDetail = ComplaintDetail.objects.filter(is_deleted=False,
                                                                         consumer_id__city__city=request.user.userprofile.city.city, )

                    else:
                        if selectedFromDate and (
                                            selectedToDate == "None" or selectedToDate == '' or selectedToDate == None):
                            selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate),
                                                                               '%d/%m/%Y').date()
                            print "\nselectedFromDateValue Total All Export = ", selectedFromDateValue
                            # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                            # print "\nselectedToDateValue = ", selectedToDateValue

                            print "\nhereeeeeee from date only Total All Export"

                            complaintDetail = ComplaintDetail.objects.filter(complaint_date__gte=selectedFromDateValue,
                                                                             consumer_id__city__city=request.user.userprofile.city.city,
                                                                             # complaint_date__lte=selectedToDateValue,
                                                                             is_deleted=False)


                        elif selectedToDate and (
                                            selectedFromDate == "None" or selectedFromDate == '' or selectedFromDate == None):
                            # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                            # print "\nselectedFromDateValue = ", selectedFromDateValue
                            selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                            selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                            print "\nselectedToDateValue Total All Export = ", selectedToDateValue

                            print "\nhereeeeeee  To Date Only Total All Export"

                            complaintDetail = ComplaintDetail.objects.filter(
                                # complaint_date__gte=selectedFromDateValue,
                                complaint_date__lte=selectedToDateValue,
                                consumer_id__city__city=request.user.userprofile.city.city,
                                is_deleted=False)
                        elif selectedFromDate and selectedToDate:
                            selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate),
                                                                               '%d/%m/%Y').date()
                            print "\nselectedFromDateValue Total All Export= ", selectedFromDateValue
                            selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                            selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                            print "\nselectedToDateValue Total All Export = ", selectedToDateValue

                            print "\nhereeeeeee Both the dates Total All Export"

                            complaintDetail = ComplaintDetail.objects.filter(complaint_date__gte=selectedFromDateValue,
                                                                             complaint_date__lte=selectedToDateValue,
                                                                             consumer_id__city__city=request.user.userprofile.city.city,
                                                                             is_deleted=False)

                except Exception, e:
                    print e

            else:
                if selectedFromDate == '' and selectedToDate == '':
                    # if  selectedFromDate == '' and selectedToDate == '':
                    print "\nNo Dates Total ComplaintType Export"

                    complaintDetail = ComplaintDetail.objects.filter(complaint_type_id=selectedComplaintValue,
                                                                     consumer_id__city__city=request.user.userprofile.city.city,
                                                                     is_deleted=False)
                else:
                    if selectedFromDate and (
                                        selectedToDate == "None" or selectedToDate == '' or selectedToDate == None):
                        selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                        print "\nselectedFromDateValue Total ComplaintType Export= ", selectedFromDateValue
                        # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                        # print "\nselectedToDateValue = ", selectedToDateValue

                        print "\nhereeeeeee from date only Total ComplaintType Export"

                        complaintDetail = ComplaintDetail.objects.filter(complaint_type_id=selectedComplaintValue,
                                                                         complaint_date__gte=selectedFromDateValue,
                                                                         consumer_id__city__city=request.user.userprofile.city.city,
                                                                         # complaint_date__lte=selectedToDateValue,
                                                                         is_deleted=False)

                    elif selectedToDate and (
                                        selectedFromDate == "None" or selectedFromDate == '' or selectedFromDate == None):
                        # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                        # print "\nselectedFromDateValue = ", selectedFromDateValue
                        selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                        selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                        print "\nselectedToDateValue Total ComplaintType Export= ", selectedToDateValue

                        print "\nhereeeeeee To date only Total ComplaintType Export"

                        complaintDetail = ComplaintDetail.objects.filter(  # complaint_date__gte=selectedFromDateValue,
                            complaint_type_id=selectedComplaintValue,
                            complaint_date__lte=selectedToDateValue,
                            consumer_id__city__city=request.user.userprofile.city.city,
                            is_deleted=False)
                    elif selectedFromDate and selectedToDate:
                        selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                        print "\nselectedFromDateValue Total ComplaintType Export= ", selectedFromDateValue
                        selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                        selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                        print "\nselectedToDateValue Total ComplaintType Export= ", selectedToDateValue

                        print "\nhereeeeeee Both dates Total ComplaintType Export"

                        complaintDetail = ComplaintDetail.objects.filter(complaint_type_id=selectedComplaintValue,
                                                                         complaint_date__gte=selectedFromDateValue,
                                                                         complaint_date__lte=selectedToDateValue,
                                                                         consumer_id__city__city=request.user.userprofile.city.city,
                                                                         is_deleted=False)


        except Exception, e:
            print e

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Complaint_List.csv';
        writer = csv.writer(response)

        writer.writerow(
            ['Complaint ID', 'Complaint Type', 'Raised On', 'Consumer Name', 'Consumer Number', 'Remark'])

        for complaint in complaintDetail:
            tempList = []

            if complaint.complaint_date:
                complaint_date = complaint.complaint_date.strftime('%b %d,%Y %I:%M %p')
            else:
                complaint_date = ('------')

            tempList.append(complaint.complaint_no)
            tempList.append(complaint.complaint_type_id.complaint_type)
            tempList.append(complaint_date)
            tempList.append(complaint.consumer_id.name)
            tempList.append(complaint.consumer_id.consumer_no)
            tempList.append(complaint.remark)
            writer.writerow(tempList)
        return response
    except Exception, e:
        print 'Exception|views.py|complaint_reading_export', e
        data = {'success': 'false'}
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
