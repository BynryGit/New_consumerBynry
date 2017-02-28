import traceback
import csv
import pdb
import json
import sys
import StringIO

import pdb
import datetime
from dateutil.relativedelta import relativedelta
import django
from django.http import HttpResponse

import MySQLdb, sys
import dateutil.relativedelta
from django.shortcuts import render, render_to_response, redirect
from django.db.models import Q
from serviceapp.models import  ServiceRequest,ServiceRequestType
from adminapp.models import City, BillCycle, RouteDetail
from consumerapp.models import ConsumerDetails
# Create your views here


# Create your views here.
def service_request(request):
    serviceRequest=ServiceRequest.objects.filter(is_deleted=False,consumer_id__city__city=request.user.userprofile.city.city)
    totalRequest=serviceRequest.filter(is_deleted=False).count()

    # for service request type dropdown
    serviceRequestType=ServiceRequestType.objects.filter(is_deleted=False)
    get_user_service_request_list(request)
    data ={'total':totalRequest, 'serviceRequestType':serviceRequestType}
    print "data",data
    return render(request,'serviceapp/service.html',data)



def get_user_service_request_list(request):

    # pdb.set_trace()

    try:
        print "hereeeeeeeeeeeeeeeeeeeeeeeeee"
        data = {}
        userServiceList = []
        column = request.GET.get('order[0][column]')  # for ordering
        print "\n column value Success = ", column
        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"

        list = ['service_type']  # order using this field
        column_name = order + list[int(column)]
        start = request.GET.get('start')  # pagination lenth say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        selectedStatus = request.GET.get('statusValue')
        print "\n Sumaaaaarrryyyyyy VAaaaaaaalllllue ", selectedStatus

        serviceType = request.GET.get('filterby')
        print "\n Selecetd Service Value =  ", serviceType
        # print "+++++++++++++++++++++++++++++++++++"
        fromDate = request.GET.get('fromdate')
        print fromDate
        toDate = request.GET.get('todate')
        print toDate
        ServiceDetail=''
        total_record=''

        try:
            check = ServiceRequest.objects.filter(service_type = serviceType)
            print "\n CCCCCCCCCCCheckkkkkkkkkkk it ",check

        except Exception, e:
            print e
            print "\n Error in service type"


        try:
            if serviceType == 'All':
                    if (fromDate == "None" and toDate == "None") or (fromDate == '' and toDate == ''):
                        print "\nNo Dates Total All"
                        total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                      Q(consumer_id__name__icontains=searchTxt) |
                                                                      Q(service_type__request_type__icontains=searchTxt),
                                                                        is_deleted=False).count()

                        ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt)|
                                                                 Q(consumer_id__name__icontains=searchTxt)|
                                                                 Q(service_type__request_type__icontains=searchTxt),
                                                                 is_deleted=False).order_by(column_name)[start:length]



                    else:
                        if fromDate and (toDate == "None" or toDate == '' or toDate == None):
                            fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                            print "\nselectedFromDateValue Total All = ", fromDateValue
                            # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                            # print "\nselectedToDateValue = ", selectedToDateValue

                            print "\nhereeeeeee from date only Total All"

                            total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                         Q(consumer_id__name__icontains=searchTxt) |
                                                                         Q(service_type__request_type__icontains=searchTxt),
                                                                         request_date__gte=fromDateValue,
                                                                         is_deleted=False).count()

                            ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt)|
                                                                     Q(consumer_id__name__icontains=searchTxt)|
                                                                     Q(service_type__request_type__icontains=searchTxt),
                                                                     request_date__gte=fromDateValue,
                                                                     is_deleted=False).order_by(column_name)[start:length]


                        elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
                            # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                            # print "\nselectedFromDateValue = ", selectedFromDateValue
                            toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                            toDateValue = toDateValue + relativedelta(days=1)
                            print "\nselectedToDateValue Total All= ", toDateValue

                            print "\nhereeeeeee  To Date Only Total All"

                            total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                         Q(consumer_id__name__icontains=searchTxt) |
                                                                         Q(service_type__request_type__icontains=searchTxt),
                                                                         request_date__lte=toDateValue,
                                                                         is_deleted=False).count()

                            ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                     Q(consumer_id__name__icontains=searchTxt) |
                                                                     Q(service_type__request_type__icontains=searchTxt),
                                                                     request_date__lte=toDateValue,
                                                                     is_deleted=False).order_by(column_name)[start:length]


                        elif fromDate and toDate:
                            fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                            print "\nselectedFromDateValue Total All = ", fromDateValue
                            toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                            toDateValue = toDateValue + relativedelta(days=1)
                            print "\nselectedToDateValue = ", toDateValue

                            print "\nhereeeeeee Both the dates Total All "

                            total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                         Q(consumer_id__name__icontains=searchTxt) |
                                                                         Q(service_type__request_type__icontains=searchTxt),
                                                                         request_date__gte=fromDateValue,
                                                                         request_date__lte=toDateValue,
                                                                         is_deleted=False).count()

                            ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                     Q(consumer_id__name__icontains=searchTxt) |
                                                                     Q(service_type__request_type__icontains=searchTxt),
                                                                     request_date__gte=fromDateValue,
                                                                     request_date__lte=toDateValue,
                                                                     is_deleted=False).order_by(column_name)[start:length]




            else:
                if fromDate == '' and toDate == '':
                    # if  selectedFromDate == '' and selectedToDate == '':
                    print "\nNo Dates Total ServiceType "
                    total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                 Q(consumer_id__name__icontains=searchTxt) |
                                                                 Q(service_type__request_type__icontains=searchTxt),
                                                                 service_type=serviceType,
                                                                 is_deleted=False).count()

                    ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                             Q(consumer_id__name__icontains=searchTxt) |
                                                             Q(service_type__request_type__icontains=searchTxt),
                                                             service_type=serviceType,
                                                             is_deleted=False).order_by(column_name)[start:length]


                else:
                    if fromDate and (toDate == "None" or toDate == '' or toDate == None):
                        fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                        # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                        # print "\nselectedToDateValue = ", selectedToDateValue

                        print "\n From date only Total ServiceType "

                        total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                     Q(consumer_id__name__icontains=searchTxt) |
                                                                     Q(service_type__request_type__icontains=searchTxt),
                                                                     service_type=serviceType,
                                                                     request_date__gte=fromDateValue,
                                                                     is_deleted=False).count()

                        ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                 Q(consumer_id__name__icontains=searchTxt) |
                                                                 Q(service_type__request_type__icontains=searchTxt),
                                                                 service_type=serviceType,
                                                                 request_date__gte=fromDateValue,
                                                                 is_deleted=False).order_by(column_name)[start:length]


                    elif toDate and (fromDate == "None" or fromDate== '' or fromDate == None):
                        # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                        # print "\nselectedFromDateValue = ", selectedFromDateValue
                        toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                        toDateValue = toDateValue + relativedelta(days=1)
                        print "\nselectedToDateValue = Total ServiceType ", toDateValue

                        print "\nhereeeeeee To date only Total ServiceType  "

                        total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                     Q(consumer_id__name__icontains=searchTxt) |
                                                                     Q(service_type__request_type__icontains=searchTxt),
                                                                     service_type=serviceType,
                                                                     request_date__lte=toDateValue,
                                                                     is_deleted=False).count()

                        ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                 Q(consumer_id__name__icontains=searchTxt) |
                                                                 Q(service_type__request_type__icontains=searchTxt),
                                                                 service_type=serviceType,
                                                                 request_date__lte=toDateValue,
                                                                 is_deleted=False).order_by(column_name)[start:length]

                    elif fromDate and toDate:
                        fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                        print "\nselectedFromDateValue  Total ServiceType = ", fromDateValue
                        toDateValue= datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                        toDateValue = toDateValue + relativedelta(days=1)
                        print "\nselectedToDateValue = ", toDateValue

                        print "\nhereeeeeee Both dates Total ServiceType "

                        total_record = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                     Q(consumer_id__name__icontains=searchTxt) |
                                                                     Q(service_type__request_type__icontains=searchTxt),
                                                                     service_type=serviceType,
                                                                     request_date__gte=fromDateValue,
                                                                     request_date__lte=toDateValue,
                                                                     is_deleted=False).count()

                        ServiceDetail = ServiceRequest.objects.filter(Q(consumer_id__consumer_no__icontains=searchTxt) |
                                                                 Q(consumer_id__name__icontains=searchTxt) |
                                                                 Q(service_type__request_type__icontains=searchTxt),
                                                                 service_type=serviceType,
                                                                 request_date__gte=fromDateValue,
                                                                 request_date__lte=toDateValue,
                                                                 is_deleted=False).order_by(column_name)[start:length]


        except Exception, e:
            print e

        # total_record = userRole.filter().count()


        for role in ServiceDetail:
            if role.consumer_id:
                cname = role.consumer_id.name
            else:
                cname = '---'
            tempList = []
            id=role.id
            serviceNo=role.service_no
            id1 = '<a title="viewRequestIdDetail" onclick="viewRequestIdDetail(' + str(
                    role.id) + ')" >' + str(serviceNo) + '</a>'

            consumerName = '<a title="viewConsumerConnectionDetail" onclick="viewConsumerConnectionDetail(' + str(role.consumer_id.id) + ')" >' + str(cname) + '</a>'

            # consumer_remark = '<span>' + role.consumer_remark[:50] + '</span>'
            if role.consumer_remark:
                consumer_remark = len(role.consumer_remark)
                if (consumer_remark > 50):
                    consumer_remark = '<span>' + role.consumer_remark[:50] + ' ......</span>'
                else:
                    consumer_remark = role.consumer_remark
            else:
                consumer_remark="---------"

            if role.service_type:
		retype = role.service_type.request_type
	    else:
		retype = 'NA'
	    tempList.append(id1)
            tempList.append(retype)
            tempList.append(consumerName)
            tempList.append(role.consumer_id.consumer_no )
            # tempList.append(role.status)
            tempList.append(consumer_remark)
            userServiceList.append(tempList)

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userServiceList}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|service.py|get_user_service_request_list', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# def get_user_service_request_list(request):
#     try:
#         userServiceList = []
#
#         column = request.GET.get('order[0][column]')
#         print "column", column
#         searchTxt = request.GET.get('search[value]')
#         serviceType = request.GET.get('filterby')
#         print "serviceType==================>>>>>>>>>>>>>>>>><<<<", serviceType
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['request_id', 'request_id_request_type']
#         column_name = order + list[int(column)]
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))
#         total_record = ServiceRequest.objects.filter(
#             (Q(status__icontains=searchTxt) | Q(request_id__request_type__icontains=serviceType)),
#             is_deleted=False).count()
#         print "total_record==========****************", total_record
#         userRole = ServiceRequest.objects.filter(
#             (Q(status__icontains=searchTxt) | Q(request_id__request_type__icontains=serviceType)),
#             is_deleted=False).order_by(column_name)[start:length]
#         print "userRole############################", userRole
#         for role in userRole:
#
#             tempList = []
#             id = role.id
#             name = role.consumer_id.name
#             cosumerid = role.consumer_id.id
#             # print "name ================>>>>>>>>>>>>>>>>>>",role.consumer_id.id
#             if role.status == 'WIP':
#                 status = '<span style="text-align:center;" class="label label-sm label-success"> WIP </span>'
#                 id1 = '<a title="viewRequestIdDetail" style="color: #32c5d2;" onclick="viewRequestIdDetail(' + str(
#                     role.id) + ')" >' + str(id) + '</a>'
#                 # print "id1*******************",id1
#             elif role.status == 'Closed':
#                 status = '<span style="text-align:center;" class="label label-sm label-danger"> Closed </span>'
#                 id1 = '<a title="viewRequestIdDetail" style="color: #32c5d2;" onclick="viewRequestIdDetail(' + str(
#                     role.id) + ')" >' + str(id) + '</a>'
#
#             else:
#                 status = '<span style="text-align:center;" class="label label-sm label-danger"> Open </span>'
#                 id1 = '<a title="viewRequestIdDetail" style="color: #32c5d2;" onclick="viewRequestIdDetail(' + str(
#                     role.id) + ')" >' + str(id) + '</a>'
#
#             consumerName = '<a title="viewConsumerConnectionDetail" style="color: #32c5d2;" onclick="viewConsumerConnectionDetail(' + str(
#                 role.consumer_id.id) + ')" >' + str(
#                 name) + '</a>'
#             # print "name============", consumerName
#             tempList.append(id1)
#             tempList.append(role.request_id.request_type)
#             tempList.append(consumerName)
#             tempList.append(role.consumer_id.consumer_no)
#             tempList.append(role.consumer_id.connection_status)
#             tempList.append(status)
#             tempList.append(role.remark)
#
#             userServiceList.append(tempList)
#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userServiceList}
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|service.py|get_user_service_request_list', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')

