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

#SHUBHAM
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Pincode, Zone, Utility
from datetime import datetime

Months = {
    1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR',
    5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG',
    9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DEC'}


# Create your views here.

# # TODO Starting view for consumer card
# @login_required(login_url='/')
# # @role_required(privileges=[ 'Consumers'], login_url='/', raise_exception=True)
# def consumer_jobcard(request):
#     data = {}
#     objlist = {}
#     finallist = []
#     billcycles = []
#     consumerfinal_list = []
#     edit1 = ''
#     consumercardPagination = []
#     consumersCount = ConsumerDetails.objects.filter(parent__isnull=True,
#                                                     city__city=request.user.userprofile.city.city,
#                                                     is_deleted=False, is_new=False).count()
#     billcycled = BillCycle.objects.filter(is_deleted=False)
#     print billcycled

#     billingUnits = BillingUnit.objects.all()
#     # for billingUnit in billingUnits:
#     #     processingCycles = ProcessingCycle.objects.filter(B_U__B_U=billingUnit)

#     city = request.GET.get('city')
#     filterBy_BillingUnit = request.GET.get('filterBy_BillingUnit')
#     filterBy_ProcessingCycle = request.GET.get('filterBy_ProcessingCycle')
#     filterBy_BillCycle = request.GET.get('filterBy_BillCycle')
#     fromDate = request.GET.get('filterfromDate')
#     toDate = request.GET.get('filtertoDate')
#     image_address = ''

#     if filterBy_BillCycle or filterBy_BillingUnit:
#         try:
#             if city == 'Muzaffarpur':
#                 if filterBy_BillCycle == 'All':
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    is_deleted=False, is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    is_deleted=False, is_new=False,
#                                                                    register_date__gte=fromDate1).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    is_deleted=False,
#                                                                    register_date__lte=toDate1, is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    is_deleted=False,
#                                                                    register_date__gte=fromDate1,
#                                                                    register_date__lte=toDate1, is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                 else:
#                     print "\n All billcycle All"
#                     billcycle = BillCycle.objects.get(id=filterBy_BillCycle, is_deleted=False)
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False, register_date__gte=fromDate1,
#                                                                    is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False, register_date__lte=toDate1,
#                                                                    is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    register_date__gte=fromDate1,
#                                                                    is_deleted=False, register_date__lte=toDate1,
#                                                                    is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#             else:
#                 if filterBy_BillingUnit == 'All':
#                     billingUnits = BillingUnit.objects.all()
#                     print "billingUnit*****---------------******", billingUnits
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    is_deleted=False, is_new=False,
#                                                                    register_date__gte=fromDate1,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    is_deleted=False,
#                                                                    register_date__lte=toDate1, is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    is_deleted=False,
#                                                                    register_date__gte=fromDate1,
#                                                                    register_date__lte=toDate1, is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)

#                 else:
#                     print "Billing unit All"
#                     billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                     if filterBy_ProcessingCycle == 'All':
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False, register_date__gte=fromDate1,
#                                                                        is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False, register_date__lte=toDate1,
#                                                                        is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        register_date__gte=fromDate1,
#                                                                        is_deleted=False, register_date__lte=toDate1,
#                                                                        is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         else:
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                     else:
#                         print " Billing Unit and processing cycle"
#                         # billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                         # processingCycle = ProcessingCycle.objects.get(B_U__B_U=billingUnit, P_C=filterBy_ProcessingCycle)



#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False, register_date__gte=fromDate1,
#                                                                        is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False, register_date__lte=toDate1,
#                                                                        is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        register_date__gte=fromDate1,
#                                                                        is_deleted=False, register_date__lte=toDate1,
#                                                                        is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         else:
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)

#             for consumer in consumerfinal_list:
#                 print "consumer----------555555555555---SSSS---", consumer
#                 servicerequest = ServiceRequest.objects.filter(is_deleted=False,
#                                                                consumer_id_id=consumer.id).count()
#                 complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
#                                                                  consumer_id_id=consumer.id).count()
#                 feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id).last()
#                 # print '-----------', feedbackscount
#                 edit1 = ''
#                 if feedbackscount:
#                     if feedbackscount.stars == 'STAR1':
#                         edit1 = 1
#                     elif feedbackscount.stars == 'STAR2':
#                         edit1 = 2
#                     elif feedbackscount.stars == 'STAR3':
#                         edit1 = 3
#                     elif feedbackscount.stars == 'STAR4':
#                         edit1 = 4
#                     elif feedbackscount.stars == 'STAR5':
#                         edit1 = 5
#                     else:
#                         edit1 = ''

#                 if consumer.email_id:
#                     mail = consumer.email_id
#                 else:
#                     mail = consumer.alternate_email

#                 try:
#                     appUser = AppUser.objects.filter(consumer=consumer.id)
#                     image_address = "http://" + get_current_site(request).domain + "/sitemedia/" + str(
#                         appUser.profile_pic)
#                 except Exception, e:
#                     print '================Exception in AppUser = ',e

#                 objlist = {
#                     'profile_pic':image_address,
#                     'id': consumer.id,
#                     'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
#                     'name': consumer.name,
#                     'consumer_no': consumer.consumer_no,
#                     'email_id': mail,
#                     'contact_no': consumer.contact_no,
#                     'servicerequest': servicerequest,
#                     'complaintraised': complaintraised,
#                     'edit1': edit1,
#                 }
#                 finallist.append(objlist)
#             paginator = Paginator(finallist, 4)  # Show 25 contacts per page
#             page = request.GET.get('page')
#             print "#############dddddd..............request.GET.get('page', 1)................dddddddd#####", page
#             page_number=request.GET.get('page_number')
#             try:
#                 consumercardPagination = paginator.page(page_number)
#             except PageNotAnInteger:  # If page is not an integer, deliver first page.
#                 consumercardPagination = paginator.page(1)
#             except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
#                 consumercardPagination = paginator.page(paginator.num_pages)
#             data = {'finallist': consumercardPagination}
#             data = render(request, 'consumer/consumerBody.html', data)
#         except Exception, e:
#             print 'exception ', str(traceback.print_exc())
#             print 'Exception|views.py|consumer_card_filter', e
#             data = {'No consumer found': 'error'}
#         return HttpResponse(data)

#     else:
#         consumersCount = ConsumerDetails.objects.filter(parent__isnull=True,
#                                                         city__city=request.user.userprofile.city.city,
#                                                         is_deleted=False, is_new=False).count()
#         consumers = ConsumerDetails.objects.filter(parent__isnull=True,city__city=request.user.userprofile.city.city, is_deleted=False,is_new=False,is_active=True).order_by('-register_date')




#         consumerfinal_list.extend(consumers)
#         for consumer in consumerfinal_list:
#             try:
#                 appUser = AppUser.objects.get(consumer=consumer.id)
#                 print "===================APPUSER===================== ", appUser
#                 image_address = "http://" + get_current_site(request).domain +"/sitemedia/" +  str(
#                     appUser.profile_pic)
#                # print str(appUser.profile_pic)
#                 print "image_address============",image_address

#             except Exception, e:
#                 print '================Exception in AppUser = ', e

#             servicerequest = ServiceRequest.objects.filter(is_deleted=False,
#                                                            consumer_id_id=consumer.id).count()
#             complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
#                                                              consumer_id_id=consumer.id).count()
#             feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id).last()
#             # print '-----------', feedbackscount
#             edit1 = ''
#             if feedbackscount:
#                 if feedbackscount.stars == 'STAR1':
#                     edit1 = 1
#                 elif feedbackscount.stars == 'STAR2':
#                     edit1 = 2
#                 elif feedbackscount.stars == 'STAR3':
#                     edit1 = 3
#                 elif feedbackscount.stars == 'STAR4':
#                     edit1 = 4
#                 elif feedbackscount.stars == 'STAR5':
#                     edit1 = 5
#                 else:
#                     edit1 = ''
#             if consumer.email_id:
#                 mail = consumer.email_id
#             else:
#                 mail = consumer.alternate_email
#             objlist = {
#                 'profile_pic':image_address,
#                 'id': consumer.id,
#                 'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
#                 'name': consumer.name,
#                 'consumer_no': consumer.consumer_no,
#                 'email_id': mail,
#                 'contact_no': consumer.contact_no,
#                 'servicerequest': servicerequest,
#                 'complaintraised': complaintraised,
#                 'edit1': edit1,
#             }
#             finallist.append(objlist)

#         paginator = Paginator(finallist, 4)  # Show 25 contacts per page
#         page = request.GET.get('page')
#         print "#############dddddd.............here i am............dddddddd#####", page
#         page_number = request.GET.get('page_number')
#         try:
#             consumercardPagination = paginator.page(page_number)
#         except PageNotAnInteger:  # If page is not an integer, deliver first page.
#             consumercardPagination = paginator.page(1)
#         except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
#             consumercardPagination = paginator.page(paginator.num_pages)
#         data = {'finallist': consumercardPagination, 'consumersCount': consumersCount, 'billingUnit': billingUnits,'billcycles':billcycled}

#     return render(request, 'consumer/consumer.html', data)




# # TODO Billing unit mapping for processing cycle
# def get_pc_accordingtoBU(request):
#     data = {}
#     pc_list = []
#     try:
#         billing_unit = request.GET.get('bu')
#         billingUnit = BillingUnit.objects.filter(B_U=billing_unit)
#         processingUnit = ProcessingCycle.objects.filter(B_U__B_U=billing_unit)
#         print "SSSSSSSSSSSS", processingUnit
#         for unit in processingUnit:
#             pc = unit.P_C
#             pc_list.append({'pc': pc})
#         data = {'pc_list': pc_list}
#         print "data------------in------get_pc_accordingtoBU-------", data
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|get_pc_accordingtoBU', e
#         data = {'pc_list': 'none', 'message': 'No pc available'}
#     return HttpResponse(json.dumps(data), content_type='application/json')


