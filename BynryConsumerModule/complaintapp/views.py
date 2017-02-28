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
from .models import ComplaintType,ComplaintDetail
from adminapp.models import City, BillCycle, RouteDetail
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
import datetime

from dateutil.relativedelta import relativedelta

import time

import pdb


# Create your views here.

@login_required(login_url='/')
def complaint(request):
    try:
        total = ComplaintDetail.objects.filter(is_deleted=False,consumer_id__city__city=request.user.userprofile.city.city).count()
        open = ComplaintDetail.objects.filter(complaint_status = 'Open', is_deleted=False).count()
        closed = ComplaintDetail.objects.filter(complaint_status = 'Closed', is_deleted=False).count()
        WIP = ComplaintDetail.objects.filter(complaint_status = 'WIP', is_deleted=False).count()
        complaintType = ComplaintType.objects.filter(is_deleted=False)
        data = {'total':total,'open':open,'closed':closed,'WIP':WIP,'complaintType':complaintType}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|complaint', e
        print e

    return render(request, 'complaint/complaint.html',data)

@login_required(login_url='/')
def get_complaint_datatable(request):
    # pdb.set_trace()

    try:
        print "hereeeeeeeeeeeeeeeeeeeeeeeeee"
        data = {}
        userComplaintList = []
        column = request.GET.get('order[0][column]')  # for ordering
        print "\n column value = Success", column
        searchTxt = request.GET.get('search[value]')
        # complaintTypeFilter = request.GET.get('complaintTypeValue')
        # print "======================================= complaintTypeValue",complaintTypeFilter
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"

        list = ['complaint_no']  # order using this field
        column_name = order + list[int(column)]
        start = request.GET.get('start')  # pagination lenth say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))


        selectedStatus = request.GET.get('summaryValue')
        print "\n Sumaaaaarrryyyyyy VAaaaaaaalllllue ",selectedStatus

        # Status = ComplaintDetail.objects.all()
        # print "\n Status Hereeeeeeeeeeeeeeee ",Status

        selectedComplaintValue = request.GET.get('selectedComplaintType')
        print "\n Selecetd Complaint Value ",selectedComplaintValue
        print "+++++++++++++++++++++++++++++++++++"
        selectedFromDate = request.GET.get('selectedFromDate')
        print selectedFromDate
        selectedToDate = request.GET.get('selectedToDate')
        print selectedToDate
        complaintDetail=''
        total_record=''