def get_filterBy_service_request(request):
    #pdb.set_trace()
    try:
        # fromDate = datetime.datetime.strptime(request.GET.get('fromdate'), '%d/%m/%Y')
        # print "fromDate############################",fromDate
        # toDate = datetime.datetime.strptime(request.GET.get('todate'), '%d/%m/%Y')
        # print "toDate$$$$$$$$$$$$$$$$$",toDate
        serviceType=request.GET.get('filterby')
        print "22222222222serviceType=========================",serviceType
        data = {'success': 'true', 'serviceType':serviceType}

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|service.py|get-filterBy-service-request', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def request_idDetail(request):
    print 'Request Show History in service request with---',request.GET
    try:
        mail=''
        serviceRequests = ServiceRequest.objects.filter(id=request.GET.get('id'))
        print "serviceRequest================>>>>",serviceRequests
        for serviceRequest in serviceRequests:
            if serviceRequest.consumer_id.email_id:
                mail = serviceRequest.consumer_id.email_id
            else:
                mail = serviceRequest.consumer_id.alternate_email
            consumeraddress1 = serviceRequest.consumer_id.address_line_1
            consumeraddress2 = serviceRequest.consumer_id.address_line_2
            consumeraddress3 = serviceRequest.consumer_id.address_line_3
            if (consumeraddress1 == None or consumeraddress1 == '') and (
                    consumeraddress2 == None or consumeraddress2 == ''):
                if (consumeraddress3 != None):
                    consumeraddressA = serviceRequest.consumer_id.address_line_3
                else:
                    consumeraddressA = serviceRequest.consumer_id.address_line_3
            elif (consumeraddress1 == None or consumeraddress1 == ''):
                if consumeraddress2 != None:
                    if (consumeraddress3 == None or consumeraddress3 == ''):
                        consumeraddressA = serviceRequest.consumer_id.address_line_2
                    else:
                        consumeraddressA = serviceRequest.consumer_id.address_line_2 + ', ' + serviceRequest.consumer_id.address_line_3
                else:
                    consumeraddressA = serviceRequest.consumer_id.address_line_2
            elif (consumeraddress1 == None or consumeraddress1 == '') and (
                    consumeraddress2 == None or consumeraddress2 == '') and (
                    consumeraddress3 == None or consumeraddress3 == ''):
                consumeraddressA = serviceRequest.consumer_id.address_line_1
            elif (consumeraddress1 != None) and (consumeraddress2 != None):
                if (consumeraddress3 == None or consumeraddress3 == ''):
                    consumeraddressA = serviceRequest.consumer_id.address_line_1 + ', ' + serviceRequest.consumer_id.address_line_2
                else:
                    consumeraddressA = serviceRequest.consumer_id.address_line_1 + ', ' + serviceRequest.consumer_id.address_line_2 + ', ' + serviceRequest.consumer_id.address_line_3
            else:
                consumeraddressA = ''

            if request.user.userprofile.city.city == "Muzaffarpur":
                serviceRequestDetail = {
                    'requestId':serviceRequest.service_no,
                    'requestType':serviceRequest.service_type.request_type,
                    'requestStatus':serviceRequest.status,
                    'consumerName':serviceRequest.consumer_id.name,
                    'consumerNumber': serviceRequest.consumer_id.consumer_no,
                    'consumerConnectionType': serviceRequest.consumer_id.connection_status,
                    'consumerEmailID': mail,
                    'consumeraddress': consumeraddressA,
                    'nearConsumerNumber': serviceRequest.consumer_id.nearest_consumer_no,
                    'poleNumber': serviceRequest.consumer_id.pole_no,
                    'consumerRemark': serviceRequest.consumer_remark,
                    'colsureRemark': serviceRequest.closure_remark,
                }
            else:
                serviceRequestDetail = {
                    'requestId': serviceRequest.service_no,
                    'requestType': serviceRequest.service_type.request_type,
                    'requestStatus': serviceRequest.status,
                    'consumerName': serviceRequest.consumer_id.name,
                    'consumerNumber': serviceRequest.consumer_id.consumer_no,
                    'consumerConnectionType': serviceRequest.consumer_id.connection_status,
                    'consumerEmailID': mail,
                    'consumeraddress': consumeraddressA,
                    'nearConsumerNumber': serviceRequest.consumer_id.nearest_consumer_no,
                    'poleNumber': serviceRequest.consumer_id.pole_no,
                    'consumerRemark': serviceRequest.consumer_remark,
                    'colsureRemark': serviceRequest.closure_remark,
                }



        data = {'success': 'true',  'serviceRequestDetail':serviceRequestDetail}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|services.py|request_idDetail', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def consumer_connection_history(request):
    print 'Request Show History in service request with---', request.GET
    try:
        consumerDetails = ConsumerDetails.objects.filter(id=request.GET.get('id'),)
        print "serviceRequest================>>>>",consumerDetails
        for consumerDetail in consumerDetails:
            consumeraddress1 =consumerDetail.address_line_1
            consumeraddress2 = consumerDetail.address_line_2
            consumeraddress3 = consumerDetail.address_line_3
            if (consumeraddress1 == None or consumeraddress1 == '') and (
                            consumeraddress2 == None or consumeraddress2 == ''):
                if (consumeraddress3 != None):
                    consumeraddressA = consumerDetail.address_line_3
                else:
                    consumeraddressA = consumerDetail.address_line_3
            elif (consumeraddress1 == None or consumeraddress1 == ''):
                if consumeraddress2 != None:
                    if (consumeraddress3 == None or consumeraddress3 == ''):
                        consumeraddressA = consumerDetail.address_line_2
                    else:
                        consumeraddressA = consumerDetail.address_line_2 + ', ' + consumerDetail.address_line_3
                else:
                    consumeraddressA = consumerDetail.address_line_2
            elif (consumeraddress1 == None or consumeraddress1 == '') and (
                            consumeraddress2 == None or consumeraddress2 == '') and (
                            consumeraddress3 == None or consumeraddress3 == ''):
                consumeraddressA = consumerDetail.address_line_1
            elif (consumeraddress1 != None) and (consumeraddress2 != None):
                if (consumeraddress3 == None or consumeraddress3 == ''):
                    consumeraddressA = consumerDetail.address_line_1 + ', ' + consumerDetail.address_line_2
                else:
                    consumeraddressA = consumerDetail.address_line_1 + ', ' + consumerDetail.address_line_2 + ', ' + consumerDetail.address_line_3
            else:
                consumeraddressA = ''

            if request.user.userprofile.city.city == "Muzaffarpur":
                consumerrelateDetail = {
                    'billcyclecode':consumerDetail.bill_cycle.bill_cycle_code,
                    #'routeId':consumerDetail.route.route_code,
                    'consumerNumber':consumerDetail.consumer_no,
                    'meterNumber':consumerDetail.meter_no,
                    'consumerName':consumerDetail.name,
                    'consumeraddress': consumeraddressA,
                    'consumerMeterPhase': consumerDetail.meter_phase,
                    'consumerMeterMake': consumerDetail.meter_make,
                    'consumerMeterDigit': consumerDetail.meter_digit,
                    'consumerMeterType': consumerDetail.meter_type,
                }
            else:
                consumerrelateDetail = {
                    'billingUnit': consumerDetail.B_U,
                    'processingCycle': consumerDetail.P_C,
                    # 'routeId':consumerDetail.route.route_code,
                    'consumerNumber': consumerDetail.consumer_no,
                    'meterNumber': consumerDetail.meter_no,
                    'consumerName': consumerDetail.name,
                    'consumeraddress': consumeraddressA,
                    'consumerMeterPhase': consumerDetail.meter_phase,
                    'consumerMeterMake': consumerDetail.meter_make,
                    'consumerMeterDigit': consumerDetail.meter_digit,
                    'consumerMeterType': consumerDetail.meter_type,
                }

        data = {'success': 'true',  'consumerrelateDetail':consumerrelateDetail}
        print 'Request show history out service request with---', data
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|services.py|consumer_connection_history', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')