# # TODO search for consumer card
# def consumer_card_search_filter(request):
#     objlist={}
#     finallist=[]
#     consumerfinal_list=[]
#     consumercardPagination=[]
#     data={}
#     searchTxt=request.GET.get('searchTxt')
#     print "searchTxt===============",searchTxt
#     image_address = ''
#     city = request.GET.get('city')
#     filterBy_BillingUnit = request.GET.get('filterBy_BillingUnit')
#     filterBy_ProcessingCycle = request.GET.get('filterBy_ProcessingCycle')
#     filterBy_BillCycle = request.GET.get('filterBy_BillCycle')
#     fromDate = request.GET.get('filterfromDate')
#     toDate = request.GET.get('filtertoDate')
#     print "filterBy_BillingUnit===========================",filterBy_BillingUnit
#     try:
#         if filterBy_BillCycle or filterBy_BillingUnit:
#             try:
#                 if city == 'Muzaffarpur':
#                     if filterBy_BillCycle == 'All':
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        is_deleted=False, is_new=False).order_by(
#                                 '-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        is_deleted=False, is_new=False,
#                                                                        register_date__gte=fromDate1).order_by(
#                                 '-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        is_deleted=False,
#                                                                        register_date__lte=toDate1,
#                                                                        is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        is_deleted=False,
#                                                                        register_date__gte=fromDate1,
#                                                                        register_date__lte=toDate1,
#                                                                        is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         else:
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False,
#                                                                        is_new=False, is_active=True).order_by(
#                                 '-register_date')
#                             consumerfinal_list.extend(consumers)
#                     else:
#                         print "\n All billcycle All"
#                         billcycle = BillCycle.objects.get(id=filterBy_BillCycle, is_deleted=False)
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        bill_cycle=billcycle,
#                                                                        is_deleted=False, is_new=False,
#                                                                        is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        bill_cycle=billcycle,
#                                                                        is_deleted=False, register_date__gte=fromDate1,
#                                                                        is_new=False, is_active=True).order_by(
#                                 '-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        bill_cycle=billcycle,
#                                                                        is_deleted=False, register_date__lte=toDate1,
#                                                                        is_new=False, is_active=True).order_by(
#                                 '-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        bill_cycle=billcycle,
#                                                                        register_date__gte=fromDate1,
#                                                                        is_deleted=False, register_date__lte=toDate1,
#                                                                        is_new=False, is_active=True).order_by(
#                                 '-register_date')
#                             consumerfinal_list.extend(consumers)
#                         else:
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),(Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        bill_cycle=billcycle,
#                                                                        is_deleted=False, is_new=False,
#                                                                        is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                 else:
#                     if filterBy_BillingUnit == 'All':
#                         billingUnits = BillingUnit.objects.all()
#                         print "billingUnit*****---------------******", billingUnits
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        B_U__in=[bu.B_U for bu in billingUnits],
#                                                                        is_deleted=False, is_new=False,
#                                                                        is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        B_U__in=[bu.B_U for bu in billingUnits],
#                                                                        is_deleted=False, is_new=False,
#                                                                        register_date__gte=fromDate1,
#                                                                        is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        B_U__in=[bu.B_U for bu in billingUnits],
#                                                                        is_deleted=False,
#                                                                        register_date__lte=toDate1, is_new=False,
#                                                                        is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        B_U__in=[bu.B_U for bu in billingUnits],
#                                                                        is_deleted=False,
#                                                                        register_date__gte=fromDate1,
#                                                                        register_date__lte=toDate1, is_new=False,
#                                                                        is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         else:
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                        B_U__in=[bu.B_U for bu in billingUnits],
#                                                                        is_deleted=False, is_new=False,
#                                                                        is_active=True).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)

#                     else:
#                         print "Billing unit All"
#                         billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                         if filterBy_ProcessingCycle == 'All':
#                             if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                             fromDate == None or toDate == None):
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=billingUnit,
#                                                                            is_deleted=False, is_new=False,
#                                                                            is_active=True).order_by('-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                                 fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                        '%d/%m/%Y').date()
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=billingUnit,
#                                                                            is_deleted=False,
#                                                                            register_date__gte=fromDate1,
#                                                                            is_new=False, is_active=True).order_by(
#                                     '-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                                 toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                      '%d/%m/%Y').date()
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=billingUnit,
#                                                                            is_deleted=False, register_date__lte=toDate1,
#                                                                            is_new=False, is_active=True).order_by(
#                                     '-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             elif fromDate and toDate:
#                                 fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                        '%d/%m/%Y').date()
#                                 toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                      '%d/%m/%Y').date()
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=billingUnit,
#                                                                            register_date__gte=fromDate1,
#                                                                            is_deleted=False, register_date__lte=toDate1,
#                                                                            is_new=False, is_active=True).order_by(
#                                     '-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             else:
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=billingUnit,
#                                                                            is_deleted=False, is_new=False,
#                                                                            is_active=True).order_by('-register_date')
#                                 consumerfinal_list.extend(consumers)
#                         else:
#                             print " Billing Unit and processing cycle"
#                             # billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                             # processingCycle = ProcessingCycle.objects.get(B_U__B_U=billingUnit, P_C=filterBy_ProcessingCycle)



#                             if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                             fromDate == None or toDate == None):
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=filterBy_BillingUnit,
#                                                                            P_C=filterBy_ProcessingCycle,
#                                                                            is_deleted=False, is_new=False,
#                                                                            is_active=True).order_by('-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                                 fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                        '%d/%m/%Y').date()
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=filterBy_BillingUnit,
#                                                                            P_C=filterBy_ProcessingCycle,
#                                                                            is_deleted=False,
#                                                                            register_date__gte=fromDate1,
#                                                                            is_new=False, is_active=True).order_by(
#                                     '-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                                 toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                      '%d/%m/%Y').date()
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=filterBy_BillingUnit,
#                                                                            P_C=filterBy_ProcessingCycle,
#                                                                            is_deleted=False, register_date__lte=toDate1,
#                                                                            is_new=False, is_active=True).order_by(
#                                     '-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             elif fromDate and toDate:
#                                 fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                        '%d/%m/%Y').date()
#                                 toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                      '%d/%m/%Y').date()
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=filterBy_BillingUnit,
#                                                                            P_C=filterBy_ProcessingCycle,
#                                                                            register_date__gte=fromDate1,
#                                                                            is_deleted=False, register_date__lte=toDate1,
#                                                                            is_new=False, is_active=True).order_by(
#                                     '-register_date')
#                                 consumerfinal_list.extend(consumers)
#                             else:
#                                 consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=city,
#                                                                            B_U=filterBy_BillingUnit,
#                                                                            P_C=filterBy_ProcessingCycle,
#                                                                            is_deleted=False, is_new=False,
#                                                                            is_active=True).order_by('-register_date')
#                                 consumerfinal_list.extend(consumers)

#                 for consumer in consumerfinal_list:
#                     servicerequest = ServiceRequest.objects.filter(is_deleted=False,
#                                                                    consumer_id_id=consumer.id).count()
#                     complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
#                                                                      consumer_id_id=consumer.id).count()
#                     feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id).last()
#                     # print '-----------', feedbackscount
#                     edit1 = ''
#                     if feedbackscount:
#                         if feedbackscount.stars == 'STAR1':
#                             edit1 = 1
#                         elif feedbackscount.stars == 'STAR2':
#                             edit1 = 2
#                         elif feedbackscount.stars == 'STAR3':
#                             edit1 = 3
#                         elif feedbackscount.stars == 'STAR4':
#                             edit1 = 4
#                         elif feedbackscount.stars == 'STAR5':
#                             edit1 = 5
#                         else:
#                             edit1 = ''

#                     if consumer.email_id:
#                         mail = consumer.email_id
#                     else:
#                         mail = consumer.alternate_email

#                     try:
#                         appUser = AppUser.objects.filter(consumer=consumer.id)
#                         image_address = "http://" + get_current_site(request).domain + "/sitemedia/" + str(
#                             appUser.profile_pic)
#                     except Exception, e:
#                         print '================Exception in AppUser = ', e

#                     objlist = {
#                         'profile_pic': image_address,
#                         'id': consumer.id,
#                         'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
#                         'name': consumer.name,
#                         'consumer_no': consumer.consumer_no,
#                         'email_id': mail,
#                         'contact_no': consumer.contact_no,
#                         'servicerequest': servicerequest,
#                         'complaintraised': complaintraised,
#                         'edit1': edit1,
#                     }
#                     finallist.append(objlist)
#                 paginator = Paginator(finallist, 4)  # Show 25 contacts per page
#                 page = request.GET.get('page')
#                 print "search.............request.GET.get('page', 1)................dddddddd#####", page
#                 page_number = request.GET.get('page_number')
#                 try:
#                     consumercardPagination = paginator.page(page_number)
#                 except PageNotAnInteger:  # If page is not an integer, deliver first page.
#                     consumercardPagination = paginator.page(1)
#                 except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
#                     consumercardPagination = paginator.page(paginator.num_pages)
#                 data = {'finallist': consumercardPagination}
#                 data = render(request, 'consumer/consumerBody.html', data)
#             except Exception, e:
#                 print 'exception ', str(traceback.print_exc())
#                 print 'Exception|views.py|consumer_card_filter', e
#                 data = {'No consumer found': 'error'}
#             return HttpResponse(data)

#         else:
#             print "==dddd=================APPUSER===================== "
#             consumersCount = ConsumerDetails.objects.filter(parent__isnull=True,
#                                                             city__city=request.user.userprofile.city.city,
#                                                             is_deleted=False, is_new=False).count()
#             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True,
#                                                        city__city=request.user.userprofile.city.city, is_deleted=False,
#                                                        is_new=False, is_active=True).order_by('-register_date')

#             consumerfinal_list.extend(consumers)
#             for consumer in consumerfinal_list:
#                 try:
#                     appUser = AppUser.objects.get(consumer=consumer.id)
#                     image_address = "http://" + get_current_site(request).domain + "/sitemedia/" + str(
#                         appUser.profile_pic)
#                     # print str(appUser.profile_pic)

#                 except Exception, e:
#                     print '================Exception in AppUser = ', e

#                 servicerequest = ServiceRequest.objects.filter(is_deleted=False,
#                                                                consumer_id_id=consumer.id).count()
#                 complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
#                                                                  consumer_id_id=consumer.id).count()
#                 feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id).last()
#                 # print '-----------', feedbackscount
#                 edit1 = ''
#                 if feedbackscount:
#                     if feedbackscount.stars == 'STAR1':
#                         edit1 = 1
#                     elif feedbackscount.stars == 'STAR2':
#                         edit1 = 2
#                     elif feedbackscount.stars == 'STAR3':
#                         edit1 = 3
#                     elif feedbackscount.stars == 'STAR4':
#                         edit1 = 4
#                     elif feedbackscount.stars == 'STAR5':
#                         edit1 = 5
#                     else:
#                         edit1 = ''
#                 if consumer.email_id:
#                     mail = consumer.email_id
#                 else:
#                     mail = consumer.alternate_email
#                 objlist = {
#                     'profile_pic': image_address,
#                     'id': consumer.id,
#                     'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
#                     'name': consumer.name,
#                     'consumer_no': consumer.consumer_no,
#                     'email_id': mail,
#                     'contact_no': consumer.contact_no,
#                     'servicerequest': servicerequest,
#                     'complaintraised': complaintraised,
#                     'edit1': edit1,
#                 }
#                 finallist.append(objlist)

#             paginator = Paginator(finallist, 4)  # Show 25 contacts per page
#             page = request.GET.get('page')
#             print "search............here i am............dddddddd#####", page
#             page_number = request.GET.get('page_number')
#             try:
#                 consumercardPagination = paginator.page(page_number)
#             except PageNotAnInteger:  # If page is not an integer, deliver first page.
#                 consumercardPagination = paginator.page(1)
#             except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
#                 consumercardPagination = paginator.page(paginator.num_pages)
#         data = {'finallist': consumercardPagination}
#         data = render(request, 'consumer/consumerBody.html', data)





#         # consumer =ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#         #                         meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True, city__city=request.user.userprofile.city.city,
#         #                                is_deleted=False, is_new=False,is_active=True).order_by('-register_date')
#         # consumerfinal_list.extend(consumer)
#         # for consumer in consumerfinal_list :
#         #     print "consumer-------------SSSS---", consumer
#         #     servicerequest = ServiceRequest.objects.filter(is_deleted=False,
#         #                                                    consumer_id_id=consumer.id).count()
#         #     complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
#         #                                                      consumer_id_id=consumer.id).count()
#         #     feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id).last()
#         #     print '-----------', feedbackscount
#         #     edit1 = ''
#         #     if feedbackscount:
#         #         if feedbackscount.stars == 'STAR1':
#         #             edit1 = 1
#         #         elif feedbackscount.stars == 'STAR2':
#         #             edit1 = 2
#         #         elif feedbackscount.stars == 'STAR3':
#         #             edit1 = 3
#         #         elif feedbackscount.stars == 'STAR4':
#         #             edit1 = 4
#         #         elif feedbackscount.stars == 'STAR5':
#         #             edit1 = 5
#         #         else:
#         #             edit1 = ''
#         #     if consumer.email_id:
#         #         mail = consumer.email_id
#         #     else:
#         #         mail = consumer.alternate_email
#         #
#         #     try:
#         #         appUser = AppUser.objects.get(consumer=consumer.id)
#         #         print "===================APPUSER===================== ", appUser
#         #         image_address = "http://" + get_current_site(request).domain +"/sitemedia/" +  str(
#         #             appUser.profile_pic)
#         #        # print str(appUser.profile_pic)
#         #         print "image_address============",image_address
#         #
#         #     except Exception, e:
#         #         print '================Exception in AppUser = ', e
#         #
#         #     objlist = {
#         #         'profile_pic': image_address,
#         #         'id': consumer.id,
#         #         'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
#         #         'name': consumer.name,
#         #         'consumer_no': consumer.consumer_no,
#         #         'email_id': mail,
#         #         'contact_no': consumer.contact_no,
#         #         'servicerequest': servicerequest,
#         #         'complaintraised': complaintraised,
#         #         'edit1': edit1,
#         #     }
#         #     finallist.append(objlist)
#         # paginator = Paginator(finallist, 4)  # Show 25 contacts per page
#         # page = request.GET.get('page')
#         # print "#############dddddddddddddd#####", page
#         # page_number = request.GET.get('page_number')
#         # try:
#         #     consumercardPagination = paginator.page(page_number)
#         # except PageNotAnInteger:  # If page is not an integer, deliver first page.
#         #     consumercardPagination = paginator.page(1)
#         # except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
#         #     consumercardPagination = paginator.page(paginator.num_pages)

#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|consumer_card_filter', e
#         data = {'No consumer found': 'error'}
#     return HttpResponse(data)


# # TODO Consumer Card Filter
# def consumer_card_filter(request,filterBy_BillingUnit=None,filterBy_ProcessingCycle=None,filterfromDate=None,filtertoDate=None,city=None):

#     print '=============consumer_card_filter====================>>',request.GET
#     print '===============consumer_card_filter==================>>', request.GET.get('page')
#     # pdb.set_trace()
#     edit1 = ''
#     netamount = ''
#     payment_done = ''
#     finallist=[]
#     consumers = ''
#     paymentMode = ''
#     consumercardPagination = []
#     consumerfinal_list=[]
#     try:
#         data = {}
#         finallist = []
#         city = city
#         filterBy_BillingUnit = filterBy_BillingUnit
#         filterBy_ProcessingCycle = filterBy_ProcessingCycle
#         filterBy_BillCycle = request.GET.get('filterBy_BillCycle')
#         fromDate = filterfromDate
#         toDate = filtertoDate

#         # city = request.GET.get('city')
#         # filterBy_BillingUnit = request.GET.get('filterBy_BillingUnit')
#         # filterBy_ProcessingCycle = request.GET.get('filterBy_ProcessingCycle')
#         # filterBy_BillCycle = request.GET.get('filterBy_BillCycle')
#         # fromDate = request.GET.get('fromDate')
#         # toDate = request.GET.get('toDate')

#         consumersCount = ConsumerDetails.objects.filter(parent__isnull=True,
#                                                         city__city=request.user.userprofile.city.city,
#                                                         is_deleted=False, is_new=False).count()
#         billingUnits = BillingUnit.objects.all()
#         if city == 'Muzaffarpur':
#             if filterBy_BillCycle == 'All':
#                 if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                 fromDate == None or toDate == None):
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                     fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                            '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,is_new=False,
#                                                                register_date__gte=fromDate1)
#                     consumerfinal_list.extend(consumers)
#                 elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                     toDate1 = datetime.datetime.strptime(str(toDate),
#                                                          '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,
#                                                                register_date__lte=toDate1,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 elif fromDate and toDate:
#                     fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                            '%d/%m/%Y').date()
#                     toDate1 = datetime.datetime.strptime(str(toDate),
#                                                          '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,
#                                                                register_date__gte=fromDate1,
#                                                                register_date__lte=toDate1,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 else:
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False,is_new=False)
#                     consumerfinal_list.extend(consumers)
#             else:
#                 print "\n All billcycle All"
#                 billcycle = BillCycle.objects.get(id=filterBy_BillCycle, is_deleted=False)
#                 if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                 fromDate == None or toDate == None):
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                bill_cycle=billcycle,
#                                                                is_deleted=False,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                     fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                            '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                bill_cycle=billcycle,
#                                                                is_deleted=False, register_date__gte=fromDate1,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                     toDate1 = datetime.datetime.strptime(str(toDate),
#                                                          '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                bill_cycle=billcycle,
#                                                                is_deleted=False, register_date__lte=toDate1,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 elif fromDate and toDate:
#                     fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                            '%d/%m/%Y').date()
#                     toDate1 = datetime.datetime.strptime(str(toDate),
#                                                          '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                bill_cycle=billcycle,
#                                                                register_date__gte=fromDate1,
#                                                                is_deleted=False, register_date__lte=toDate1,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 else:
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                bill_cycle=billcycle,
#                                                                is_deleted=False,is_new=False)
#                     consumerfinal_list.extend(consumers)
#         else:
#             if filterBy_BillingUnit == 'All':
#                 billingUnits = BillingUnit.objects.all()
#                 print "billingUnit***********", billingUnits
#                 if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                 fromDate == None or toDate == None):
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                     fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                            '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,is_new=False,
#                                                                register_date__gte=fromDate1)
#                     consumerfinal_list.extend(consumers)
#                 elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                     toDate1 = datetime.datetime.strptime(str(toDate),
#                                                          '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,
#                                                                register_date__lte=toDate1,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 elif fromDate and toDate:
#                     fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                            '%d/%m/%Y').date()
#                     toDate1 = datetime.datetime.strptime(str(toDate),
#                                                          '%d/%m/%Y').date()
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,
#                                                                register_date__gte=fromDate1,
#                                                                register_date__lte=toDate1,is_new=False)
#                     consumerfinal_list.extend(consumers)
#                 else:
#                     consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,is_new=False)
#                     consumerfinal_list.extend(consumers)

