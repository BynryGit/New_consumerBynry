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
from consumerapp.models import ConsumerDetails,PaymentDetail
from django.views.decorators.csrf import csrf_exempt

# Todo show list view for payment detail
@login_required(login_url='/')
def open_payment_list(request):
    try:
        totalPayment = PaymentDetail.objects.filter(is_deleted=False).count()
        data = {'total': totalPayment}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|open_payment_list', e
        data = {'message': 'Server Error'}
    return render(request, 'paymentapp/payment.html',data)


@login_required(login_url='/')
def list_payment_deatail(request):
    try:
        userRoleList = []
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['payment_date']
        column_name = order + list[int(column)]
        start = request.GET.get('start')
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        consumerBy = request.GET.get('filter')
        print "consumerBy-----------------",consumerBy
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        payments=''
        total_record=''
        try:
            if consumerBy == 'all':
                print "here -----------consumerBy------all------------"
                try:
                    if startDate == "None" and endDate == "None":
                        print "\nNo Dates"
                        total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                               is_deleted=False).count()
                        payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                            is_deleted=False).order_by(column_name)[start:length]
                    else:
                        if startDate and (endDate == "None" or endDate == '' or endDate == None):
                            checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                   payment_date__gte=checkStart, is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                payment_date__gte=checkStart,
                                                                is_deleted=False).order_by(column_name)[start:length]
                            print "\nhereeeeeee from date only "

                        elif endDate and (startDate == "None" or startDate == '' or startDate == None):
                            checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
                            print "\nhereeeeeee  To Date Only"

                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                   payment_date__lte=checkEnd, is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                payment_date__lte=checkEnd,
                                                                is_deleted=False).order_by(column_name)[start:length]

                        elif startDate and endDate:
                            checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                            checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')

                            print "\nhereeeeeee Both the dates "

                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt),
                                                                   payment_date__gte=checkStart,payment_date__lte=checkEnd, is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                payment_date__gte=checkStart,payment_date__lte=checkEnd,
                                                                is_deleted=False).order_by(column_name)[start:length]
                        else:
                            total_record = PaymentDetail.objects.filter(
                                Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                is_deleted=False).order_by(column_name)[start:length]

                except Exception, e:
                    print e

            else:
                if startDate == '' and endDate == '':
                    print "No Dates--------------------"
                    if consumerBy == 'Registered':
                        total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=True,is_deleted=False).count()
                        payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                consumer_id__parent__isnull=True,is_deleted=False).order_by(column_name)[start:length]
                    elif consumerBy == 'Unregistered':
                        total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=False, is_deleted=False).count()
                        payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                consumer_id__parent__isnull=False, is_deleted=False).order_by(
                            column_name)[start:length]
                else:
                    if startDate and (endDate == "None" or endDate == '' or endDate == None):
                        checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                        print "\nhereeeeeee from date only "
                        if consumerBy == 'Registered':
                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                        consumer_id__parent__isnull=True,payment_date__gte=checkStart, is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=True,payment_date__gte=checkStart, is_deleted=False).order_by(column_name)[start:length]
                        elif consumerBy == 'Unregistered':
                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                        consumer_id__parent__isnull=False,
                                                                        payment_date__gte=checkStart,
                                                                        is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=False,
                                                                    payment_date__gte=checkStart,
                                                                    is_deleted=False).order_by(column_name)[start:length]

                    elif endDate and (startDate == "None" or startDate == '' or startDate == None):
                        checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')

                        print "\nhereeeeeee To date only "
                        if consumerBy == 'Registered':
                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                        consumer_id__parent__isnull=True, payment_date__lte=checkEnd,
                                                                   is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=True, payment_date__lte=checkEnd,
                                                                is_deleted=False).order_by(column_name)[start:length]
                        elif consumerBy == 'Unregistered':
                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                        consumer_id__parent__isnull=False,
                                                                        payment_date__lte=checkEnd,
                                                                        is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=False,
                                                                    payment_date__lte=checkEnd,
                                                                    is_deleted=False).order_by(column_name)[start:length]

                    elif startDate and endDate:
                        checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                        checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')

                        print "\nhereeeeeee Both dates "
                        if consumerBy == 'Registered':
                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                        consumer_id__parent__isnull=True,payment_date__gte=checkStart,payment_date__lte=checkEnd,
                                                                   is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=True,payment_date__gte=checkStart,payment_date__lte=checkEnd,
                                                                is_deleted=False).order_by(column_name)[start:length]
                        elif consumerBy == 'Unregistered':
                            total_record = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                        consumer_id__parent__isnull=False,
                                                                        payment_date__gte=checkStart,
                                                                        payment_date__lte=checkEnd,
                                                                        is_deleted=False).count()
                            payments = PaymentDetail.objects.filter(Q(transaction_id__icontains=searchTxt)|Q(consumer_id__name__icontains=searchTxt),
                                                                    consumer_id__parent__isnull=False,
                                                                    payment_date__gte=checkStart,
                                                                    payment_date__lte=checkEnd,
                                                                    is_deleted=False).order_by(column_name)[start:length]

        except Exception, e:
            print e

        for payment in payments:
            tempList = []
            if payment.payment_date:
                payment_date = payment.payment_date.strftime('%b %d, %Y')
            else:
                payment_date = ('-----')

            # name = '<a onclick="viewDetails(' + str(payment.id) + ')" >' + str(payment.consumer_id.name) + '</a>'

            tempList.append(payment_date)
            tempList.append(str(payment.bill_amount_paid))
            tempList.append(payment.transaction_id)
            tempList.append(payment.consumer_id.name)
            tempList.append(payment.consumer_id.consumer_no)
            tempList.append('Mobile App')

            userRoleList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': userRoleList}

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|list_custom_notification', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/')
def export_to_excel(request):
    try:
        consumerBy = request.GET.get('filterby')
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        try:
            if consumerBy == 'all':
                print "here -----------consumerBy------all------------"
                try:
                    if startDate == "None" and endDate == "None":
                        print "\nNo Dates"
                        payments = PaymentDetail.objects.filter(is_deleted=False)
                    else:
                        if startDate and (endDate == "None" or endDate == '' or endDate == None):
                            checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                            payments = PaymentDetail.objects.filter(payment_date__gte=checkStart,
                                                                    is_deleted=False)
                            print "\nhereeeeeee from date only "

                        elif endDate and (startDate == "None" or startDate == '' or startDate == None):
                            checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
                            print "\nhereeeeeee  To Date Only"
                            payments = PaymentDetail.objects.filter(payment_date__lte=checkEnd,
                                                                    is_deleted=False)
                        elif startDate and endDate:
                            checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                            checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')

                            print "\nhereeeeeee Both the dates "
                            payments = PaymentDetail.objects.filter(payment_date__gte=checkStart,payment_date__lte=checkEnd,
                                                                    is_deleted=False)
                        else:
                            payments = PaymentDetail.objects.filter(is_deleted=False)
                except Exception, e:
                    print e

            else:
                if startDate == '' and endDate == '':
                    print "No Dates--------------------"
                    if consumerBy == 'Registered':
                        payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, is_deleted=False)
                    elif consumerBy == 'Unregistered':
                        payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, is_deleted=False)
                else:
                    if startDate and (endDate == "None" or endDate == '' or endDate == None):
                        checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                        print "\nhereeeeeee from date only "
                        if consumerBy == 'Registered':
                            payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, payment_date__gte=checkStart,
                                                                is_deleted=False)
                        elif consumerBy == 'Unregistered':
                            payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, payment_date__gte=checkStart,
                                                                                        is_deleted=False)

                    elif endDate and (startDate == "None" or startDate == '' or startDate == None):
                        checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
                        print "\nhereeeeeee To date only "
                        if consumerBy == 'Registered':
                            payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, payment_date__lte=checkEnd,
                                                                is_deleted=False)
                        elif consumerBy == 'Unregistered':
                            payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, payment_date__lte=checkEnd,
                                                                    is_deleted=False)
                    elif startDate and endDate:
                        checkStart = datetime.datetime.strptime(startDate, '%d/%m/%Y')
                        checkEnd = datetime.datetime.strptime(endDate, '%d/%m/%Y')
                        print "\nhereeeeeee Both dates "
                        if consumerBy == 'Registered':
                            payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=True, payment_date__gte=checkStart,
                                                                payment_date__lte=checkEnd,is_deleted=False)
                        elif consumerBy == 'Unregistered':
                            payments = PaymentDetail.objects.filter(consumer_id__parent__isnull=False, payment_date__gte=checkStart,
                                                                   payment_date__lte=checkEnd, is_deleted=False)

        except Exception, e:
            print e

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Payment_Export_To_Excel.csv"';
        writer = csv.writer(response)
        writer.writerow(
            ['PYAMENT_DATE', 'PAYMENT_AMOUNT', 'TRASACTION_ID', 'NAME', 'CONSUMER_NUMBER', 'PAYMENT_MODE'])

        for payment in payments:
            tempList = []
            if payment.payment_date:
                payment_date = payment.payment_date.strftime('%b %d, %Y')
            else:
                payment_date = ('-----')

            tempList.append(payment_date)
            tempList.append(str(payment.bill_amount_paid))
            tempList.append(payment.transaction_id)
            tempList.append(payment.consumer_id.name)
            tempList.append(payment.consumer_id.consumer_no)
            tempList.append('Mobile App')

            writer.writerow(tempList)
            print "tempList------------------------", tempList
        return response
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|export_to_excel', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