#Complaint_Type = All and No Dates

        try :
            if selectedComplaintValue =='All':
                print "here yeah"
                try:
                   if (selectedFromDate == "None" and selectedToDate == "None") or (selectedFromDate == '' and selectedToDate == ''):
                           # if selectedFromDate == '' and selectedToDate == '' :
                               print "\nNo Dates and all"
                               # print selectedFromDate
                               # print selectedToDate
                               total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                             Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                             consumer_id__city__city=request.user.userprofile.city.city,is_deleted=False).count()

                               complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                                Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                                consumer_id__city__city=request.user.userprofile.city.city,is_deleted=False).order_by(column_name)[start:length]



                   else:
                           if selectedFromDate and (selectedToDate == "None" or selectedToDate == '' or selectedToDate == None):
                                selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                                print "\nselectedFromDateValue = ",selectedFromDateValue
                                # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                                # print "\nselectedToDateValue = ", selectedToDateValue

                                print "\nhereeeeeee from date only "


                                total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                              Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                                complaint_date__gte=selectedFromDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                                # complaint_date__lte=selectedToDateValue,
                                                                                is_deleted=False).count()


                                complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                                 Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                                   complaint_date__gte=selectedFromDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                                   # complaint_date__lte=selectedToDateValue,
                                                                                   is_deleted=False).order_by(column_name)[start:length]

                           elif selectedToDate and (selectedFromDate == "None" or selectedFromDate == '' or selectedFromDate == None):
                               # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                               # print "\nselectedFromDateValue = ", selectedFromDateValue
                               # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                               selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                               selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                               print "\nselectedToDateValue = ", selectedToDateValue

                               print "\nhereeeeeee  To Date Only"

                               total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                             Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                               # complaint_date__gte=selectedFromDateValue,
                                                                               complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                               is_deleted=False).count()

                               complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                                Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                                  #   complaint_date__gte=selectedFromDateValue,
                                                                                  complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                                  is_deleted=False).order_by(column_name)[start:length]
                           elif selectedFromDate and selectedToDate:
                               selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                               print "\nselectedFromDateValue = ", selectedFromDateValue
                               selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                               selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                               print "\nselectedToDateValue = ", selectedToDateValue

                               print "\nhereeeeeee Both the dates "

                               total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                             Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                               complaint_date__gte=selectedFromDateValue,
                                                                               complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                               is_deleted=False).count()

                               complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                                Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                                  complaint_date__gte=selectedFromDateValue,
                                                                                  complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                                  is_deleted=False).order_by(column_name)[start:length]



                except Exception, e:
                    print e

            else:
                if selectedFromDate == '' and selectedToDate == '' :
                    # if  selectedFromDate == '' and selectedToDate == '':
                        print "\nNo Dates"

                        total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                      Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                        complaint_type_id=selectedComplaintValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                        is_deleted=False).count()

                        complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                         Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                           complaint_type_id=selectedComplaintValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                           is_deleted=False).order_by(column_name)[start:length]


                else:
                    if selectedFromDate and (selectedToDate == "None" or selectedToDate == '' or selectedToDate == None):
                        selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                        print "\nselectedFromDateValue = ", selectedFromDateValue
                        # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                        # print "\nselectedToDateValue = ", selectedToDateValue

                        print "\nhereeeeeee from date only "

                        total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                      Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                        complaint_type_id=selectedComplaintValue,
                                                                        complaint_date__gte=selectedFromDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                        # complaint_date__lte=selectedToDateValue,
                                                                        is_deleted=False).count()

                        complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                         Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                           complaint_type_id=selectedComplaintValue,
                                                                           complaint_date__gte=selectedFromDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                           # complaint_date__lte=selectedToDateValue,
                                                                           is_deleted=False).order_by(column_name)[start:length]

                    elif selectedToDate and (selectedFromDate == "None" or selectedFromDate == '' or selectedFromDate == None):
                        # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                        # print "\nselectedFromDateValue = ", selectedFromDateValue
                        selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                        selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                        print "\nselectedToDateValue = ", selectedToDateValue

                        print "\nhereeeeeee To date only "

                        total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                      Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                      # complaint_date__gte=selectedFromDateValue,
                                                                        complaint_type_id=selectedComplaintValue,
                                                                        complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                        is_deleted=False).count()

                        complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                         Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                         # complaint_date__gte=selectedFromDateValue,
                                                                           complaint_type_id=selectedComplaintValue,
                                                                           complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                           is_deleted=False).order_by(column_name)[start:length]
                    elif selectedFromDate and selectedToDate:
                        selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                        print "\nselectedFromDateValue = ", selectedFromDateValue
                        selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                        selectedToDateValue = selectedToDateValue + relativedelta(days=1)
                        print "\nselectedToDateValue = ", selectedToDateValue

                        print "\nhereeeeeee Both dates "

                        total_record = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                      Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                        complaint_type_id=selectedComplaintValue,
                                                                        complaint_date__gte=selectedFromDateValue,
                                                                        complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                        is_deleted=False).count()

                        complaintDetail = ComplaintDetail.objects.filter(Q(consumer_id__name__icontains=searchTxt) |
                                                                         Q(consumer_id__consumer_no__icontains=searchTxt),
                                                                           complaint_type_id=selectedComplaintValue,
                                                                           complaint_date__gte=selectedFromDateValue,
                                                                           complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                           is_deleted=False).order_by(column_name)[start:length]

        except Exception, e:
            print e

        # print "\nhereeeeee nowwwww complaintDetail",complaintDetail

        for complaint in complaintDetail:
            tempList = []
            if complaint.consumer_id:
                cname = complaint.consumer_id.name
            else:
                cname = '-----'

            id = complaint.complaint_no
            # cname = complaint.consumer_id.name
            # print "\n hereeeeeeeeeeeeeeeeeee cname",cname
            consumerid = complaint.consumer_id.consumer_no


            id1 = '<a title="complaintIdModal" onclick="complaintIdModal(' + str(
                    complaint.id) + ')">' + str(id) + '</a>'
                # print "\nOpen id1 = ", id1

            consumerName = '<a title="consumer_modal" onclick="consumer_modal(' + str(
                complaint.consumer_id.id) + ')" >' + str(
                cname) + '</a>'
            # print "name============", consumerName

            if complaint.complaint_date:
                complaint_date = complaint.complaint_date.strftime('%b %d, %Y %I:%M %p')
            else:
                complaint_date = ('------')
            if len(complaint.remark) > 25:
                remark = '<span>' + complaint.remark[:25] + ' ...</span>'
            else:
                remark = complaint.remark
            # remark = '<span>' + complaint.remark[:50] + '</span>'
            tempList.append(id1)
            tempList.append(complaint.complaint_type_id.complaint_type)
            tempList.append(complaint_date)
            tempList.append(consumerName)
            tempList.append(complaint.consumer_id.consumer_no)
            # tempList.append(complaint.complaint_status)
            tempList.append(remark)
            userComplaintList.append(tempList)
            # print "********************************************", userComplaintList

        total = ComplaintDetail.objects.filter(is_deleted=False,consumer_id__city__city=request.user.userprofile.city.city).count()
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userComplaintList,'total':total}
        # hi=request.session['userComplaintList'] = [i.id for i in userComplaintList]
        # print "HHHHHHHHHIIIIIIIII hereeeee",hi
        # count = userComplaintList.count()
        print "\nUserComplaintList = ",len(userComplaintList)

        if data:
            print "Get data = Success"

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_complaint_datatable', e
        data = {'msg': 'error'}
        print e
    return HttpResponse(json.dumps(data,cls=DjangoJSONEncoder), content_type='application/json')