#             else:
#                 print "Billing unit All"
#                 if filterBy_ProcessingCycle == 'All':
#                     billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle
#                                                                             in ProcessingCycle.objects.filter(
#                                                                            B_U__B_U=billingUnit)],
#                                                                    is_deleted=False,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle
#                                                                             in ProcessingCycle.objects.filter(
#                                                                            B_U__B_U=billingUnit)],
#                                                                    is_deleted=False, register_date__gte=fromDate1,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle
#                                                                             in ProcessingCycle.objects.filter(
#                                                                            B_U__B_U=billingUnit)],
#                                                                    is_deleted=False, register_date__lte=toDate1,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle
#                                                                             in ProcessingCycle.objects.filter(
#                                                                            B_U__B_U=billingUnit)],
#                                                                    register_date__gte=fromDate1,
#                                                                    is_deleted=False, register_date__lte=toDate1,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle
#                                                                             in ProcessingCycle.objects.filter(
#                                                                            B_U__B_U=billingUnit)],
#                                                                    is_deleted=False,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                 else:
#                     print " Billing Unit and processing cycle"
#                     # billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                     # processingCycle = ProcessingCycle.objects.get(B_U__B_U=billingUnit, P_C=filterBy_ProcessingCycle)
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle in
#                                                                             ProcessingCycle.objects.filter(
#                                                                                 B_U__B_U=filterBy_BillingUnit,
#                                                                                 P_C=filterBy_ProcessingCycle)],
#                                                                    is_deleted=False,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle in
#                                                                             ProcessingCycle.objects.filter(
#                                                                                 B_U__B_U=filterBy_BillingUnit,
#                                                                                 P_C=filterBy_ProcessingCycle)],
#                                                                    is_deleted=False, register_date__gte=fromDate1,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle in
#                                                                             ProcessingCycle.objects.filter(
#                                                                                 B_U__B_U=filterBy_BillingUnit,
#                                                                                 P_C=filterBy_ProcessingCycle)],
#                                                                    is_deleted=False, register_date__lte=toDate1,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle in
#                                                                             ProcessingCycle.objects.filter(
#                                                                                 B_U__B_U=filterBy_BillingUnit,
#                                                                                 P_C=filterBy_ProcessingCycle)],
#                                                                    register_date__gte=fromDate1,
#                                                                    is_deleted=False, register_date__lte=toDate1,is_new=False)
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    P_C__in=[processingCycle.P_C for processingCycle in
#                                                                             ProcessingCycle.objects.filter(
#                                                                                 B_U__B_U=filterBy_BillingUnit,
#                                                                                 P_C=filterBy_ProcessingCycle)],
#                                                                    is_deleted=False,is_new=False)
#                         consumerfinal_list.extend(consumers)

#         for consumer in set(consumerfinal_list):
#             print "consumer-------------SSSS---", consumer
#             servicerequest = ServiceRequest.objects.filter(is_deleted=False,
#                                                            consumer_id_id=consumer.id).count()
#             complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
#                                                              consumer_id_id=consumer.id).count()
#             feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id).last()
#             print '-----------', feedbackscount
#             edit1 = ''
#             if feedbackscount:
#                 if feedbackscount.stars == 'STAR1':
#                     edit1 = 1
#                 elif feedbackscount.stars == 'STAR2':
#                     edit1 = 2
#                 elif feedbackscount.stars == 'STAR3':
#                     edit1 = 3
#                 elif feedbackscount.stars == 'STAR4':
#                     edit1 = 4
#                 elif feedbackscount.stars == 'STAR5':
#                     edit1 = 5
#                 else:
#                     edit1 = ''
#             objlist = {
#                 'id': consumer.id,
#                 'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
#                 'name': consumer.name,
#                 'consumer_type': consumer.connection_status,
#                 'consumer_no': consumer.consumer_no,
#                 'email_id': consumer.email_id,
#                 'contact_no': consumer.contact_no,
#                 'meter_no': consumer.meter_no,
#                 'servicerequest': servicerequest,
#                 'complaintraised': complaintraised,
#                 'edit1': edit1,
#             }
#             finallist.append(objlist)
#         paginator = Paginator(finallist, 4)  # Show 25 contacts per page
#         page = request.GET.get('page')
#         print "#############dddddd..............request.GET.get('page', 1)................dddddddd#####", page
#         try:
#             consumercardPagination = paginator.page(page)
#         except PageNotAnInteger:  # If page is not an integer, deliver first page.
#             consumercardPagination = paginator.page(1)
#         except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
#             consumercardPagination = paginator.page(paginator.num_pages)
#         data = {'finallist': consumercardPagination}
#         data = render(request, 'consumer/consumerBody.html', data)
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|consumer_card_filter', e
#         data = {'No consumer found': 'error'}
#     return HttpResponse(data)


# # TODO datatable for consumer card list
# def get_consumer_card_list(request):
#     print "here............shubh"
#     data = {}
#     edit1 = ''
#     consumers = ''
#     try:
#         userPaymentList = []
#         userRole = []
#         column = request.GET.get('order[0][column]')
#         print "column---------------", column
#         searchTxt = request.GET.get('search[value]')
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['consumer_no']
#         # column_name = order + list[int(column)]
#         # print "column_name-----------", column_name
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))
#         total_record = ''
#         filterBy_BillCycle = request.GET.get('filterBy_BillCycle')
#         print "filterBy_BillCycle", filterBy_BillCycle
#         filterBy_BillingUnit = request.GET.get('filterBy_BillingUnit')
#         print "###########filterBy_BillingUnit#", filterBy_BillingUnit
#         filterBy_ProcessingCycle = request.GET.get('filterBy_ProcessingCycle')
#         print "###########filterBy_ProcessingCycle#", filterBy_ProcessingCycle
#         fromDate = request.GET.get('filterfromDate')
#         toDate = request.GET.get('filtertoDate')
#         city = request.GET.get('city')
#         total_record = ''
#         consumerfinal_list=[]
#         totalrecord_list=[]
#         # print "\n Bill Cycle = " + filterBy_BillCycle + "\n From Date = " + fromDate + "\n To Date = " + toDate
#         try:
#             total_record = ''
#             if city == 'Muzaffarpur':
#                 consumerfinal_list = []
#                 if filterBy_BillCycle == 'All':
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, is_deleted=False,is_new=False,is_active=True).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, is_deleted=False,is_new=False,is_active=True).order_by('-register_date')[start:length]
#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)

#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, is_deleted=False,
#                                                                       is_active=True,register_date__gte=fromDate1,is_new=False).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, is_deleted=False,
#                                                                    is_active=True,register_date__gte=fromDate1,is_new=False).order_by('-register_date')[start:length]
#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)

#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, is_deleted=False,is_active=True,
#                                                                       register_date__lte=toDate1,is_new=False).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, is_deleted=False,is_active=True,
#                                                                    register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]
#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)

#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, is_deleted=False,
#                                                                       register_date__gte=fromDate1,is_active=True,
#                                                                       register_date__lte=toDate1,is_new=False).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, is_deleted=False,
#                                                                    register_date__gte=fromDate1,is_active=True,
#                                                                    register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]

#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)
#                 else:
#                     print "\n billcycle "
#                     billcycle = BillCycle.objects.get(id=filterBy_BillCycle, is_deleted=False)
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, bill_cycle=billcycle,is_active=True,
#                                                                       is_deleted=False,is_new=False).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, bill_cycle=billcycle,is_active=True,
#                                                                    is_deleted=False,is_new=False).order_by('-register_date')[start:length]
#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)

#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, bill_cycle=billcycle,
#                                                                       is_deleted=False,is_new=False,is_active=True,
#                                                                       register_date__gte=fromDate1).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, bill_cycle=billcycle,
#                                                                    is_deleted=False,is_new=False,is_active=True,
#                                                                    register_date__gte=fromDate1).order_by('-register_date')[start:length]
#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)

#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, bill_cycle=billcycle,
#                                                                       is_deleted=False,is_new=False,is_active=True,
#                                                                       register_date__lte=toDate1).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, bill_cycle=billcycle,
#                                                                    is_deleted=False,is_new=False,is_active=True,
#                                                                    register_date__lte=toDate1).order_by('-register_date')[start:length]
#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)

#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, bill_cycle=billcycle,
#                                                                       register_date__gte=fromDate1,is_active=True,
#                                                                       is_deleted=False,is_new=False,
#                                                                       register_date__lte=toDate1).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, bill_cycle=billcycle,
#                                                                    register_date__gte=fromDate1,
#                                                                    is_deleted=False,is_active=True,
#                                                                    register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]

#                         consumerfinal_list.extend(consumers)
#                         totalrecord_list.append(total_record)
#             else:
#                 print "filterBy_BillingUnit is All"
#                 consumerfinal_list = []
#                 if filterBy_BillingUnit == 'All':
#                     billingUnits = BillingUnit.objects.all()
#                     print "billingUnit***********", billingUnits

#                     # processingCycles = ProcessingCycle.objects.filter(B_U__B_U=billingUnit)

#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)),parent__isnull=True,city__city=city, is_deleted=False,
#                                                                       is_new=False,is_active=True,
#                                                                       B_U__in=[bu.B_U for bu in billingUnits]).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                       city__city=city, is_deleted=False,is_active=True,
#                                                                       is_new=False).order_by('-register_date')[start:length]

#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       city__city=city, is_deleted=False,
#                                                                       B_U__in=[bu.B_U for bu in billingUnits],
#                                                                       register_date__gte=fromDate1,is_active=True,
#                                                                       is_new=False).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    city__city=city, is_deleted=False,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    register_date__gte=fromDate1,is_new=False,is_active=True).order_by('-register_date')[start:length]

#                         consumerfinal_list.extend(consumers)
#                         # totalrecord_list.append(total_record)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       is_deleted=False, B_U__in=[bu.B_U for bu in billingUnits],
#                                                                       city__city=city,
#                                                                       register_date__lte=toDate1,is_active=True,
#                                                                       is_new=False).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    is_deleted=False, B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    city__city=city,is_active=True,
#                                                                    register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]

#                         consumerfinal_list.extend(consumers)
#                         # totalrecord_list.append(total_record)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                       B_U__in=[bu.B_U for bu in billingUnits],
#                                                                       city__city=city, is_deleted=False,
#                                                                       register_date__gte=fromDate1,
#                                                                       register_date__lte=toDate1,is_active=True,
#                                                                       is_new=False).count()
#                         consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                             meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                    is_deleted=False,
#                                                                    register_date__gte=fromDate1,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits],
#                                                                    city__city=city,is_active=True,
#                                                                    register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]

#                         consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                 else:
#                     print "filterBy_BillingUnit is selected"
#                     if filterBy_ProcessingCycle == 'All':
#                         billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                         # processingCycles = ProcessingCycle.objects.filter(B_U__B_U=billingUnit)
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True, is_deleted=False, is_new=False,
#                                                                           city__city=city,is_active=True,B_U=billingUnit).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        city__city=city,is_active=True,B_U=billingUnit,
#                                                                        is_deleted=False,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           city__city=city,B_U=billingUnit,
#                                                                           is_deleted=False,is_active=True,
#                                                                           register_date__gte=fromDate1,
#                                                                           is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        city__city=city, B_U=billingUnit,
#                                                                        is_deleted=False,is_active=True,
#                                                                        register_date__gte=fromDate1,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.extend(total_record)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           B_U=billingUnit,
#                                                                           city__city=city, is_deleted=False,
#                                                                           register_date__lte=toDate1,is_active=True,
#                                                                           is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        city__city=city,B_U=billingUnit,
#                                                                        is_deleted=False,is_active=True,
#                                                                        register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           city__city=city, B_U=billingUnit,
#                                                                           register_date__gte=fromDate1,
#                                                                           is_deleted=False,is_active=True,
#                                                                           register_date__lte=toDate1,
#                                                                           is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        B_U=billingUnit,
#                                                                        city__city=city,
#                                                                        register_date__gte=fromDate1,
#                                                                        is_deleted=False,is_active=True,
#                                                                        register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                         else:
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           city__city=city,  B_U=billingUnit,
#                                                                           is_deleted=False,is_active=True,  is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        city__city=city,  B_U=billingUnit,
#                                                                        is_deleted=False,is_active=True,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                     else:
#                         # billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                         # processingCycle = ProcessingCycle.objects.get(B_U__B_U=filterBy_BillingUnit,
#                         #                                               )
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           city__city=city,B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                           is_deleted=False,is_active=True, is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        city__city=city,B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False,is_active=True,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           city__city=city, B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                           is_deleted=False,is_active=True,
#                                                                           register_date__gte=fromDate1,
#                                                                           is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        city__city=city, B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False,is_active=True,
#                                                                        register_date__gte=fromDate1,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           B_U=filterBy_BillingUnit,
#                                                                           P_C=filterBy_ProcessingCycle,
#                                                                           city__city=city, is_deleted=False,is_active=True,
#                                                                           register_date__lte=toDate1,
#                                                                           is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        city__city=city, B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False,is_active=True,
#                                                                        register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]


#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)
#                         elif fromDate and toDate:

#                             fromDate1 = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                             total_record = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                           city__city=city,B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                           register_date__gte=fromDate1,
#                                                                           is_deleted=False,is_active=True,
#                                                                           register_date__lte=toDate1,
#                                                                           is_new=False).count()
#                             consumers = ConsumerDetails.objects.filter((Q(consumer_no__icontains=searchTxt) | Q(
#                                 meter_no__icontains=searchTxt) | Q(name__icontains=searchTxt)), parent__isnull=True,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        city__city=city, register_date__gte=fromDate1,
#                                                                        is_deleted=False,is_active=True,
#                                                                        register_date__lte=toDate1,is_new=False).order_by('-register_date')[start:length]