def servicerequest_reading_export(request):

    try:
            serviceType = request.GET.get('filterby')
            print "serviceType==================>>>>>>>>>>>>>>>>><<<<", serviceType
            selectedStatus = request.GET.get('statusValue')
            fromDate = request.GET.get('fromdate')
            # print " *********fromDate*********",fromDate
            toDate = request.GET.get('todate')
            # print " *********toDate *********", toDate
            userRole = ''


            try:
                if serviceType == 'All':
                    print "here yeah Export"
                    try:
                        if (fromDate == "None" and toDate == "None") or (fromDate == '' and toDate == ''):
                            print "\nNo Dates Total All Export"
                            userRole = ServiceRequest.objects.filter(is_deleted=False)

                        else:
                            if fromDate and (toDate == "None" or toDate == '' or toDate == None):
                                fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                                print "\nTotal All Export selectedFromDateValue = ", fromDateValue
                                # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                                # print "\nselectedToDateValue = ", selectedToDateValue

                                print "\nhereeeeeee from date only Total All Export"

                                userRole = ServiceRequest.objects.filter(request_date__gte=fromDateValue,
                                                                         is_deleted=False)

                            elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
                                # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                                # print "\nselectedFromDateValue = ", selectedFromDateValue
                                # toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                                toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                                toDateValue = toDateValue + relativedelta(days=1)
                                print "\nTotal All Export selectedToDateValue = ", toDateValue

                                print "\nhereeeeeee  To Date Only Total All Export"
                                userRole = ServiceRequest.objects.filter(request_date__lte=toDateValue,
                                                                         is_deleted=False)


                            elif fromDate and toDate:
                                fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                                print "\n Total All Export selectedFromDateValue = ", fromDateValue
                                toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                                toDateValue = toDateValue + relativedelta(days=1)
                                print "\n Total All Export selectedToDateValue = ", toDateValue

                                print "\nhereeeeeee Both the dates Total All Export"

                                userRole = ServiceRequest.objects.filter(request_date__gte=fromDateValue,
                                                                         request_date__lte=toDateValue,
                                                                         is_deleted=False)


                    except Exception, e:
                        print e

                else:
                    if fromDate == '' and toDate == '':
                        # if  selectedFromDate == '' and selectedToDate == '':
                        print "\nNo Dates Total service type Export"

                        userRole = ServiceRequest.objects.filter(service_type=serviceType,
                                                                 is_deleted=False)


                    else:
                        if fromDate and (toDate == "None" or toDate == '' or toDate == None):
                            fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                            print "\nTotal service type Export selectedFromDateValue = ", fromDateValue
                            # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
                            # print "\nselectedToDateValue = ", selectedToDateValue

                            print "\nhereeeeeee from date only Total service type Export"

                            userRole = ServiceRequest.objects.filter(service_type=serviceType,
                                                                     request_date__gte=fromDateValue,
                                                                     is_deleted=False)

                        elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
                            # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
                            # print "\nselectedFromDateValue = ", selectedFromDateValue
                            # toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                            toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                            toDateValue = toDateValue + relativedelta(days=1)
                            print "\nTotal service type Export selectedToDateValue = ", toDateValue

                            print "\nhereeeeeee To date only Total service type Export"

                            userRole = ServiceRequest.objects.filter(service_type=serviceType,
                                                                     request_date__lte=toDateValue,
                                                                     is_deleted=False)

                        elif fromDate and toDate:
                            fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
                            print "\n Total service type Export selectedFromDateValue = ", fromDateValue
                            toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
                            toDateValue = toDateValue + relativedelta(days=1)
                            print "\n Total service type Export selectedToDateValue = ", toDateValue

                            print "\nhereeeeeee Both dates Total service type Export"

                            userRole = ServiceRequest.objects.filter(service_type=serviceType,
                                                                     request_date__gte=fromDateValue,
                                                                     request_date__lte=toDateValue,
                                                                     is_deleted=False)

                            print "\nhereeeeeee Both dates Total service type Export userRole", userRole


            except Exception, e:
                print e

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Service_Request_List.csv"';
            writer = csv.writer(response)
            # writer = csv.writer(response, delimiter=' ', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(['Request ID','Service Request Type','Consumer Name','Consumer Number','Connection Type', 'Remark'])

            for serviceRequest in userRole:
                tempList=[]
                tempList.append(serviceRequest.service_no)
                tempList.append(serviceRequest.service_type.request_type)
                tempList.append(serviceRequest.consumer_id.name)
                tempList.append(serviceRequest.consumer_id.consumer_no)
                tempList.append(serviceRequest.consumer_id.connection_status)
                tempList.append(serviceRequest.consumer_remark)
                writer.writerow(tempList)

            return response
    except Exception, e:
        print e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_service_count(request):
    totals = ServiceRequest.objects.filter(is_deleted = False,consumer_id__city__city=request.user.userprofile.city.city).count()
    print "total count = ",totals
    total = {
        'total': totals,
    }
    data = {'success': 'true', 'total': total}
    return HttpResponse(json.dumps(data), content_type='application/json')




