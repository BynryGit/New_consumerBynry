import csv
import json
import pdb
import traceback
import datetime
from string import strip

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from paymentapp.models import PaymentDetail
from BynryConsumerModuleapp.models import Zone,BillCycle,RouteDetail
from django.views.decorators.csrf import csrf_exempt

# Todo show list view for payment detail
# @login_required(login_url='/')
# def open_payment_list(request):
#     try:
#         totalPayment = PaymentDetail.objects.filter(is_deleted=False).count()
#         data = {'total': totalPayment}
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|open_payment_list', e
#         data = {'message': 'Server Error'}
#     return render(request, 'paymentapp/payment.html',data)

# 'Online Payment', 'Online Payment'),
#         ('Paytm Wallet', 'Paytm Wallet'),
#         ('Cash Payment', 'Cash Payment'),

def payments(request):
    data={}
    zone = Zone.objects.all()
    billcycle = BillCycle.objects.all()
    routeDetail = RouteDetail.objects.all()

    data={'zone':zone,'billcycle':billcycle,'routeDetail':routeDetail}
    print '--------data----',data
    return render(request, 'payments.html',data)


def online_payments(request):
    try:
        online_payment_list=[]
        #online_data={}
        #data={}

        print "in payments--1---------------"
        payment_details = PaymentDetail.objects.all()
        print '------------payments---1---',payment_details
        for i in payment_details:
            payment_mode = i.payment_mode
            print '-------payment_mode--1----',payment_mode
            if payment_mode == 'Online Payment':
                print '----Online1----'
                payment_date = i.payment_date.strftime("%d/%m/%Y")
                print '--------payment_date-1',payment_date
                transaction_id = i.transaction_id
                bill_amount_paid = i.bill_amount_paid
                consumer_id = i.consumer_id
                consumer_name = consumer_id.name
                payment_mode = 'Online Payment'

                online_data ={'payment_date':str(payment_date),'bill_amount_paid':str(bill_amount_paid),
                              'transaction_id':str(transaction_id),'consumer_id':str(consumer_id),
                              'consumer_name':str(consumer_name),'payment_mode':str(payment_mode)}

                online_payment_list.append(online_data)

        print '------online_payment_list--1----',online_payment_list
        data = {'data':online_payment_list}
    except Exception, e:
        print e
    print 'data--------',data
    return HttpResponse(json.dumps(data), content_type='application/json')


def paytm_payments(request):
    try:
        payment_wallet_list=[]
        #paytm_data={}
        #data={}
        print "in payments-----2------------"
        payment_details = PaymentDetail.objects.all()
        print '------------payments--2----',payment_details
        for i in payment_details:
            payment_mode = i.payment_mode
            print '-------payment_mode--2----',payment_mode
            if payment_mode == 'Paytm Wallet':
                print '----Paytm-2---'
                payment_date = i.payment_date.strftime("%d/%m/%Y")
                print '--------payment_date2-',payment_date
                transaction_id = i.transaction_id
                bill_amount_paid = i.bill_amount_paid
                consumer_id = i.consumer_id
                consumer_name = consumer_id.name
                payment_mode = 'Paytm Payment'

                paytm_data ={'payment_date':str(payment_date),'bill_amount_paid':str(bill_amount_paid),
                              'transaction_id':str(transaction_id),'consumer_id':str(consumer_id),
                              'consumer_name':str(consumer_name),'payment_mode':str(payment_mode)}
                payment_wallet_list.append(paytm_data)
        data = {'data':payment_wallet_list}
    except Exception, e:
        print e
    return HttpResponse(json.dumps(data), content_type='application/json')

def cash_payments(request):
    try:
        cash_payment_list=[]
        #data={}
        #cash_data={}
        print "in payments--------3---------"
        payment_details = PaymentDetail.objects.all()
        print '------------payments--3----',payment_details
        for i in payment_details:
            payment_mode = i.payment_mode
            print '-------payment_mode--3----',payment_mode
            if payment_mode == 'Cash Payment':
                print '----Paytm--3--'
                payment_date = i.payment_date.strftime("%d/%m/%Y")
                print '--------payment_date3-',payment_date
                transaction_id = i.transaction_id
                bill_amount_paid = i.bill_amount_paid
                consumer_id = i.consumer_id
                consumer_name = consumer_id.name
                payment_mode = 'Cash Payment'

                cash_data ={'payment_date':str(payment_date),'bill_amount_paid':str(bill_amount_paid),
                              'transaction_id':str(transaction_id),'consumer_id':str(consumer_id),
                              'consumer_name':str(consumer_name),'payment_mode':str(payment_mode)}
                cash_payment_list.append(cash_data)
        data = {'data':cash_payment_list}
    except Exception, e:
        print e
    return HttpResponse(json.dumps(data), content_type='application/json')