#                             consumerfinal_list.extend(consumers)
#                             # totalrecord_list.append(total_record)

#         except Exception, e:
#             print e
#         for consumer in consumerfinal_list:
#             id = consumer.consumer_no
#             id1 = '<a title="consumerCardListViewDetail" style="color: #32c5d2;" onclick="consumerCardListViewDetail(' + str(
#                 consumer.id) + ')" >' + str(id) + '</a>'
#             tempList = []
#             servicerequest = ServiceRequest.objects.filter(is_deleted=False, consumer_id__id=consumer.id).count()
#             complaintraised = ComplaintDetail.objects.filter(is_deleted=False, consumer_id__id=consumer.id).count()
#             feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id__id=consumer.id)
#             print feedbackscount
#             edit1 = ''
#             for feedback1 in feedbackscount:
#                 print feedback1.stars
#                 print "________________________________________"
#                 if feedback1.stars == 'STAR1':
#                     edit1 = '<i class="fa fa-star samp" style="color: #FF8C00;"></i>'
#                 elif feedback1.stars == 'STAR2':

#                     edit1 = '<i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i>'

#                 elif feedback1.stars == 'STAR3':
#                     edit1 = '<i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i>'

#                 elif feedback1.stars == 'STAR4':
#                     edit1 = '<i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i>'
#                 elif feedback1.stars == 'STAR5':
#                     edit1 = '<i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i><i class="fa fa-star samp" style="color: #FF8C00;"></i>'
#                 else:
#                     edit1 = ''
#             if consumer.email_id:
#                 mail = consumer.email_id
#             else:
#                 mail = consumer.alternate_email

#             tempList.append(id1)
#             tempList.append(consumer.name)
#             tempList.append(consumer.contact_no)
#             tempList.append(mail)
#             tempList.append(servicerequest)
#             tempList.append(complaintraised)
#             tempList.append(edit1)
#             userPaymentList.append(tempList)

#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userPaymentList}
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|consumer.py|get_consumer_card_list', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')
#     # return render(request, 'consumer/consumer.html', data)


# # TODO Export to excel for consumer card & list
# def consumer_card_export_to_excel(request):
#     servicecount = 0
#     complaintcount = 0
#     pstatus = ''
#     consumers = ''
#     data = {}
#     consumerfinal_list=[]
#     finallist = []
#     try:
#         city = request.GET.get('city')
#         print city
#         filterBy_BillingUnit = request.GET.get('filterBy_BillingUnit')
#         print filterBy_BillingUnit
#         filterBy_ProcessingCycle = request.GET.get('filterBy_ProcessingCycle')
#         print filterBy_ProcessingCycle
#         filterBy_BillCycle = request.GET.get('filterBy_BillCycle')
#         print filterBy_BillCycle

#         fromDate = request.GET.get('fromDate')
#         toDate = request.GET.get('toDate')
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="consumerCardDetail.csv"';
#         writer = csv.writer(response)
#         # writer = csv.writer(response, delimiter=' ', quotechar='"', quoting=csv.QUOTE_ALL)
#         writer.writerow(
#             ['Consumer ID', 'Consumer Name',  'Contact Number', 'Email_id',
#              'Service Request Count', 'Complaint Count'])

#         try:
#             if city == 'Muzaffarpur':
#                 if filterBy_BillCycle == 'All':
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,is_new=False,is_active=True,).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,
#                                                                    register_date__gte=fromDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,
#                                                                    register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city, is_deleted=False,
#                                                                    register_date__gte=fromDate1,
#                                                                    register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)


#                 else:
#                     print "\n All billcycle All"
#                     billcycle = BillCycle.objects.get(id=filterBy_BillCycle, is_deleted=False)
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False, register_date__gte=fromDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False, register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    register_date__gte=fromDate1,
#                                                                    is_deleted=False, register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    bill_cycle=billcycle,
#                                                                    is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)

#             else:
#                 print "in nagpur"
#                 if filterBy_BillingUnit == 'All':
#                     print "in all"
#                     billingUnits = BillingUnit.objects.all()
#                     print "billingUnit***********", billingUnits
#                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                     fromDate == None or toDate == None):
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,
#                                                                    register_date__gte=fromDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,
#                                                                    register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     elif fromDate and toDate:
#                         fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                '%d/%m/%Y').date()
#                         toDate1 = datetime.datetime.strptime(str(toDate),
#                                                              '%d/%m/%Y').date()
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,
#                                                                    register_date__gte=fromDate1,
#                                                                    register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)
#                     else:
#                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                    B_U__in=[bu.B_U for bu in billingUnits], is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                         consumerfinal_list.extend(consumers)


#                 else:
#                     print "Billing unit All"
#                     if filterBy_ProcessingCycle == 'All':
#                         billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                         # processingCycles = ProcessingCycle.objects.filter(B_U__B_U=billingUnit)
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False, register_date__gte=fromDate1,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False, register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        register_date__gte=fromDate1,
#                                                                        is_deleted=False, register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         else:
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=billingUnit,
#                                                                        is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)

#                     else:
#                         print " Billing Unit and processing cycle"
#                         billingUnit = BillingUnit.objects.get(B_U=filterBy_BillingUnit)
#                         processingCycle = ProcessingCycle.objects.get(B_U__B_U=billingUnit, P_C=filterBy_ProcessingCycle)
#                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
#                                         fromDate == None or toDate == None):
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False, register_date__gte=fromDate1,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False, register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         elif fromDate and toDate:
#                             fromDate1 = datetime.datetime.strptime(str(fromDate),
#                                                                    '%d/%m/%Y').date()
#                             toDate1 = datetime.datetime.strptime(str(toDate),
#                                                                  '%d/%m/%Y').date()
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        register_date__gte=fromDate1,
#                                                                        is_deleted=False, register_date__lte=toDate1,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)
#                         else:
#                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, city__city=city,
#                                                                        B_U=filterBy_BillingUnit,
#                                                                        P_C=filterBy_ProcessingCycle,
#                                                                        is_deleted=False,is_active=True,is_new=False).order_by('-register_date')
#                             consumerfinal_list.extend(consumers)

#         except Exception, e:
#             print e

#         print "===========consumers===========",consumerfinal_list
#         for a in set(consumerfinal_list):
#             print "a.id", a.id
#             tempList = []
#             # request_date = serviceRequest.request_date.strftime('%d/%m/%Y')
#             servicecount = ServiceRequest.objects.filter(consumer_id__id=a.id).count()
#             complaintcount = ComplaintDetail.objects.filter(consumer_id__id=a.id).count()
#             if a.email_id:
#                 mail = a.email_id
#             else:
#                 mail = a.alternate_email
#             tempList.append(a.consumer_no)
#             tempList.append(a.name)
#             tempList.append(a.contact_no)
#             tempList.append(mail)
#             tempList.append(servicecount)
#             tempList.append(complaintcount)
#             writer.writerow(tempList)
#         return response


#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|consumer_card_export_to_excel', e
#         print e
#     data = {'success': 'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')



# def get_consumer_count(request):
#     totals =  ConsumerDetails.objects.filter(parent__isnull=True,
#                                                     city__city=request.user.userprofile.city.city,
#                                                     is_deleted=False,is_active=True, is_new=False).count()
#     print "total count = ",totals
#     total = {
#         'total': totals,
#     }
#     data = {'success': 'true', 'total': total}
#     return HttpResponse(json.dumps(data), content_type='application/json')



# def get_service_count(request):
#     consumerID =  request.GET.get('consumerID')
#     totals = ServiceRequest.objects.filter(is_deleted = False,consumer_id__id=consumerID,consumer_id__city__city=request.user.userprofile.city.city).count()
#     print "total count = ",totals
#     total = {
#         'total': totals,
#     }
#     data = {'success': 'true', 'total': total}
#     return HttpResponse(json.dumps(data), content_type='application/json')

# def get_compliant_count(request):
#     consumerID = request.GET.get('consumerID')
#     totals = ComplaintDetail.objects.filter(is_deleted = False,consumer_id__id=consumerID,consumer_id__city__city=request.user.userprofile.city.city).count()
#     print "total count = ",totals
#     total = {
#         'total': totals,
#     }
#     data = {'success': 'true', 'total': total}
#     return HttpResponse(json.dumps(data), content_type='application/json')



# # TODO Secondary detail view of consumer
# @csrf_exempt
# def consumerdetail(request, consumer_id=None):
#     # pdb.set_trace()
#     data = {}
#     objlist = {}
#     finallist = []
#     billcycles = []
#     conlist = {}
#     consumerlist = []
#     edit1 = ''
#     data = ''
#     lastfeedback_date = ''
#     feedback = ''
#     image_address = ''

#     try:
#         consumer = ConsumerDetails.objects.get(id=consumer_id, is_deleted=False,is_new=False)

#         feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id).last()
#         print"============feedbackscount================", feedbackscount
#         if feedbackscount:
#             if feedbackscount.feedback_date:
#                 lastfeedback_date = feedbackscount.feedback_date.strftime('%d %b %Y')
#             else:
#                 lastfeedback_date = ''
#             feedback = feedbackscount.feedback
#             if feedbackscount.stars == 'STAR1':
#                 edit1 = 1
#             elif feedbackscount.stars == 'STAR2':
#                 edit1 = 2
#             elif feedbackscount.stars == 'STAR3':
#                 edit1 = 3
#             elif feedbackscount.stars == 'STAR4':
#                 edit1 = 4
#             elif feedbackscount.stars == 'STAR5':
#                 edit1 = 5
#             else:
#                 edit1 = ''
#         if consumer.email_id:
#             mail = consumer.email_id
#         else:
#             mail = consumer.alternate_email
#         try:
#             image_address = ''
#             appUser = AppUser.objects.get(consumer=consumer.id)
#             print "===================APPUSER===================== ", appUser
#             image_address = "http://" + get_current_site(request).domain + "/sitemedia/" + str(
#                 appUser.profile_pic)
#             # print str(appUser.profile_pic)
#             print "image_address============", image_address

#         except Exception, e:
#             print '================Exception in AppUser = ', e

#         objlist = {
#             'profile_pic': image_address,
#             'id': consumer.id,
#             'name': consumer.name + ' ' + "(Primary)",
#             'consumer_no': consumer.consumer_no,
#             'email_id': mail,
#             'contact_no': consumer.contact_no,
#             'address_line_1': consumer.address_line_1,
#             'address_line_2': consumer.address_line_2,
#             'address_line_3': consumer.address_line_3,
#             'edit1': edit1,
#             'lastfeedback_date': lastfeedback_date,
#             'feedback': feedback,
#             # 'consumer_type':consumer.consumer_type,
#         }
#         finallist.append(objlist)
#         consumerAll = ConsumerDetails.objects.filter(parent=consumer, is_deleted=False,is_new=False).order_by('-id')[:10]
#         consumerlist.append({'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + " (Primary)",
#                              'consumerid': consumer.id})
#         for i in consumerAll:
#             consumerlist.append({'nameid': i.name + '-' + i.consumer_no,
#                                  'consumerid': i.id})

#         servicerequesttotal = ServiceRequest.objects.filter(is_deleted=False, consumer_id=consumer_id).count()
#         servicerequestType = ServiceRequestType.objects.filter(is_deleted=False)

#         complaintraised = ComplaintDetail.objects.filter(is_deleted=False, consumer_id=consumer_id).count()
#         complaintType = ComplaintType.objects.filter(is_deleted=False)

#         data = {'id': consumer_id, 'finallist': finallist, 'servicerequesttotal': servicerequesttotal,
#                 'servicerequestType': servicerequestType,
#                 'complaintraised': complaintraised, 'complaintType': complaintType, 'consumerlist': consumerlist}
#     except Exception as e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|consumerdetail', e
#         print e
#         pass
#     return render(request, 'consumer/consumerfinal.html', data)


# # TODO Secondary detail view of filter consumer ID
# def get_consumer_account_filterBy(request):
#     try:
#         finallist = []
#         paymentobjlist = {}
#         paymentfinallist = []
#         edit1 = ''
#         lastfeedback_date = ''
#         feedback = ''
#         paymentobj = ''
#         # count = ConsumerDetails.objects.get(id=request.GET.get('filterby'), is_deleted=False).count()
#         print "===================", request.GET.get('filterby')
#         consumer = ConsumerDetails.objects.get(id=request.GET.get('filterby'), is_deleted=False,is_new=False)
#         feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=request.GET.get('filterby')).last()
#         print '-----------', feedbackscount
#         edit1 = ''
#         lastfeedback_date = ''
#         image_address = ''
#         if feedbackscount:
#             if feedbackscount.feedback_date:
#                 lastfeedback_date = feedbackscount.feedback_date.strftime('%d %b %Y')
#             else:
#                 lastfeedback_date = ''
#             feedback = feedbackscount.feedback
#             if feedbackscount.stars == 'STAR1':
#                 edit1 = 1
#             elif feedbackscount.stars == 'STAR2':
#                 edit1 = 2
#             elif feedbackscount.stars == 'STAR3':
#                 edit1 = 3
#             elif feedbackscount.stars == 'STAR4':
#                 edit1 = 4
#             elif feedbackscount.stars == 'STAR5':
#                 edit1 = 5
#             else:
#                 edit1 = ''
#         if consumer.email_id:
#             mail = consumer.email_id
#         else:
#             mail = consumer.alternate_email

#         try:
#             appUser = AppUser.objects.get(consumer=consumer.id)
#             print "===================APPUSER===================== ", appUser
#             image_address = "http://" + get_current_site(request).domain + "/sitemedia/" + str(
#                 appUser.profile_pic)
#             # print str(appUser.profile_pic)
#             print "image_address============", image_address

#         except Exception, e:
#             print '================Exception in AppUser = ', e