@login_required(login_url='/')
def get_complaint_id_modal(request):
    print 'Complaint ID Column Detail---', request.GET
    try:
        complaintDetail = ComplaintDetail.objects.filter(id=request.GET.get('id'),consumer_id__city__city=request.user.userprofile.city.city,)
        print "ComplaintDetail================>>>>", complaintDetail
        for complaint in complaintDetail:
            image_address = "http://" + get_current_site(request).domain + "/sitemedia/" + str(complaint.complaint_img)
            complaintIdDetail = {
                'complaintID': complaint.complaint_no,
                'complaintType': complaint.complaint_type_id.complaint_type,
                'complaintConsumerName': complaint.consumer_id.name,
                'complaintConsumerNo': complaint.consumer_id.consumer_no,
                'complaintStatus': complaint.complaint_status,
                'consumerRemark': complaint.remark,
                'closureRemark': complaint.closure_remark,
                'complaint_img':image_address ,
            }

        print "\n\nComplaint Image Address = ",image_address
        data = {'success': 'true', 'complaintIdDetail': complaintIdDetail,}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_complaint_id_modal', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url='/')
def get_consumer_modal(request):
    print 'Complaint ID Column Detail---', request.GET
    try:
        consumerDetails = ConsumerDetails.objects.filter(id=request.GET.get('id'),city__city=request.user.userprofile.city.city,)
        print "ConsumerDetail================>>>>", consumerDetails
        for consumer in consumerDetails:
            if request.user.userprofile.city.city == "Muzaffarpur":
                getConsumer = {
                    'billCycle': consumer.bill_cycle.bill_cycle_code,
                    'consumerNo': consumer.consumer_no,
                    'consumerName': consumer.name,

                    'consumerAddress': consumer.address_line_1 +'  '+consumer.address_line_2+ '  ' +consumer.address_line_3,

                }
            else :
                getConsumer = {
                    'billingUnit': consumer.B_U,
                    'processingCycle': consumer.P_C,
                    'consumerNo': consumer.consumer_no,
                    'consumerName': consumer.name,
                    # 'routeCode': consumer.route.route_code,
                    'consumerAddress': consumer.address_line_1 + '  ' + consumer.address_line_2 + '  ' + consumer.address_line_3,
                }
        data = {'success': 'true', 'getConsumer': getConsumer}
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
                            complaintDetail = ComplaintDetail.objects.filter(is_deleted=False,consumer_id__city__city=request.user.userprofile.city.city,)

                        else:
                            if selectedFromDate and (
                                        selectedToDate == "None" or selectedToDate == '' or selectedToDate == None):
                                selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate),
                                                                                   '%d/%m/%Y').date()
                                print "\nselectedFromDateValue Total All Export = ", selectedFromDateValue
                                # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                                # print "\nselectedToDateValue = ", selectedToDateValue

                                print "\nhereeeeeee from date only Total All Export"

                                complaintDetail = ComplaintDetail.objects.filter(complaint_date__gte=selectedFromDateValue,consumer_id__city__city=request.user.userprofile.city.city,
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

                                complaintDetail = ComplaintDetail.objects.filter(#   complaint_date__gte=selectedFromDateValue,
                                                                                 complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
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
                                                                                 complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
                                                                                 is_deleted=False)

                    except Exception, e:
                        print e

                else:
                    if selectedFromDate == '' and selectedToDate == '':
                        # if  selectedFromDate == '' and selectedToDate == '':
                        print "\nNo Dates Total ComplaintType Export"

                        complaintDetail = ComplaintDetail.objects.filter(complaint_type_id=selectedComplaintValue,consumer_id__city__city=request.user.userprofile.city.city,
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
                                                                             complaint_date__gte=selectedFromDateValue,consumer_id__city__city=request.user.userprofile.city.city,
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

                            complaintDetail = ComplaintDetail.objects.filter(# complaint_date__gte=selectedFromDateValue,
                                                                             complaint_type_id=selectedComplaintValue,
                                                                             complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
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
                                                                             complaint_date__lte=selectedToDateValue,consumer_id__city__city=request.user.userprofile.city.city,
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
        totals = ComplaintDetail.objects.filter(is_deleted = False,consumer_id__city__city=request.user.userprofile.city.city).count()
        print "\n====================================================== total count ===================================================================",totals
        total = {
            'total': totals,
        }
        data = {'success': 'true', 'total': total}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception,e:
        print "Exception | complaintapp | get_complaint_count = ",e