# __author__='Swapnil Kadu'
import json
import traceback
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from paymentapp.models import PaymentDetail
from BynryConsumerModuleapp.models import Zone, BillCycle, RouteDetail, Branch
from consumerapp.models import ConsumerDetails, MeterReadingDetail
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import string
import random

# To view payment page
def payments(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        print 'paymentapp|views.py|payments'
        if request.session['branch_id']:
            branch_obj = Branch.objects.get(id=request.session['branch_id'])
            zones = Zone.objects.filter(is_deleted=False, branch=branch_obj)
        else:
            zones = ''
        data = {'branch_list': Branch.objects.filter(is_deleted=False),  # Branch List
                'zones': zones
                }
        return render(request, 'payments.html', data)


# To get online payments list
def online_payments(request):
    online_payment_list = []
    payment_details_list = []
    try:
        print 'paymentapp|views.py|online_payments'
        filter_branch = request.GET.get('filter_branch')
        filter_zone = request.GET.get('filter_zone')
        filter_bill = request.GET.get('filter_bill')
        filter_route = request.GET.get('filter_route')
        filter_from = request.GET.get('filter_from')
        filter_to = request.GET.get('filter_to')

        try:
            payment_details_list = PaymentDetail.objects.filter(payment_mode= 'Online Payment')
            # filter payment data by barnch
            if filter_branch != 'all':
                consumer_obj = ConsumerDetails.objects.filter(branch__id=str(filter_branch))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by zone
            if filter_zone != 'all':
                consumer_obj = ConsumerDetails.objects.filter(zone__id=str(filter_zone))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by bill cycle
            if filter_bill != 'all':
                consumer_obj = ConsumerDetails.objects.filter(bill_cycle__id=str(filter_bill))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by route
            if filter_route != 'all':
                consumer_obj = ConsumerDetails.objects.filter(route__id=str(filter_route))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by date range
            if filter_from != '' and filter_to != '':
                filter_from = datetime.strptime(filter_from, "%d/%m/%Y")
                filter_from = filter_from.strftime("%Y-%m-%d")
                filter_to = datetime.strptime(filter_to, "%d/%m/%Y")
                filter_to = filter_to.strftime("%Y-%m-%d")
                payment_details_list = payment_details_list.filter(created_on__range=[filter_from, filter_to])

            # get online payment data list by payment obj
            for i in payment_details_list:
                online_data = {
                    'payment_date': str(i.created_on.strftime('%B %d, %Y %I:%M %p')),
                    'bill_amount_paid': str(i.bill_amount_paid),
                    'transaction_id': str(i.transaction_id),
                    'consumer_id': '<a onclick="consumer_details_modal(' + str(
                       i.consumer_id) + ');">' + str(i.consumer_id) + '</a>',
                    'consumer_name': str(i.consumer_id.name),
                    'payment_mode': str('Online Payment')
                }
                online_payment_list.append(online_data)
            data = {'data': online_payment_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|paymentapp|views.py|online_payments', e
            print 'Exception', e
            data = {'success': 'false', 'error': 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')


# To get paytm payments list
def paytm_payments(request):
    try:
        print 'paymentapp|views.py|paytm_payments'
        payment_wallet_list = []
        payment_details_list = []

        filter_branch = request.GET.get('filter_branch')
        filter_zone = request.GET.get('filter_zone')
        filter_bill = request.GET.get('filter_bill')
        filter_route = request.GET.get('filter_route')
        filter_from = request.GET.get('filter_from')
        filter_to = request.GET.get('filter_to')
        try:
            payment_details_list = PaymentDetail.objects.filter(payment_mode= 'Paytm Wallet')
            # filter payment data by barnch
            if filter_branch != 'all':
                consumer_obj = ConsumerDetails.objects.filter(branch__id=str(filter_branch))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by zone
            if filter_zone != 'all':
                consumer_obj = ConsumerDetails.objects.filter(zone__id=str(filter_zone))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by bill cycle
            if filter_bill != 'all':
                consumer_obj = ConsumerDetails.objects.filter(bill_cycle__id=str(filter_bill))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by route
            if filter_route != 'all':
                consumer_obj = ConsumerDetails.objects.filter(route__id=str(filter_route))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by date range
            if filter_from != '' and filter_to != '':
                filter_from = datetime.strptime(filter_from, "%d/%m/%Y")
                filter_from = filter_from.strftime("%Y-%m-%d")
                filter_to = datetime.strptime(filter_to, "%d/%m/%Y")
                filter_to = filter_to.strftime("%Y-%m-%d")
                payment_details_list = payment_details_list.filter(created_on__range=[filter_from, filter_to])

            # get paytm payment data list by payment obj
            for i in payment_details_list:
                paytm_data = {
                    'payment_date': str(i.created_on.strftime('%B %d, %Y %I:%M %p')),
                    'bill_amount_paid': str(i.bill_amount_paid),
                    'transaction_id': str(i.transaction_id),
                    'consumer_id': '<a onclick="consumer_details_modal(' + str(
                        i.consumer_id) + ');">' + str(i.consumer_id) + '</a>',
                    'consumer_name': str(i.consumer_id.name),
                    'payment_mode': str('Paytm Wallet')
                }
                payment_wallet_list.append(paytm_data)
            data = {'data': payment_wallet_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|paytm_payments', e
            print 'Exception', e
            data = {'success': 'false', 'error': 'Exception ' + str(e)}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|paytm_payments', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# To get cash payments list
def cash_payments(request):
    try:
        print 'paymentapp|views.py|cash_payments'
        cash_payment_list = []
        payment_details_list = []
        filter_branch = request.GET.get('filter_branch')
        filter_zone = request.GET.get('filter_zone')
        filter_bill = request.GET.get('filter_bill')
        filter_route = request.GET.get('filter_route')
        filter_from = request.GET.get('filter_from')
        filter_to = request.GET.get('filter_to')

        try:
            payment_details_list = PaymentDetail.objects.filter(payment_mode= 'Cash Payment')
            # filter payment data by barnch
            if filter_branch != 'all':
                consumer_obj = ConsumerDetails.objects.filter(branch__id=str(filter_branch))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by zone
            if filter_zone != 'all':
                consumer_obj = ConsumerDetails.objects.filter(zone__id=str(filter_zone))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by bill cycle
            if filter_bill != 'all':
                consumer_obj = ConsumerDetails.objects.filter(bill_cycle__id=str(filter_bill))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by route
            if filter_route != 'all':
                consumer_obj = ConsumerDetails.objects.filter(route__id=str(filter_route))
                payment_details_list = payment_details_list.filter(consumer_id__in=consumer_obj)
            # filter payment data by date range
            if filter_from != '' and filter_to != '':
                filter_from = datetime.strptime(filter_from, "%d/%m/%Y")
                filter_from = filter_from.strftime("%Y-%m-%d")
                filter_to = datetime.strptime(filter_to, "%d/%m/%Y")
                filter_to = filter_to.strftime("%Y-%m-%d")
                payment_details_list = payment_details_list.filter(created_on__range=[filter_from, filter_to])

            # get cash payment data list by payment obj
            for i in payment_details_list:
                cash_data = {
                    'payment_date': str(i.created_on.strftime('%B %d, %Y %I:%M %p')),
                    'bill_amount_paid': str(i.bill_amount_paid),
                    'transaction_id': str(i.transaction_id),
                    'consumer_id': '<a onclick="consumer_details_modal(' + str(
                     i.consumer_id) + ');">' + str(i.consumer_id) + '</a>',
                    'consumer_name': str(i.consumer_id.name),
                    'payment_mode': str('Cash Payment')
                }
                cash_payment_list.append(cash_data)
            data = {'data': cash_payment_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|cash_payments', e
            print 'Exception', e
            data = {'success': 'false', 'error': 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# To get consumer details
def payments_get_consumer_details(request):
    try:
        print 'paymentapp|views.py|payments_get_consumer_details'
        # filter consumer details by consumer id
        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.GET.get('consumer_id'))
        consumer_data = {
            'billCycle': consumer_obj.bill_cycle.bill_cycle_code,
            'consumerCity': consumer_obj.city.city,
            'consumerRoute': consumer_obj.route.route_code,
            'consumerZone': consumer_obj.bill_cycle.zone.zone_name,
            'consumerNo': consumer_obj.consumer_no,
            'consumerName': consumer_obj.name,
            'consumerAddress': consumer_obj.address_line_1 + '  ' + consumer_obj.address_line_2 + '-' + consumer_obj.pin_code.pincode
        }
        data = {'success': 'true', 'consumerData': consumer_data}

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|payments_get_consumer_details', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# To get payment details
def payments_get_payment_details(request):
    print request
    consumer_no = request.GET.get('consumer_no')
    bill_month = request.GET.get('bill_month')
    try:
        print 'paymentapp|views.py|payments_get_payment_details'
        # filter meter reading details by consumer id and bill month
        consumer_obj = ConsumerDetails.objects.get(consumer_no = request.GET.get('consumer_no'))
        meter_obj = MeterReadingDetail.objects.get(consumer_id=consumer_obj, bill_month=bill_month, bill_status = 'Unpaid')
        if meter_obj.bill_unit and meter_obj.adjusted_unit:
            total_reading = int(meter_obj.bill_unit) - int(meter_obj.adjusted_unit)
        else:
            total_reading = meter_obj.bill_unit

        total_charges = meter_obj.fixed_charges + meter_obj.energy_charges + meter_obj.electricity_duty + meter_obj.wheeling_charges + meter_obj.fuel_adjustment_charges + meter_obj.additional_supply_charges + meter_obj.tax_on_sale - meter_obj.previous_bill_credit + meter_obj.current_interest + meter_obj.capacitor_penalty + meter_obj.other_charges
        total_arrears = meter_obj.net_arrears + meter_obj.adjustments_arrears + meter_obj.interest_arrears
        net_bill_amount = total_charges + total_arrears

        consumer_address = str(consumer_obj.address_line_1)
        if consumer_obj.address_line_2:
            consumer_address = consumer_address + ', ' + str(consumer_obj.address_line_2)

        payment_data = {
            'consumer_no': consumer_obj.consumer_no,
            'meter_no': consumer_obj.meter_no,
            'bill_month': str(meter_obj.bill_month),
            'consumption': str(total_reading),
            'current_month_reading': str(meter_obj.current_month_reading),
            'previous_month_reading': str(meter_obj.previous_month_reading),
            'current_reading_date': meter_obj.current_reading_date.strftime('%d %b %Y'),
            'prompt_date': meter_obj.prompt_date.strftime('%d %b %Y'),
            'current_amount': str(total_charges),
            'tariff_rate': str(meter_obj.tariff),
            'net_amount': str(net_bill_amount),
            'arrears': str(total_arrears),
            'bill_amount_after_due_date': str(meter_obj.bill_amount_after_due_date),
            'prompt_amount': str(meter_obj.prompt_amount),
            'due_date': meter_obj.due_date.strftime('%d %b %Y'),
        }
        data = {'success': 'true', 'payment_data': payment_data}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|payments_get_payment_details', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# To save payment details
def payments_save_payment_details(request):
    try:
        print request
        print 'paymentapp|views.py|payments_save_payment_details'
        # filter meter reading details by consumer id and bill month
        consumer_obj = ConsumerDetails.objects.get(consumer_no=request.GET.get('consumer_no'))
        meter_reading_obj = MeterReadingDetail.objects.get(consumer_id=consumer_obj, bill_month=request.GET.get('bill_month'))

        chars = string.digits
        Size = 5
        regstrtn_no = ''.join(random.choice(chars) for _ in range(Size))

        payment_obj = PaymentDetail(
            consumer_id=consumer_obj,
            meter_reading_id=meter_reading_obj,
            bill_amount_paid=request.GET.get('paid_amount'),
            payment_mode='Cash Payment',
            transaction_id='TRANC'+regstrtn_no,
        )
        payment_obj.save()

        meter_reading_obj.bill_status = 'Paid'
        meter_reading_obj.save()
        data = {'success': 'True'}

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|payments_save_payment_details', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_bills_details(request):
    try:
        data = {}
        final_list = []
        try:
            consumer_id = request.POST.get('consumer_id')
            monthList = request.POST.get('monthList')
            month = monthList.split('-')

            try:
                reading_obj = MeterReadingDetail.objects.get(consumer_id=consumer_id, bill_month=str(month[0]),
                                                             bill_months_year=str(month[1]))
                payment_obj = PaymentDetail.objects.filter(meter_reading_id=reading_obj.id).first()

                transaction_id = payment_obj.transaction_id
                bill_amount_paid = str(payment_obj.bill_amount_paid)
                payment_date = str(payment_obj.payment_date.strftime("%d/%m/%Y"))
                payment_mode = payment_obj.payment_mode

                payment_data = {
                    'transaction_id': transaction_id,
                    'bill_amount_paid': bill_amount_paid,
                    'payment_date': payment_date,
                    'payment_mode': payment_mode
                }
            except Exception, e:
                print '....................Exception', e
                payment_data = {}

            data = {'success': 'true', 'data': payment_data}
        except Exception as e:
            print "==============Exception===============================", e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    return HttpResponse(json.dumps(data), content_type='application/json')