#         objlist = {
#             'profile_pic': image_address,
#             'id': consumer.id,
#             'name': consumer.name,
#             'consumer_no': consumer.consumer_no,
#             'email_id': mail,
#             'contact_no': consumer.contact_no,
#             'address_line_1': consumer.address_line_1,
#             'address_line_2': consumer.address_line_2,
#             'address_line_3': consumer.address_line_3,
#             'edit1': edit1,
#             'lastfeedback_date': lastfeedback_date,
#             'feedback': feedback,
#             # 'consumer_type':consumer.consumer_type,
#         }
#         finallist.append(objlist)
#         servicerequesttotal = ServiceRequest.objects.filter(is_deleted=False,
#                                                             consumer_id_id=request.GET.get('filterby')).count()
#         servicerequestType = ServiceRequestType.objects.filter(is_deleted=False)
#         complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
#                                                          consumer_id_id=request.GET.get('filterby')).count()
#         complaintType = ComplaintType.objects.filter(is_deleted=False)
#         data = {'finallist': finallist, 'servicerequesttotal': servicerequesttotal,
#                 'servicerequestType': servicerequestType,
#                 'complaintraised': complaintraised, 'complaintType': complaintType,
#                 'paymentfinallist': paymentfinallist,}
#         data = render(request, 'consumer/consumerDetailBody.html', data)

#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|consumer.py|get-consumer-account-filterBy', e
#         data = {'msg': 'error'}
#     return HttpResponse(data)

# # TODO datatable for bill payment
# def get_consumer_bill_payment_list(request):
#     try:

#         month = None
#         userPaymentList = []
#         userRole = []
#         column = request.GET.get('order[0][column]')
#         print "column---------------", column
#         searchTxt = request.GET.get('search[value]')
#         consumer_id = request.GET.get('id')
#         print "consumer_id@@@@@@@@@@@@@@@", consumer_id

#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['service_type']
#         column_name = order + list[int(column)]
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))
#         total_recordc = ''
#         yearMonth = str(datetime.date.today().year) + checkMonth(datetime.date.today().month)
#         print "yearMonth============>>>>", yearMonth
#         month = month_minus(yearMonth)
#         count = 0
#         print "++++++++++++++++++", month_minus(yearMonth)
#         for billMonth in month:
#             print "!!!!!!!!!billMonth!!!!!!!!!!!!!!", billMonth
#             userRole = PaymentDetail.objects.filter(bill_month=billMonth,
#                                                     consumer_id__city__city=request.user.userprofile.city.city,
#                                                     consumer_id__id=consumer_id,
#                                                     is_deleted=False,consumer_id__is_new=False).order_by('bill_month')
#             if userRole:
#                 count = count + 1

#             # total_recordc = PaymentDetail.objects.filter(bill_month=billMonth, consumer_id_id=consumer_id, is_deleted=False).count()
#             total_recordc = count
#             for role in userRole:
#                 # print "SSSSSSSSSSSSSS", role.bill_month
#                 tempList = []
#                 if role.payment_date:
#                     payment_date = role.payment_date.strftime('%b.%d,%Y')
#                 else:
#                     payment_date = ('------')
#                 tempList.append(role.bill_month)

#                 tempList.append(payment_date)
#                 tempList.append(role.unit_consumed)
#                 tempList.append(role.net_amount)
#                 tempList.append(str(role.bill_amount_paid)[:-3])
#                 tempList.append('Mobile App')
#                 userPaymentList.append(tempList)
#         data = {'iTotalRecords': total_recordc, 'iTotalDisplayRecords': total_recordc, 'aaData': userPaymentList}
#         # print "\n\n\ndata billpaymentlist==========================>>>>>>>>>>>", data
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|consumer.py|get_consumer_bill_payment_list', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')

# #TODO Datatable for service request
# def get_consumer_service_request_list(request):
#     # pdb.set_trace()
#     try:
#         data = {}
#         userServiceList = []
#         column = request.GET.get('order[0][column]')
#         print "\n Column = ", column
#         searchTxt = request.GET.get('search[value]')
#         serviceType = request.GET.get('servicefilterby')
#         print "\n Consumer Service Filter = ", serviceType
#         serviceconsumerID = request.GET.get('id')
#         print "\n Service Consumer ID = ", serviceconsumerID
#         fromdate = request.GET.get('servicefromdate')
#         print "\n Service From date = ", fromdate
#         todate = request.GET.get('servicetodate')
#         print "\n Service To Date = ", todate
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['service_no']
#         column_name = order + list[int(column)]
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))
#         ServiceDetail = ''
#         total_record = ''

#         try:
#             if serviceType == 'All':
#                 if (fromdate == "None" and todate == "None") or (fromdate == '' and todate == ''):
#                     print "\nService No Dates Total All"
#                     total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                  is_deleted=False,consumer_id__is_new=False).count()

#                     ServiceDetail = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                   consumer_id__city__city=request.user.userprofile.city.city,
#                                                                   is_deleted=False,consumer_id__is_new=False).order_by(column_name)[start:length]



#                 else:
#                     if fromdate and (todate == "None" or todate == '' or todate == None):
#                         fromdateValue = datetime.datetime.strptime(str(fromdate), '%d/%m/%Y').date()
#                         print "\nService selectedfromdateValue Total All = ", fromdateValue
#                         # selectedtodateValue = datetime.datetime.strptime(str(selectedtodate), '%d/%m/%Y').date()
#                         # print "\nselectedtodateValue = ", selectedtodateValue

#                         print "\nhereeeeeee Service from date only Total All"

#                         total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                      consumer_id__city__city=request.user.userprofile.city.city,
#                                                                      request_date__gte=fromdateValue,
#                                                                      is_deleted=False,consumer_id__is_new=False).count()

#                         ServiceDetail = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                       consumer_id__city__city=request.user.userprofile.city.city,
#                                                                       request_date__gte=fromdateValue,
#                                                                       is_deleted=False,consumer_id__is_new=False).order_by(column_name)[
#                                         start:length]


#                     elif todate and (fromdate == "None" or fromdate == '' or fromdate == None):
#                         # selectedfromdateValue = datetime.datetime.strptime(str(selectedfromdate), '%d/%m/%Y').date()
#                         # print "\nselectedfromdateValue = ", selectedfromdateValue
#                         todateValue = datetime.datetime.strptime(str(todate), '%d/%m/%Y').date()
#                         todateValue = todateValue + relativedelta(days=1)
#                         print "\nService selectedtodateValue Total All= ", todateValue

#                         print "\nhereeeeeee Service  To Date Only Total All"

#                         total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                      consumer_id__city__city=request.user.userprofile.city.city,
#                                                                      request_date__lte=todateValue,
#                                                                      is_deleted=False,consumer_id__is_new=False).count()

#                         ServiceDetail = ServiceRequest.objects.filter(
#                             (Q(service_type__request_type__icontains=searchTxt)), consumer_id__id=serviceconsumerID,
#                             consumer_id__city__city=request.user.userprofile.city.city, request_date__lte=todateValue,
#                             is_deleted=False,consumer_id__is_new=False).order_by(column_name)[start:length]


#                     elif fromdate and todate:
#                         fromdateValue = datetime.datetime.strptime(str(fromdate), '%d/%m/%Y').date()
#                         print "\nService selectedfromdateValue Total All = ", fromdateValue
#                         todateValue = datetime.datetime.strptime(str(todate), '%d/%m/%Y').date()
#                         todateValue = todateValue + relativedelta(days=1)
#                         # datetime.datetime.strftime(todateValue, "%Y/%m/%d")
#                         # print "hjgfhfvhf", datetime.datetime.strftime(todateValue, "%Y/%m/%d")
#                         print "\nService selectedtodateValue = ", todateValue

#                         print "\nhereeeeeee Service Both the dates Total All "

#                         total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                      consumer_id__city__city=request.user.userprofile.city.city,
#                                                                      request_date__gte=fromdateValue,
#                                                                      request_date__lte=todateValue,
#                                                                      is_deleted=False,consumer_id__is_new=False).count()

#                         ServiceDetail = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                       consumer_id__city__city=request.user.userprofile.city.city,
#                                                                       request_date__gte=fromdateValue,
#                                                                       request_date__lte=todateValue,
#                                                                       is_deleted=False,consumer_id__is_new=False).order_by(column_name)[
#                                         start:length]



#             else:
#                 if fromdate == '' and todate == '':
#                     # if  selectedfromdate == '' and selectedtodate == '':
#                     print "\nNo Dates Total ServiceType "
#                     total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                  consumer_id__city__city=request.user.userprofile.city.city,
#                                                                  service_type__id=serviceType, is_deleted=False,consumer_id__is_new=False).count()

#                     ServiceDetail = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                   consumer_id__city__city=request.user.userprofile.city.city,
#                                                                   service_type__id=serviceType,
#                                                                   is_deleted=False,consumer_id__is_new=False).order_by(column_name)[start:length]


#                 else:
#                     if fromdate and (todate == "None" or todate == '' or todate == None):
#                         fromdateValue = datetime.datetime.strptime(str(fromdate), '%d/%m/%Y').date()
#                         # selectedtodateValue = datetime.datetime.strptime(str(selectedtodate), '%d/%m/%Y').date()
#                         # print "\nselectedtodateValue = ", selectedtodateValue

#                         print "\n From date only Total ServiceType "

#                         total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                      consumer_id__city__city=request.user.userprofile.city.city,
#                                                                      service_type__id=serviceType,
#                                                                      request_date__gte=fromdateValue,
#                                                                      is_deleted=False,consumer_id__is_new=False).count()

#                         ServiceDetail = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                       consumer_id__city__city=request.user.userprofile.city.city,
#                                                                       service_type__id=serviceType,
#                                                                       request_date__gte=fromdateValue,
#                                                                       is_deleted=False,consumer_id__is_new=False).order_by(column_name)[
#                                         start:length]


#                     elif todate and (fromdate == "None" or fromdate == '' or fromdate == None):
#                         # selectedfromdateValue = datetime.datetime.strptime(str(selectedfromdate), '%d/%m/%Y').date()
#                         # print "\nselectedfromdateValue = ", selectedfromdateValue
#                         todateValue = datetime.datetime.strptime(str(todate), '%d/%m/%Y').date()
#                         todateValue = todateValue + relativedelta(days=1)
#                         print "\nselectedtodateValue Total ServiceType ", todateValue

#                         print "\nhereeeeeee To date only Total ServiceType  "

#                         total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                      service_type__id=serviceType,
#                                                                      request_date__lte=todateValue,
#                                                                      is_deleted=False,consumer_id__is_new=False).count()

#                         ServiceDetail = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                       service_type__id=serviceType,
#                                                                       request_date__lte=todateValue,
#                                                                       is_deleted=False,consumer_id__is_new=False).order_by(column_name)[
#                                         start:length]

#                     elif fromdate and todate:
#                         fromdateValue = datetime.datetime.strptime(str(fromdate), '%d/%m/%Y').date()
#                         print "\nselectedfromdateValue  Total ServiceType = ", fromdateValue
#                         todateValue = datetime.datetime.strptime(str(todate), '%d/%m/%Y').date()
#                         todateValue = todateValue + relativedelta(days=1)
#                         print "\nselectedtodateValue = ", todateValue

#                         print "\nhereeeeeee Both dates Total ServiceType "

#                         total_record = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                      consumer_id__city__city=request.user.userprofile.city.city,
#                                                                      service_type__id=serviceType,
#                                                                      request_date__gte=fromdateValue,
#                                                                      request_date__lte=todateValue,
#                                                                      is_deleted=False,consumer_id__is_new=False).count()

#                         ServiceDetail = ServiceRequest.objects.filter(consumer_id__id=serviceconsumerID,
#                                                                       consumer_id__city__city=request.user.userprofile.city.city,
#                                                                       service_type__id=serviceType,
#                                                                       request_date__gte=fromdateValue,
#                                                                       request_date__lte=todateValue,
#                                                                       is_deleted=False,consumer_id__is_new=False).order_by(column_name)[
#                                         start:length]
#         except Exception, e:
#             print e

#         for role in ServiceDetail:
#             id = role.id
#             service_no=role.service_no
#             id1 = '<a title="viewRequestIdDetail" style="color: #32c5d2;" onclick="viewRequestIdDetail(' + str(
#                 role.id) + ')" >' + str(service_no) + '</a>'
#             tempList = []
#             if role.request_date:
#                 request_date = role.request_date.strftime('%b %d,%Y %I:%M %p')
#             else:
#                 request_date = ('------')
#             #
#             consumer_remark = len(role.consumer_remark)
#             if (consumer_remark > 50):
#                 consumer_remark = '<span>' + role.consumer_remark[:50] + ' ......</span>'
#             else:
#                 consumer_remark = role.consumer_remark

#             tempList.append(id1)
#             tempList.append(role.service_type.request_type)
#             tempList.append(consumer_remark)
#             tempList.append(request_date)
#             userServiceList.append(tempList)
#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userServiceList}
#         # print "data servicelist==========================>>>>>>>>>>>", data
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|consumer.py|get_consumer_service_request_list', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')

# #TODO Modal for service request detail
# def request_idDetail(request):
#     print 'Request Show History in service request with---', request.GET
#     consumeraddressA = ''
#     mail=''
#     try:
#         print "========================", request.GET.get('id')
#         serviceRequests = ServiceRequest.objects.filter(id=request.GET.get('id'),consumer_id__is_new=False,
#                                                         consumer_id__city__city=request.user.userprofile.city.city)
#         print "serviceRequest================>>>>", serviceRequests


#         for serviceRequest in serviceRequests:
#             if serviceRequest.consumer_id.email_id:
#                 mail = serviceRequest.consumer_id.email_id
#             else:
#                 mail = serviceRequest.consumer_id.alternate_email