def payments_get_consumer_details(request):
    consumer_no = request.GET.get('consumer_no')
    bill_month = request.GET.get('bill_month')
    print '------consumer_no-----',consumer_no
    print '------bill_month-----',bill_month

    consumer_obj = PaymentDetail.objects.filter(consumer_id=consumer_no,bill_month=bill_month)

    consumption = consumer_obj.consumption
    current_month_reading = consumer_obj.current_month_reading
    previous_month_reading = consumer_obj.previous_month_reading
    current_amount = consumer_obj.current_amount
    tariff_rate = consumer_obj.tariff_rate
    net_amount = consumer_obj.net_amount
    bill_amount_paid = consumer_obj.bill_amount_paid
    amount_after_due_date = consumer_obj.amount_after_due_date
    arriers = consumer_obj.arriers
    payment_date = consumer_obj.payment_date.strftime("%d/%m/%Y")
    due_date = consumer_obj.due_date.strftime("%d/%m/%Y")

    data={'consumer_no':consumer_no,'bill_month':bill_month,'consumption':consumption,
          'current_month_reading':current_month_reading,'previous_month_reading':previous_month_reading,
          'current_amount':current_amount,'tariff_rate':tariff_rate,'net_amount':net_amount,
          'bill_amount_paid':bill_amount_paid,'amount_after_due_date':amount_after_due_date,
          'arriers':arriers,'payment_date':payment_date,'due_date':due_date
          }
    print '--------data----',data
    return HttpResponse(json.dumps(data), content_type='application/json')

def payments_save_payment_details(request):
    consumer_no = request.GET.get('consumer_no')
    bill_month = request.GET.get('bill_month')

    payment_mode = request.GET.get('payment_mode')
    bill_amount_paid = request.GET.get('amount')
    payment_date = request.GET.get('payment_date')

    consumer_obj = PaymentDetail.objects.filter(consumer_id=consumer_no,bill_month=bill_month)

    consumer_obj.payment_mode = payment_mode
    consumer_obj.bill_amount_paid = bill_amount_paid
    consumer_obj.payment_date = payment_date
    consumer_obj.save()

    data={'success':True}
    print '--------data----',data
    return HttpResponse(json.dumps(data), content_type='application/json')