#             consumeraddress1 = serviceRequest.consumer_id.address_line_1
#             consumeraddress2 = serviceRequest.consumer_id.address_line_2
#             consumeraddress3 = serviceRequest.consumer_id.address_line_3
#             if (consumeraddress1 == None or consumeraddress1 == '') and (
#                     consumeraddress2 == None or consumeraddress2 == ''):
#                 if (consumeraddress3 != None):
#                     consumeraddressA = serviceRequest.consumer_id.address_line_3
#                 else:
#                     consumeraddressA = serviceRequest.consumer_id.address_line_3
#             elif (consumeraddress1 == None or consumeraddress1 == ''):
#                 if consumeraddress2 != None:
#                     if (consumeraddress3 == None or consumeraddress3 == ''):
#                         consumeraddressA = serviceRequest.consumer_id.address_line_2
#                     else:
#                         consumeraddressA = serviceRequest.consumer_id.address_line_2 + ', ' + serviceRequest.consumer_id.address_line_3
#                 else:
#                     consumeraddressA = serviceRequest.consumer_id.address_line_2
#             elif (consumeraddress1 == None or consumeraddress1 == '') and (
#                     consumeraddress2 == None or consumeraddress2 == '') and (
#                     consumeraddress3 == None or consumeraddress3 == ''):
#                 consumeraddressA = serviceRequest.consumer_id.address_line_1
#             elif (consumeraddress1 != None) and (consumeraddress2 != None):
#                 if (consumeraddress3 == None or consumeraddress3 == ''):
#                     consumeraddressA = serviceRequest.consumer_id.address_line_1 + ', ' + serviceRequest.consumer_id.address_line_2
#                 else:
#                     consumeraddressA = serviceRequest.consumer_id.address_line_1 + ', ' + serviceRequest.consumer_id.address_line_2 + ', ' + serviceRequest.consumer_id.address_line_3
#             else:
#                 consumeraddressA = ''

#             serviceRequestDetail = {
#                 'requestId': serviceRequest.service_no,
#                 'requestType': serviceRequest.service_type.request_type,
#                 'requestStatus': serviceRequest.status,
#                 'consumerName': serviceRequest.consumer_id.name,
#                 'consumerNumber': serviceRequest.consumer_id.consumer_no,
#                 'consumerEmailID': mail,
#                 'consumeraddress1': consumeraddressA,
#                 'consumerRemark': serviceRequest.consumer_remark,
#                 'colsureRemark': serviceRequest.closure_remark,
#             }

#         data = {'success': 'true', 'serviceRequestDetail': serviceRequestDetail}
#         print 'Request show history out service request with---', data
#     except Exception, e:
#         print e
#     return HttpResponse(json.dumps(data), content_type='application/json')

# # TODO datatable for complaint raised
# def get_consumer_complaint_raised_list(request):
#     # pdb.set_trace()
#     try:
#         data = {}
#         userComplaintList = []
#         column = request.GET.get('order[0][column]')
#         print "column", column
#         searchTxt = request.GET.get('search[value]')

#         complaintType = request.GET.get('complaintfilterby')
#         print "\n Consumer Complaint Filter = ", complaintType
#         consumerID = request.GET.get('id')
#         print "\n Consumer ID = ", consumerID
#         fromDate = request.GET.get('complaintfromdate')
#         print " \n Consumer Complaint From Date = ", fromDate
#         toDate = request.GET.get('complainttodate')
#         print "\n Consumer Complaint To Date = ", toDate

#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['id']
#         column_name = order + list[int(column)]
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))
#         complaintDetail = ''
#         total_record = ''

#         try:
#             if complaintType == 'All':
#                 print "here yeah"
#                 try:
#                     if (fromDate == "None" and toDate == "None") or (fromDate == '' and toDate == ''):
#                         # if selectedFromDate == '' and selectedToDate == '' :
#                         print "\nNo Dates and all"
#                         # print selectedFromDate
#                         # print selectedToDate
#                         total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                       # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                       Q(consumer_id__name__icontains=searchTxt) |
#                                                                       Q(
#                                                                           consumer_id__consumer_no__icontains=searchTxt),
#                                                                       consumer_id__id=consumerID,
#                                                                       is_deleted=False).count()

#                         complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                          # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                          Q(consumer_id__name__icontains=searchTxt) |
#                                                                          Q(
#                                                                              consumer_id__consumer_no__icontains=searchTxt),
#                                                                          consumer_id__id=consumerID,
#                                                                          is_deleted=False).order_by(column_name)[
#                                           start:length]

#                     else:
#                         if fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                             fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                             print "\nselectedFromDateValue = ", fromDateValue
#                             # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
#                             # print "\nselectedToDateValue = ", selectedToDateValue

#                             print "\nhereeeeeee from date only All"

#                             total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                           # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                           Q(
#                                                                               consumer_id__name__icontains=searchTxt) |
#                                                                           Q(
#                                                                               consumer_id__consumer_no__icontains=searchTxt),
#                                                                           consumer_id__id=consumerID,
#                                                                           complaint_date__gte=fromDateValue,
#                                                                           # complaint_date__lte=selectedToDateValue,
#                                                                           is_deleted=False).count()

#                             complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                              # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                              Q(
#                                                                                  consumer_id__name__icontains=searchTxt) |
#                                                                              Q(
#                                                                                  consumer_id__consumer_no__icontains=searchTxt),
#                                                                              consumer_id__id=consumerID,
#                                                                              complaint_date__gte=fromDateValue,
#                                                                              # complaint_date__lte=selectedToDateValue,
#                                                                              is_deleted=False).order_by(
#                                 column_name)[start:length]

#                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                             # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
#                             # print "\nselectedFromDateValue = ", selectedFromDateValue
#                             toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                             toDateValue = toDateValue + relativedelta(days=1)
#                             print "\nselectedToDateValue = ", toDateValue

#                             print "\nhereeeeeee  To Date Only All"

#                             total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                           # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                           Q(
#                                                                               consumer_id__name__icontains=searchTxt) |
#                                                                           Q(
#                                                                               consumer_id__consumer_no__icontains=searchTxt),
#                                                                           consumer_id__id=consumerID,
#                                                                           # complaint_date__gte=selectedFromDateValue,
#                                                                           complaint_date__lte=toDateValue,
#                                                                           is_deleted=False).count()

#                             complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                              # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                              Q(
#                                                                                  consumer_id__name__icontains=searchTxt) |
#                                                                              Q(
#                                                                                  consumer_id__consumer_no__icontains=searchTxt),
#                                                                              consumer_id__id=consumerID,
#                                                                              #   complaint_date__gte=selectedFromDateValue,
#                                                                              complaint_date__lte=toDateValue,
#                                                                              is_deleted=False).order_by(
#                                 column_name)[start:length]
#                         elif fromDate and toDate:
#                             fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                             print "\nselectedFromDateValue = ", fromDateValue
#                             toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                             toDateValue = toDateValue + relativedelta(days=1)
#                             print "\nselectedToDateValue = ", toDateValue

#                             print "\nhereeeeeee Both the dates All"

#                             total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                           # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                           Q(
#                                                                               consumer_id__name__icontains=searchTxt) |
#                                                                           Q(
#                                                                               consumer_id__consumer_no__icontains=searchTxt),
#                                                                           consumer_id__id=consumerID,
#                                                                           complaint_date__gte=fromDateValue,
#                                                                           complaint_date__lte=toDateValue,
#                                                                           is_deleted=False).count()

#                             complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                              # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                              Q(
#                                                                                  consumer_id__name__icontains=searchTxt) |
#                                                                              Q(
#                                                                                  consumer_id__consumer_no__icontains=searchTxt),
#                                                                              consumer_id__id=consumerID,
#                                                                              complaint_date__gte=fromDateValue,
#                                                                              complaint_date__lte=toDateValue,
#                                                                              is_deleted=False).order_by(
#                                 column_name)[start:length]



#                 except Exception, e:
#                     print e

#             else:
#                 if fromDate == '' and toDate == '':
#                     # if  selectedFromDate == '' and selectedToDate == '':
#                     print "\nNo Dates selected complaint all"

#                     total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                   # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                   Q(consumer_id__name__icontains=searchTxt) |
#                                                                   Q(consumer_id__consumer_no__icontains=searchTxt),
#                                                                   consumer_id__id=consumerID,
#                                                                   complaint_type_id=complaintType,
#                                                                   is_deleted=False).count()

#                     complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                      # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                      Q(consumer_id__name__icontains=searchTxt) |
#                                                                      Q(
#                                                                          consumer_id__consumer_no__icontains=searchTxt),
#                                                                      consumer_id__id=consumerID,
#                                                                      complaint_type_id=complaintType,
#                                                                      is_deleted=False).order_by(column_name)[
#                                       start:length]


#                 else:
#                     if fromDate and (toDate == "None" or toDate == '' or toDate == None):
#                         fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         print "\nselectedFromDateValue = ", fromDateValue
#                         # selectedToDateValue = datetime.datetime.strptime(str(selectedToDate), '%d/%m/%Y').date()
#                         # print "\nselectedToDateValue = ", selectedToDateValue

#                         print "\nhereeeeeee from date only selected complaint all"

#                         total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                       # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                       Q(consumer_id__name__icontains=searchTxt) |
#                                                                       Q(
#                                                                           consumer_id__consumer_no__icontains=searchTxt),
#                                                                       consumer_id__id=consumerID,
#                                                                       complaint_type_id=complaintType,
#                                                                       complaint_date__gte=fromDateValue,
#                                                                       # complaint_date__lte=selectedToDateValue,
#                                                                       is_deleted=False).count()

#                         complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                          # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                          Q(consumer_id__name__icontains=searchTxt) |
#                                                                          Q(
#                                                                              consumer_id__consumer_no__icontains=searchTxt),
#                                                                          consumer_id__id=consumerID,
#                                                                          complaint_type_id=complaintType,
#                                                                          complaint_date__gte=fromDateValue,
#                                                                          # complaint_date__lte=selectedToDateValue,
#                                                                          is_deleted=False).order_by(column_name)[
#                                           start:length]

#                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
#                         # selectedFromDateValue = datetime.datetime.strptime(str(selectedFromDate), '%d/%m/%Y').date()
#                         # print "\nselectedFromDateValue = ", selectedFromDateValue
#                         toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         toDateValue = toDateValue + relativedelta(days=1)
#                         print "\nselectedToDateValue = ", toDateValue

#                         print "\nhereeeeeee To date only selected complaint all"

#                         total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                       # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                       Q(consumer_id__name__icontains=searchTxt) |
#                                                                       Q(
#                                                                           consumer_id__consumer_no__icontains=searchTxt),
#                                                                       consumer_id__id=consumerID,
#                                                                       # complaint_date__gte=selectedFromDateValue,
#                                                                       complaint_type_id=complaintType,
#                                                                       complaint_date__lte=toDateValue,
#                                                                       is_deleted=False).count()

#                         complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                          # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                          Q(consumer_id__name__icontains=searchTxt) |
#                                                                          Q(
#                                                                              consumer_id__consumer_no__icontains=searchTxt),
#                                                                          consumer_id__id=consumerID,
#                                                                          # complaint_date__gte=selectedFromDateValue,
#                                                                          complaint_type_id=complaintType,
#                                                                          complaint_date__lte=toDateValue,
#                                                                          is_deleted=False).order_by(column_name)[
#                                           start:length]
#                     elif fromDate and toDate:
#                         fromDateValue = datetime.datetime.strptime(str(fromDate), '%d/%m/%Y').date()
#                         print "\nselectedFromDateValue = ", fromDateValue
#                         toDateValue = datetime.datetime.strptime(str(toDate), '%d/%m/%Y').date()
#                         toDateValue = toDateValue + relativedelta(days=1)
#                         print "\nselectedToDateValue = ", toDateValue

#                         print "\nhereeeeeee Both dates selected complaint all"

#                         total_record = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                       # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                       Q(consumer_id__name__icontains=searchTxt) |
#                                                                       Q(
#                                                                           consumer_id__consumer_no__icontains=searchTxt),
#                                                                       consumer_id__id=consumerID,
#                                                                       complaint_type_id=complaintType,
#                                                                       complaint_date__gte=fromDateValue,
#                                                                       complaint_date__lte=toDateValue,
#                                                                       is_deleted=False).count()

#                         complaintDetail = ComplaintDetail.objects.filter(Q(complaint_no__icontains=searchTxt) |
#                                                                          # Q(complaint_type_id__complaint_type__icontains=searchTxt) |
#                                                                          Q(consumer_id__name__icontains=searchTxt) |
#                                                                          Q(
#                                                                              consumer_id__consumer_no__icontains=searchTxt),
#                                                                          consumer_id__id=consumerID,
#                                                                          complaint_type_id=complaintType,
#                                                                          complaint_date__gte=fromDateValue,
#                                                                          complaint_date__lte=toDateValue,
#                                                                          is_deleted=False).order_by(column_name)[
#                                           start:length]



#                         # print "\n Complaint Detail = ",complaintDetail
#         except Exception, e:
#             print e

#         for role in complaintDetail:
#             id = role.complaint_no
#             id1 = '<a title="complaintIdModal" onclick="complaintIdModal(' + str(
#                 role.id) + ')" >' + str(id) + '</a>'
#             tempList = []
#             if role.complaint_date:
#                 complaint_date = role.complaint_date.strftime('%b %d, %Y  %I:%M %p')
#             else:
#                 complaint_date = ('------')

#             # remark='<span>'+ role.remark[:50] + ' ......</span>'

#             remark = len(role.remark)
#             if (remark > 50):
#                 remark = '<span>' + role.remark[:50] + ' ......</span>'
#             else:
#                 remark = role.remark
#             tempList.append(id1)
#             tempList.append(role.complaint_type_id.complaint_type)
#             tempList.append(complaint_date)
#             tempList.append(remark)

#             userComplaintList.append(tempList)

#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userComplaintList}
#         print "data servicelist==========================>>>>>>>>>>>", data
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|consumer.py|get_consumer_complaint_raised_list', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')

# # TODO modal for complaint raised
# def get_complaint_id_modal(request):
#     print 'Complaint ID Column Detail---', request.GET
#     try:
#         complaintDetail = ComplaintDetail.objects.filter(id=request.GET.get('id'),
#                                                          consumer_id__city__city=request.user.userprofile.city.city)
#         print "ComplaintDetail================>>>>", complaintDetail
#         for complaint in complaintDetail:
#             image_address = "http://" + get_current_site(request).domain + "/sitemedia/" + str(complaint.complaint_img)
#             complaintIdDetail = {
#                 'complaintID': complaint.complaint_no,
#                 'complaintType': complaint.complaint_type_id.complaint_type,
#                 'complaintConsumerName': complaint.consumer_id.name,
#                 'complaintConsumerNo': complaint.consumer_id.consumer_no,
#                 'complaintStatus': complaint.complaint_status,
#                 'consumerRemark': complaint.remark,
#                 'closureRemark': complaint.closure_remark,
#                 'complaint_img': image_address,

#             }

#             data = {'success': 'true', 'complaintIdDetail': complaintIdDetail}
#             print 'Request show history out service request with---', data


#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|get_complaint_id_modal', e
#         data = {'success': 'false', 'error': 'Exception ' + str(e)}
#     return HttpResponse(json.dumps(data), content_type='application/json')








# def get_consumer_filterBy_complaint(request):
#     try:

#         serviceType = request.GET.get('filterby')
#         consumer_id = request.GET.get('id')
#         data = {'success': 'true', 'serviceType': serviceType}
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|consumer.py|get-filterBy-consumer', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')


# def consumer_service_request_export_to_excel(request):
#     try:
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="consumerDservice.csv"';
#         writer = csv.writer(response)
#         # writer = csv.writer(response, delimiter=' ', quotechar='"', quoting=csv.QUOTE_ALL)
#         writer.writerow(['Request ID', 'Service Request Type', 'Requested Date', 'Remarks'])

#         serviceRequests = ServiceRequest.objects.filter(is_deleted=False)
#         print "serviceRequests***************************", serviceRequests
#         for serviceRequest in serviceRequests:
#             tempList = []
#             # request_date = serviceRequest.request_date.strftime('%d/%m/%Y')
#             tempList.append(serviceRequest.id)
#             tempList.append(serviceRequest.service_type.request_type)
#             tempList.append(serviceRequest.closure_remark)
#             # tempList.append(request_date)

#             writer.writerow(tempList)
#         return response
#     except Exception, e:
#         print e
#     data = {'success': 'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')


# def consumer_complaint_raised_export_to_excel(request):
#     try:
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="ConsumerDComplaint.csv"';
#         writer = csv.writer(response)
#         # writer = csv.writer(response, delimiter=' ', quotechar='"', quoting=csv.QUOTE_ALL)
#         writer.writerow(['Request ID', 'Complaint Type', 'Raised On', 'Remark'])

#         complaintDetail = ComplaintDetail.objects.filter(is_deleted=False)
#         total_record = complaintDetail.filter().count()
#         for role in complaintDetail:
#             tempList = []
#             if role.complaint_date:
#                 complaint_date = role.complaint_date.strftime('%b %d,%Y %I:%M %p')
#             else:
#                 complaint_date = ('------')

#             tempList.append(role.id)
#             tempList.append(role.complaint_type_id.complaint_type)
#             tempList.append(complaint_date)
#             tempList.append(role.remark)

#             writer.writerow(tempList)
#         return response
#     except Exception, e:
#         print e
#     data = {'success': 'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')


# # @csrf_exempt
# # def consumer_zone_filter(request):
# #     route_list = []
# #     try:
# #         zoneid=request.POST.get('zone')
# #         if zoneid != 'All':
# #             zones = Zone.objects.get(id=request.POST.get('zone'))
# #             print "zones&&&&&&&&&&&&&&&&&&&&&------",zones
# #             billcycle = BillCycle.objects.filter(zone__zone_name=zones)
# #             print "billcycle-------------------",billcycle
# #         else:
# #             billcycle = BillCycle.objects.all()
# #         for cycle in billcycle:
# #             id = cycle.id
# #             bill_cycle_code = cycle.bill_cycle_code
# #             route_list.append({'cycle_code':bill_cycle_code,'id':id})
# #         data = {'route_list': route_list}
# #         print "data----------------",data
# #     except Exception, e:
# #         print 'exception ', str(traceback.print_exc())
# #         print 'Exception|views.py|consumer_zone_filter', e
# #         data = {'route_list': 'none', 'message': 'No route available'}
# #     return HttpResponse(json.dumps(data), content_type='application/json')
# #
# # # @csrf_exempt
# # # def consumer_cycle_filter(request):
# # #     route_list = []
# # #     try:
# # #         billcycle = BillCycle.objects.get(id=request.POST.get('cycle'))
# # #         print "billcycle-------------------",billcycle
# # #         consumerDetails = ConsumerDetails.objects.filter(bill_cycle__bill_cycle_code=billcycle)
# # #         print "consumerDetails---------------",consumerDetails
# # #         for consumer in consumerDetails:
# # #             paymentDetail = PaymentDetail.objects.filter(consumer_id=consumer)
# # #             for payment in paymentDetail:
# # #                 id = payment.id
# # #                 payment_done = payment.payment_done
# # #                 route_list.append({'payment_done':payment_done,'id':id})
# # #         data = {'route_list': route_list}
# # #         print "data----------------",data
# # #     except Exception, e:
# # #         print 'exception ', str(traceback.print_exc())
# # #         print 'Exception|views.py|consumer_card_filter', e
# # #         data = {'route_list': 'none', 'message': 'No route available'}
# # #     return HttpResponse(json.dumps(data), content_type='application/json')
# #
# #
# # # def consumer_card_filter1(request):
# # #     # pdb.set_trace()
# # #     edit1=''
# # #     netamount=''
# # #     payment_done=''
# # #     consumers=''
# # #     paymentMode=''
# # #     try:
# # #         data = {}
# # #         finallist = []
# # #         filterBy_zone = request.GET.get('filterBy_zone')
# # #         filterBy_BillCycle = request.GET.get('filterBy_BillCycle')
# # #         filterBy_Payment = request.GET.get('filterBy_Payment')
# # #         fromDate=request.GET.get('fromDate')
# # #         toDate=request.GET.get('toDate')
# # #         yearMonth = str(datetime.date.today().year) + checkMonth(datetime.date.today().month)
# # #         print "yearMonth============>>>>", yearMonth
# # #
# # #         print "\n filterBy_zone = "+filterBy_zone+"\n Bill Cycle = "+ filterBy_BillCycle+"\n Payment Mode = "+ filterBy_Payment+"\n From Date = "+fromDate+"\n To Date = "+toDate
# # #
# # #         if filterBy_zone == 'All':
# # #             if filterBy_BillCycle == 'All':
# # #                 if filterBy_Payment == 'All':
# # #                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
# # #                                     fromDate == None or toDate == None):
# # #                       consumers = ConsumerDetails.objects.filter(parent__isnull=True,is_deleted=False)
# # #                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                         fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False,register_date__gte=fromDate1)
# # #                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                         toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                              '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False,
# # #                                                                    register_date__lte=toDate1)
# # #                     elif fromDate and  toDate :
# # #                         fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                '%d/%m/%Y').date()
# # #                         toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                              '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False,register_date__gte=fromDate1,
# # #                                                                    register_date__lte=toDate1)
# # #                     else:
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, is_deleted=False)
# # #
# # #                 else :
# # #                     paymentDone = PaymentDetail.objects.filter(payment_done=filterBy_Payment,bill_month=yearMonth)
# # #                     for payment in paymentDone:
# # #                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
# # #                                         fromDate == None or toDate == None):
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,is_deleted=False)
# # #
# # #                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                    '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                        register_date__gte=fromDate1,is_deleted=False)
# # #                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                        register_date__lte=toDate1,is_deleted=False)
# # #                         elif fromDate and  toDate :
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                    '%d/%m/%Y').date()
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                        register_date__gte=fromDate1,
# # #                                                                        register_date__lte=toDate1,is_deleted=False)
# # #                         else:
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id, parent__isnull=True,
# # #                                                                        is_deleted=False)
# # #
# # #
# # #             else:
# # #                 print "\n All billcycle All"
# # #                 billcycle = BillCycle.objects.get(id=filterBy_BillCycle, is_deleted=False)
# # #                 if filterBy_Payment == 'All':
# # #                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
# # #                                     fromDate == None or toDate == None):
# # #                        consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                is_deleted=False)
# # #                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                         fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                    is_deleted=False,register_date__gte=fromDate1)
# # #                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                         toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                              '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                    is_deleted=False, register_date__lte=toDate1)
# # #                     elif fromDate and  toDate :
# # #                         fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                '%d/%m/%Y').date()
# # #                         toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                              '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,register_date__gte=fromDate1,
# # #                                                                    is_deleted=False, register_date__lte=toDate1)
# # #                     else:
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                    is_deleted=False)
# # #
# # #                 else:
# # #                     print "\n All BCC Payment"
# # #                     # billcycle = BillCycle.objects.get(id=filterBy_BillCycle, is_deleted=False)
# # #                     paymentDone = PaymentDetail.objects.filter(payment_done=filterBy_Payment,bill_month=yearMonth)
# # #                     for payment in paymentDone:
# # #                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
# # #                                         fromDate == None or toDate == None):
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,bill_cycle=billcycle,parent__isnull=True)
# # #                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                    '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                        bill_cycle=billcycle,register_date__gte=fromDate1)
# # #                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                        bill_cycle=billcycle, register_date__lte=toDate1)
# # #                         elif fromDate and  toDate :
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                    '%d/%m/%Y').date()
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                        register_date__gte=fromDate1,bill_cycle=billcycle,
# # #                                                                        register_date__lte=toDate1)
# # #                         else:
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id, bill_cycle=billcycle,
# # #                                                                        parent__isnull=True)
# # #
# # #
# # #         else:
# # #             print "\n Zone All All",filterBy_zone
# # #             zones = Zone.objects.get(id=filterBy_zone, is_deleted=False)
# # #             print "zones##############",zones
# # #             billcycles = BillCycle.objects.filter(zone=zones, is_deleted=False)
# # #             if filterBy_BillCycle == 'All':
# # #                if filterBy_Payment == 'All':
# # #                    for billcycle in billcycles:
# # #                     # consumers = ConsumerDetails.objects.filter(parent__isnull=True,bill_cycle=billcycle
# # #                         print "billcycle***************************",billcycle
# # #                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
# # #                                         fromDate == None or toDate == None):
# # #                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle)
# # #                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                    '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                        register_date__gte=fromDate1)
# # #                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                        register_date__lte=toDate1)
# # #                         elif fromDate and toDate:
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                    '%d/%m/%Y').date()
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                        register_date__gte=fromDate1,
# # #                                                                        register_date__lte=toDate1)
# # #                         else:
# # #                             consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle)
# # #                         for consumer in consumers:
# # #                            print "consumer-------------SSSS---", consumer
# # #                            paymentDetail = PaymentDetail.objects.filter(is_deleted=False, consumer_id_id=consumer.id)
# # #                            print "paymentDetail------------------", paymentDetail
# # #                            servicerequest = ServiceRequest.objects.filter(is_deleted=False,
# # #                                                                           consumer_id_id=consumer.id).count()
# # #                            complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
# # #                                                                             consumer_id_id=consumer.id).count()
# # #                            feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id)
# # #                            # print feedbackscount
# # #                            for feedback1 in feedbackscount:
# # #
# # #                                feedback = feedback1.feedback
# # #                                if feedback1.stars == 'STAR1':
# # #                                    edit1 = 1
# # #                                elif feedback1.stars == 'STAR2':
# # #                                    edit1 = 2
# # #                                elif feedback1.stars == 'STAR3':
# # #                                    edit1 = 3
# # #                                elif feedback1.stars == 'STAR4':
# # #                                    edit1 = 4
# # #                                else:
# # #                                    edit1 = 5
# # #                            for paymentD in paymentDetail:
# # #                                netamount = paymentD.bill_amount_paid,
# # #                                payment_done = paymentD.payment_done
# # #                                paymentMode = paymentD.payment_mode
# # #                            objlist = {
# # #                                'id': consumer.id,
# # #                                'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
# # #                                'name': consumer.name,
# # #                                'consumer_type': consumer.connection_status,
# # #                                'dtc': consumer.dtc,
# # #                                'consumer_no': consumer.consumer_no,
# # #                                'pole_no': consumer.pole_no,
# # #                                'email_id': consumer.email_id,
# # #                                'contact_no': consumer.contact_no,
# # #                                'address_line_1': consumer.address_line_1,
# # #                                'meter_no': consumer.meter_no,
# # #                                'netamountpaid': netamount,
# # #                                'paymentStatus': payment_done,
# # #                                'paymentMode': paymentMode,
# # #                                'servicerequest': servicerequest,
# # #                                'complaintraised': complaintraised,
# # #                                'edit1': edit1,
# # #                            }
# # #                            finallist.append(objlist)
# # #
# # #                else:
# # #                    print "\n Zone All Payment"
# # #                    paymentDone = PaymentDetail.objects.filter(payment_done=filterBy_Payment,bill_month=yearMonth)
# # #                    zones = Zone.objects.get(id=filterBy_zone, is_deleted=False)
# # #                    billcycles = BillCycle.objects.filter(zone=zones, is_deleted=False)
# # #                    for billcycle in billcycles:
# # #                        for payment in paymentDone:
# # #                            if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (fromDate == None or toDate == None):
# # #                                 consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,bill_cycle=billcycle)
# # #
# # #
# # #                            elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                                fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                       '%d/%m/%Y').date()
# # #                                consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,bill_cycle=billcycle,
# # #                                                                           register_date__gte=fromDate1)
# # #                            elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                                toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                     '%d/%m/%Y').date()
# # #                                consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                           register_date__lte=toDate1,bill_cycle=billcycle)
# # #                            elif fromDate and toDate:
# # #                                fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                       '%d/%m/%Y').date()
# # #                                toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                     '%d/%m/%Y').date()
# # #                                consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,parent__isnull=True,
# # #                                                                           register_date__gte=fromDate1,
# # #                                                                          register_date__lte=toDate1,bill_cycle=billcycle)
# # #                            else:
# # #                                consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,
# # #                                                                           parent__isnull=True, bill_cycle=billcycle)
# # #                            for consumer in consumers:
# # #                                print "consumer-------------SSSS---", consumer
# # #                                paymentDetail = PaymentDetail.objects.filter(is_deleted=False,
# # #                                                                             consumer_id_id=consumer.id)
# # #                                print "paymentDetail------------------", paymentDetail
# # #                                servicerequest = ServiceRequest.objects.filter(is_deleted=False,
# # #                                                                               consumer_id_id=consumer.id).count()
# # #                                complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
# # #                                                                                 consumer_id_id=consumer.id).count()
# # #                                feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id)
# # #                                # print feedbackscount
# # #                                for feedback1 in feedbackscount:
# # #
# # #                                    feedback = feedback1.feedback
# # #                                    if feedback1.stars == 'STAR1':
# # #                                        edit1 = 1
# # #                                    elif feedback1.stars == 'STAR2':
# # #                                        edit1 = 2
# # #                                    elif feedback1.stars == 'STAR3':
# # #                                        edit1 = 3
# # #                                    elif feedback1.stars == 'STAR4':
# # #                                        edit1 = 4
# # #                                    else:
# # #                                        edit1 = 5
# # #                                for paymentD in paymentDetail:
# # #                                    netamount = paymentD.bill_amount_paid,
# # #                                    payment_done = paymentD.payment_done
# # #                                    paymentMode = paymentD.payment_mode
# # #                                objlist = {
# # #                                    'id': consumer.id,
# # #                                    'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
# # #                                    'name': consumer.name,
# # #                                    'consumer_type': consumer.connection_status,
# # #                                    'dtc': consumer.dtc,
# # #                                    'consumer_no': consumer.consumer_no,
# # #                                    'pole_no': consumer.pole_no,
# # #                                    'email_id': consumer.email_id,
# # #                                    'contact_no': consumer.contact_no,
# # #                                    'address_line_1': consumer.address_line_1,
# # #                                    'meter_no': consumer.meter_no,
# # #                                    'netamountpaid': netamount,
# # #                                    'paymentStatus': payment_done,
# # #                                    'paymentMode': paymentMode,
# # #                                    'servicerequest': servicerequest,
# # #                                    'complaintraised': complaintraised,
# # #                                    'edit1': edit1,
# # #                                }
# # #                                finallist.append(objlist)
# # #
# # #
# # #             else:
# # #                 print "\n Zone BCC All"
# # #                 if filterBy_Payment == 'All':
# # #                     zones = Zone.objects.get(id=filterBy_zone, is_deleted=False)
# # #                     print "Zones======================>>>>", zones
# # #                     print filterBy_BillCycle
# # #                     billcycle = BillCycle.objects.get(zone=zones,id=filterBy_BillCycle, is_deleted=False)
# # #                     print billcycle
# # #                     if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
# # #                                     fromDate == None or toDate == None):
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                    is_deleted=False)
# # #
# # #                     elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                         fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                    is_deleted=False,register_date__gte=fromDate1)
# # #
# # #
# # #                     elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                         toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                              '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                    register_date__lte=toDate1)
# # #                     elif fromDate and toDate:
# # #                         fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                '%d/%m/%Y').date()
# # #                         toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                              '%d/%m/%Y').date()
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                    register_date__gte=fromDate1,
# # #                                                                    register_date__lte=toDate1)
# # #                     else:
# # #                         consumers = ConsumerDetails.objects.filter(parent__isnull=True, bill_cycle=billcycle,
# # #                                                                is_deleted=False)
# # #
# # #
# # #                 else:
# # #                     print "\n Zone BCC Payment"
# # #                     paymentDone = PaymentDetail.objects.filter(payment_done=filterBy_Payment,bill_month=yearMonth)
# # #                     print "paymentDone+++++++++++++++++++", paymentDone
# # #
# # #                     zones = Zone.objects.get(id=filterBy_zone, is_deleted=False)
# # #                     print "Zones======================>>>>", zones
# # #                     billcycle = BillCycle.objects.get(zone=zones, id=filterBy_BillCycle,
# # #                                                       is_deleted=False)
# # #                     for payment in paymentDone:
# # #                         if (fromDate == '' and toDate == '') or (fromDate == 'None' and toDate == 'None') or (
# # #
# # #                                         fromDate == None or toDate == None):
# # #
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,bill_cycle=billcycle,parent__isnull=True)
# # #
# # #                         elif fromDate and (toDate == "None" or toDate == '' or toDate == None):
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #
# # #                                                                    '%d/%m/%Y').date()
# # #
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,bill_cycle=billcycle,
# # #
# # #                                                                        register_date__gte=fromDate1,parent__isnull=True)
# # #                         elif toDate and (fromDate == "None" or fromDate == '' or fromDate == None):
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,bill_cycle=billcycle,
# # #                                                                        register_date__lte=toDate1,parent__isnull=True)
# # #
# # #                         elif fromDate and toDate:
# # #                             print "hello here-------------"
# # #
# # #                             fromDate1 = datetime.datetime.strptime(str(fromDate),
# # #                                                                    '%d/%m/%Y').date()
# # #                             toDate1 = datetime.datetime.strptime(str(toDate),
# # #                                                                  '%d/%m/%Y').date()
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id,bill_cycle=billcycle,
# # #                                                                        register_date__gte=fromDate1,
# # #                                                                        register_date__lte=toDate1,parent__isnull=True)
# # #                         else:
# # #                             consumers = ConsumerDetails.objects.filter(id=payment.consumer_id.id, bill_cycle=billcycle,
# # #                                                                        parent__isnull=True)
# # #
# # #
# # #         print "_____________fgbrfg__________________"
# # #         for consumer in consumers:
# # #             print "consumer-------------SSSS---",consumer
# # #             paymentDetail = PaymentDetail.objects.filter(is_deleted=False, consumer_id_id=consumer.id)
# # #             print "paymentDetail------------------",paymentDetail
# # #             servicerequest = ServiceRequest.objects.filter(is_deleted=False,
# # #                                                            consumer_id_id=consumer.id).count()
# # #             complaintraised = ComplaintDetail.objects.filter(is_deleted=False,
# # #                                                              consumer_id_id=consumer.id).count()
# # #             feedbackscount = Feedback.objects.filter(is_deleted=False, consumer_id_id=consumer.id)
# # #             # print feedbackscount
# # #             for feedback1 in feedbackscount:
# # #
# # #                 feedback = feedback1.feedback
# # #                 if feedback1.stars == 'STAR1':
# # #                     edit1 = 1
# # #                 elif feedback1.stars == 'STAR2':
# # #                     edit1 = 2
# # #                 elif feedback1.stars == 'STAR3':
# # #                     edit1 = 3
# # #                 elif feedback1.stars == 'STAR4':
# # #                     edit1 = 4
# # #                 else:
# # #                     edit1 = 5
# # #             for paymentD in paymentDetail:
# # #                 netamount = paymentD.bill_amount_paid,
# # #                 payment_done = paymentD.payment_done
# # #                 paymentMode = paymentD.payment_mode
# # #             objlist = {
# # #                 'id': consumer.id,
# # #                 'nameid': consumer.name + '-' + consumer.consumer_no + ' ' + "(Primary)",
# # #                 'name': consumer.name,
# # #                 'consumer_type': consumer.connection_status,
# # #                 'dtc': consumer.dtc,
# # #                 'consumer_no': consumer.consumer_no,
# # #                 'pole_no': consumer.pole_no,
# # #                 'email_id': consumer.email_id,
# # #                 'contact_no': consumer.contact_no,
# # #                 'address_line_1': consumer.address_line_1,
# # #                 'meter_no': consumer.meter_no,
# # #                 'netamountpaid': netamount,
# # #                 'paymentStatus': payment_done,
# # #                 'paymentMode':paymentMode,
# # #                 'servicerequest': servicerequest,
# # #                 'complaintraised': complaintraised,
# # #                 'edit1': edit1,
# # #             }
# # #             finallist.append(objlist)
# # #             print "===============>>>>finallist", finallist
# # #         data={'finallist':finallist}
# # #         data = render(request, 'consumer/consumerBody.html', data)
# # #     except Exception, e:
# # #         print 'exception ', str(traceback.print_exc())
# # #         print 'Exception|consumer.py|consumer_card_filter', e
# # #         data = {'Please Select Valid Zone': 'error'}
# # #     return HttpResponse(data)