# @login_required(login_url='/')
# def list_payment_deatail(request):
#     try:
#         userRoleList = []
#         column = request.GET.get('order[0][column]')
#         searchTxt = request.GET.get('search[value]')
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['payment_date']
#         column_name = order + list[int(column)]
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))
#
#         consumerBy = request.GET.get('filter')
#         print "consumerBy-----------------",consumerBy
#         startDate = request.GET.get('startDate')
#         endDate = request.GET.get('endDate')
#         payments=''
#         total_record=''
#         try:
#             if consumerBy == 'all':
#                 print "here -----------consumerBy------all------------"
#                 try:
#                     if startDate == "None" and endDate == "None":
#                         print "\nNo Dates"
#                         total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                is_deleted=False).count()
#                         payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                             is_deleted=False).order_by(column_name)[start:length]
#                     else:
#                         if startDate and (endDate == "None" or endDate == '' or endDate == None):
#                             checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                    payment_date__gte=checkStart, is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                 payment_date__gte=checkStart,
#                                                                 is_deleted=False).order_by(column_name)[start:length]
#                             print "\nhereeeeeee from date only "
#
#                         elif endDate and (startDate == "None" or startDate == '' or startDate == None):
#                             checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#                             print "\nhereeeeeee  To Date Only"
#
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                    payment_date__lte=checkEnd, is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                 payment_date__lte=checkEnd,
#                                                                 is_deleted=False).order_by(column_name)[start:length]
#
#                         elif startDate and endDate:
#                             checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                             checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#
#                             print "\nhereeeeeee Both the dates "
#
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt),
#                                                                    payment_date__gte=checkStart,payment_date__lte=checkEnd, is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                 payment_date__gte=checkStart,payment_date__lte=checkEnd,
#                                                                 is_deleted=False).order_by(column_name)[start:length]
#                         else:
#                             total_record = PaymentDetail.objects.filter(
#                                 Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                 is_deleted=False).order_by(column_name)[start:length]
#
#                 except Exception, e:
#                     print e
#
#             else:
#                 if startDate == '' and endDate == '':
#                     print "No Dates--------------------"
#                     if consumerBy == 'Registered':
#                         total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=True,is_deleted=False).count()
#                         payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                 consumer_id__parent__isnull=True,is_deleted=False).order_by(column_name)[start:length]
#                     elif consumerBy == 'Unregistered':
#                         total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=False, is_deleted=False).count()
#                         payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                 consumer_id__parent__isnull=False, is_deleted=False).order_by(
#                             column_name)[start:length]
#                 else:
#                     if startDate and (endDate == "None" or endDate == '' or endDate == None):
#                         checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                         print "\nhereeeeeee from date only "
#                         if consumerBy == 'Registered':
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                         consumer_id__parent__isnull=True,payment_date__gte=checkStart, is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=True,payment_date__gte=checkStart, is_deleted=False).order_by(column_name)[start:length]
#                         elif consumerBy == 'Unregistered':
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                         consumer_id__parent__isnull=False,
#                                                                         payment_date__gte=checkStart,
#                                                                         is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=False,
#                                                                     payment_date__gte=checkStart,
#                                                                     is_deleted=False).order_by(column_name)[start:length]
#
#                     elif endDate and (startDate == "None" or startDate == '' or startDate == None):
#                         checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#
#                         print "\nhereeeeeee To date only "
#                         if consumerBy == 'Registered':
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                         consumer_id__parent__isnull=True, payment_date__lte=checkEnd,
#                                                                    is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=True, payment_date__lte=checkEnd,
#                                                                 is_deleted=False).order_by(column_name)[start:length]
#                         elif consumerBy == 'Unregistered':
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                         consumer_id__parent__isnull=False,
#                                                                         payment_date__lte=checkEnd,
#                                                                         is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=False,
#                                                                     payment_date__lte=checkEnd,
#                                                                     is_deleted=False).order_by(column_name)[start:length]
#
#                     elif startDate and endDate:
#                         checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                         checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#
#                         print "\nhereeeeeee Both dates "
#                         if consumerBy == 'Registered':
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                         consumer_id__parent__isnull=True,payment_date__gte=checkStart,payment_date__lte=checkEnd,
#                                                                    is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=True,payment_date__gte=checkStart,payment_date__lte=checkEnd,
#                                                                 is_deleted=False).order_by(column_name)[start:length]
#                         elif consumerBy == 'Unregistered':
#                             total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                         consumer_id__parent__isnull=False,
#                                                                         payment_date__gte=checkStart,
#                                                                         payment_date__lte=checkEnd,
#                                                                         is_deleted=False).count()
#                             payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
#                                                                     consumer_id__parent__isnull=False,
#                                                                     payment_date__gte=checkStart,
#                                                                     payment_date__lte=checkEnd,
#                                                                     is_deleted=False).order_by(column_name)[start:length]
#
#         except Exception, e:
#             print e
#
#         for payment in payments:
#             tempList = []
#             if payment.payment_date:
#                 payment_date = payment.payment_date.strftime('%b %d, %Y')
#             else:
#                 payment_date = ('-----')
#
#             # name = '<a onclick="viewDetails(' + str(payment.id) + ')" >' + str(payment.consumer_id.name) + '</a>'
#
#             tempList.append(payment_date)
#             tempList.append(str(payment.bill_amount_paid))
#             tempList.append(payment.transaction_id)
#             tempList.append(payment.consumer_id.name)
#             tempList.append(payment.consumer_id.consumer_no)
#             tempList.append('Mobile App')
#
#             userRoleList.append(tempList)
#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userRoleList}
#
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|list_custom_notification', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')
#
#
# @login_required(login_url='/')
# def export_to_excel(request):
#     try:
#         consumerBy = request.GET.get('filterby')
#         startDate = request.GET.get('startDate')
#         endDate = request.GET.get('endDate')
#         try:
#             if consumerBy == 'all':
#                 print "here -----------consumerBy------all------------"
#                 try:
#                     if startDate == "None" and endDate == "None":
#                         print "\nNo Dates"
#                         payments = PaymentDetail.objects.filter(is_deleted=False)
#                     else:
#                         if startDate and (endDate == "None" or endDate == '' or endDate == None):
#                             checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                             payments = PaymentDetail.objects.filter(payment_date__gte=checkStart,
#                                                                     is_deleted=False)
#                             print "\nhereeeeeee from date only "
#
#                         elif endDate and (startDate == "None" or startDate == '' or startDate == None):
#                             checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#                             print "\nhereeeeeee  To Date Only"
#                             payments = PaymentDetail.objects.filter(payment_date__lte=checkEnd,
#                                                                     is_deleted=False)
#                         elif startDate and endDate:
#                             checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                             checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#
#                             print "\nhereeeeeee Both the dates "
#                             payments = PaymentDetail.objects.filter(payment_date__gte=checkStart,payment_date__lte=checkEnd,
#                                                                     is_deleted=False)
#                         else:
#                             payments = PaymentDetail.objects.filter(is_deleted=False)
#                 except Exception, e:
#                     print e
#
#             else:
#                 if startDate == '' and endDate == '':
#                     print "No Dates--------------------"
#                     if consumerBy == 'Registered':
#                         payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, is_deleted=False)
#                     elif consumerBy == 'Unregistered':
#                         payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, is_deleted=False)
#                 else:
#                     if startDate and (endDate == "None" or endDate == '' or endDate == None):
#                         checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                         print "\nhereeeeeee from date only "
#                         if consumerBy == 'Registered':
#                             payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, payment_date__gte=checkStart,
#                                                                 is_deleted=False)
#                         elif consumerBy == 'Unregistered':
#                             payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, payment_date__gte=checkStart,
#                                                                                         is_deleted=False)
#
#                     elif endDate and (startDate == "None" or startDate == '' or startDate == None):
#                         checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#                         print "\nhereeeeeee To date only "
#                         if consumerBy == 'Registered':
#                             payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, payment_date__lte=checkEnd,
#                                                                 is_deleted=False)
#                         elif consumerBy == 'Unregistered':
#                             payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, payment_date__lte=checkEnd,
#                                                                     is_deleted=False)
#                     elif startDate and endDate:
#                         checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
#                         checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
#                         print "\nhereeeeeee Both dates "
#                         if consumerBy == 'Registered':
#                             payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, payment_date__gte=checkStart,
#                                                                 payment_date__lte=checkEnd,is_deleted=False)
#                         elif consumerBy == 'Unregistered':
#                             payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, payment_date__gte=checkStart,
#                                                                    payment_date__lte=checkEnd, is_deleted=False)
#
#         except Exception, e:
#             print e
#
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="Payment_Export_To_Excel.csv"';
#         writer = csv.writer(response)
#         writer.writerow(
#             ['PYAMENT_DATE', 'PAYMENT_AMOUNT', 'TRASACTION_ID', 'NAME', 'CONSUMER_NUMBER', 'PAYMENT_MODE'])
#
#         for payment in payments:
#             tempList = []
#             if payment.payment_date:
#                 payment_date = payment.payment_date.strftime('%b %d, %Y')
#             else:
#                 payment_date = ('-----')
#
#             tempList.append(payment_date)
#             tempList.append(str(payment.bill_amount_paid))
#             tempList.append(payment.transaction_id)
#             tempList.append(payment.consumer_id.name)
#             tempList.append(payment.consumer_id.consumer_no)
#             tempList.append('Mobile App')
#
#             writer.writerow(tempList)
#             print "tempList------------------------", tempList
#         return response
#     except Exception, e:
#         print 'exception ', str(traceback.print_exc())
#         print 'Exception|views.py|export_to_excel', e
#         data = {'msg': 'error'}
#     return HttpResponse(json.dumps(data), content_type='application/json')