# def checkMonth(month):
#     if month > 9:
#         return str(month)
#     else:
#         return '0' + str(month)


# def month_minus(yearMonth):
#     try:

#         monthList = []
#         # print 'In month_minus with ', yearMonth
#         year = int(yearMonth[:-2])
#         month = int(yearMonth[-2:])
#         if month == 1:
#             year = year - 1
#             month = 12
#         else:
#             month = month - 6
#         for i in range(1, 7):
#             month = month + 1
#             monthList.append(str(year) + checkMonth(month))
#         return monthList
#         print "*************", monthList
#     except Exception, e:
#         print 'Exception|task.py|fail_downloadPN33', e
#     return None


# def consumer_jobcard_list_view(request):
#     get_consumer_card_list(request)
#     return render(request, 'consumer/consumerListView.html')


# def get_consumer_list_view_detail(request):
#     try:
#         data = {}
#         # get_consumer_card_list(request)
#         data = render(request, 'consumer/consumerBodyList.html', data)
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|consumer.py|consumer_card_filter', e
#         data = {'No list view found': 'error'}
#     return HttpResponse(data)


#shubham
def consumer_list(request):
    try:
        data = {'city_list': get_city(request),
        		'zone_list': get_zone(request),
        		'billcycle_list': get_billcycle(request),
        		'route_list': get_RouteDetail(request),
        		'pincode_list': get_pincode(request)}
    except Exception, e:
        print 'Exception|views.py|consumerapp', e
    return render(request, 'consumer_list.html',data)

def get_city(request):
	city_list = []
	try:
		city_objs = City.objects.filter(is_deleted=False)
		for city in city_objs:
			city_list.append({'city_id': city.id,'city': city.city})
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
            zone_list.append({'zone_id': zone.id,'zone_name': zone.zone_name})
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
            billcycle_list.append({'bill_cycle_id': bill.id,'bill_cycle_code': bill.bill_cycle_code})
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
            route_list.append({'route_id': route.id,'route_code': route.route_code})
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
            pincode_list.append({'pincode_id': pincode.id,'pincode': pincode.pincode})
        data = pincode_list
        return data
    except Exception, ke:
        print ke
        data = {'pincode_list': 'none', 'message': 'No pincode available'}
        return data                                

def get_consumer_list(request):	
	try:
		filter_zone  	= request.GET.get('filter_zone')
		filter_bill  	= request.GET.get('filter_bill')
		filter_route 	= request.GET.get('filter_route')
		filter_category = request.GET.get('filter_category')
		filter_service 	= request.GET.get('filter_service')
		filter_from 	= request.GET.get('filter_from')
		filter_to 		= request.GET.get('filter_to')

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
				consumer_no   	 = consumer_obj.consumer_no
				consumer_no1   	 = '<a href="/consumer-details/?consumer_no='+consumer_no+'">'+consumer_no+'</a>'
				consumer_name 	 = consumer_obj.name
				contact_no    	 = consumer_obj.contact_no
				email_id      	 = consumer_obj.email_id
				servicerequest 	 = ServiceRequest.objects.filter(consumer_id=consumer_no).count()
				complaintrequest = ComplaintDetail.objects.filter(consumer_id=consumer_no).count()
				connection_status= consumer_obj.connection_status
				action 			 = '<a> <i class="fa fa-pencil" aria-hidden="true" onclick="edit_consumer('+consumer_no+')"></i> </a>'  

				consumer_data = {
				'consumer_no'		: consumer_no1,
				'consumer_name'		: consumer_name,
				'contact_no'		: contact_no,
				'email_id'			: email_id,
				'servicerequest'	: servicerequest,
				'complaintrequest'	: complaintrequest,
				'connection_status'	: connection_status,
				'action':action
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
            consumer_obj	= ConsumerDetails.objects.get(consumer_no=request.GET.get('consumer_no'))
            consumer_no   	= consumer_obj.consumer_no
            name   			= consumer_obj.name
            name 			= name +' ('+ consumer_no + ') '  
            utility   		= consumer_obj.Utility.utility
            contact_no   	= consumer_obj.contact_no
            email_id   		= consumer_obj.email_id
            aadhar_no   	= consumer_obj.aadhar_no
            address_line_1  = consumer_obj.address_line_1
            address_line_2  = consumer_obj.address_line_2
            address_line_3  = consumer_obj.address_line_3
            address 		= address_line_1 + ' ' + address_line_2 + ' ' + address_line_3
            city_id   		= str(consumer_obj.city.id)
            pincode_id 		= str(consumer_obj.pin_code.id)
            zone_id 		= str(consumer_obj.zone.id)
            meter_no 		= consumer_obj.meter_no
            meter_category 	= consumer_obj.meter_category
            sanction_load 	= consumer_obj.sanction_load
           
            consumer_data = {
                'name'			: name,
                'consumer_no'	: consumer_no,
                'utility'		: utility,
                'contact_no'	: contact_no,
                'aadhar_no'		: aadhar_no,
                'email_id'		: email_id,
                'address'		: address,
                'city_id'		: city_id,
                'pincode_id'	: pincode_id,
                'zone_id'		: zone_id,
                'meter_no'		: meter_no,
                'meter_category': meter_category,
                'sanction_load'	: sanction_load
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
        print '..................SSS............',request.POST.get('edit_utility')
        #consumer_obj.Utility = request.POST.get('edit_utility')
        # consumer_obj.user_last_name = request.POST.get('edit_contact')
        # consumer_obj.user_contact_no = request.POST.get('edit_email')
        # consumer_obj.user_contact_no = request.POST.get('edit_aadhar')
        # consumer_obj.user_contact_no = request.POST.get('edit_city')
        # consumer_obj.user_contact_no = request.POST.get('edit_pincode')
        # consumer_obj.user_contact_no = request.POST.get('edit_zone')
        # consumer_obj.user_contact_no = request.POST.get('edit_meter_no')
        # consumer_obj.user_contact_no = request.POST.get('edit_category')
        # consumer_obj.user_contact_no = request.POST.get('edit_sanction_load')
        # consumer_obj.Utility = Utility.objects.get(
        #     utility=request.POST.get('edit_utility')) if request.POST.get(
        #     'edit_utility') else None
        #user_obj.user_updated_date = datetime.now()
        #user_obj.user_status = '1'

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