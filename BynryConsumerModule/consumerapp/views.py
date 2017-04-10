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
from consumerapp.models import ConsumerDetails, MeterReadingDetail
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

# SHUBHAM
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Pincode, Zone, Utility, Branch
from paymentapp.models import PaymentDetail
from vigilanceapp.models import VigilanceType
from consumerapp.models import MeterReadingDetail
from datetime import datetime

SERVER_URL = "http://192.168.10.102:8080"


def consumer_list(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        try:
            print 'consumerapp|views.py|consumer_list'
            total = ConsumerDetails.objects.filter(is_deleted=False).count()
            if request.session['branch_id']:
                branch_obj = Branch.objects.get(id=request.session['branch_id'])
                zones = Zone.objects.filter(is_deleted=False, branch=branch_obj)
            else:
                zones = Zone.objects.filter(is_deleted=False)
            data = {
                'city_list': get_city(request),
                'zone_list': zones,
                'branch_list': get_branch(request),
                'billcycle_list': get_billcycle(request),
                'route_list': get_RouteDetail(request),
                'pincode_list': get_pincode(request),
                'total': total
            }
        except Exception, e:
            data = {}
            print 'Exception|consumerapp|views.py|consumer_list', e
        return render(request, 'consumer_list.html', data)


def get_city(request):
    city_list = []
    try:
        print 'consumerapp|views.py|get_city'
        city_objs = City.objects.filter(is_deleted=False)
        for city in city_objs:
            city_list.append({'city_id': city.id, 'city': city.city})
        data = city_list
        return data
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_city', e
        data = {'city_list': 'none', 'message': 'No city available'}
        return data


def get_branch(request):
    branch_list = []
    try:
        print 'consumerapp|views.py|get_branch'
        branch_objs = Branch.objects.filter(is_deleted=False)
        for branch in branch_objs:
            branch_list.append({'branch_id': branch.id, 'branch_name': branch.branch_name})
        data = branch_list
        return data
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_branch', e
        data = {'branch_list': 'none', 'message': 'No branch available'}
        return data


def get_billcycle(request):
    billcycle_list = []
    try:
        print 'consumerapp|views.py|get_billcycle'
        bill_objs = BillCycle.objects.filter(is_deleted=False)
        for bill in bill_objs:
            billcycle_list.append({'bill_cycle_id': bill.id, 'bill_cycle_code': bill.bill_cycle_code})
        data = billcycle_list
        return data
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_billcycle', e
        data = {'billcycle_list': 'none', 'message': 'No billcycle available'}
        return data


def get_RouteDetail(request):
    route_list = []
    try:
        print 'consumerapp|views.py|get_RouteDetail'
        route_objs = RouteDetail.objects.filter(is_deleted=False)
        for route in route_objs:
            route_list.append({'route_id': route.id, 'route_code': route.route_code})
        data = route_list
        return data
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_RouteDetail', e
        data = {'route_list': 'none', 'message': 'No route available'}
        return data


def get_pincode(request):
    pincode_list = []
    try:
        print 'consumerapp|views.py|get_pincode'
        pincode_objs = Pincode.objects.filter(is_deleted=False)
        for pincode in pincode_objs:
            pincode_list.append({'pincode_id': pincode.id, 'pincode': pincode.pincode})
        data = pincode_list
        return data
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_pincode', e
        data = {'pincode_list': 'none', 'message': 'No pincode available'}
        return data


def get_consumer_list(request):
    try:
        print 'consumerapp|views.py|get_consumer_list'
        filter_zone = request.GET.get('filter_zone')
        filter_branch = request.GET.get('filter_branch')
        filter_bill = request.GET.get('filter_bill')
        filter_route = request.GET.get('filter_route')
        filter_category = request.GET.get('filter_category')
        filter_service = request.GET.get('filter_service')
        filter_from = request.GET.get('filter_from')
        filter_to = request.GET.get('filter_to')

        data = {}
        final_list = []
        try:
            consumer_obj_list = ConsumerDetails.objects.all()
            if filter_branch != 'all':
                consumer_obj_list = consumer_obj_list.filter(branch=filter_branch)
            if filter_zone != 'all':
                consumer_obj_list = consumer_obj_list.filter(zone=filter_zone)
            if filter_bill != 'all':
                consumer_obj_list = consumer_obj_list.filter(bill_cycle=filter_bill)
            if filter_route != 'all':
                consumer_obj_list = consumer_obj_list.filter(route=filter_route)
            if filter_category != 'all':
                consumer_obj_list = consumer_obj_list.filter(meter_category=filter_category)
            if filter_service != 'all':
                consumer_obj_list = consumer_obj_list.filter(connection_status=filter_service)
            if filter_from != '' and filter_to != '':
                filter_from = datetime.strptime(filter_from, "%d/%m/%Y")
                filter_from = filter_from.strftime("%Y-%m-%d")
                filter_to = datetime.strptime(filter_to, "%d/%m/%Y")
                filter_to = filter_to.strftime("%Y-%m-%d")
                consumer_obj_list = consumer_obj_list.filter(register_date__range=[filter_from, filter_to])

            for consumer_obj in consumer_obj_list:
                consumer_no = consumer_obj.consumer_no
                consumer_no1 = '<a href="/consumerapp/consumer-details/?consumer_id=' + str(
                    consumer_obj.id) + '">' + consumer_no + '</a>'
                consumer_name = consumer_obj.name
                contact_no = consumer_obj.contact_no
                email_id = consumer_obj.email_id
                servicerequest = ServiceRequest.objects.filter(consumer_id=consumer_obj.id).count()
                complaintrequest = ComplaintDetail.objects.filter(consumer_id=consumer_obj.id).count()
                connection_status = consumer_obj.connection_status
                action = '<a> <i class="fa fa-pencil" aria-hidden="true" onclick="edit_consumer(' + str(
                    consumer_obj.id) + ')"></i> </a>'

                consumer_data = {
                    'consumer_no': consumer_no1,
                    'consumer_name': consumer_name,
                    'contact_no': contact_no,
                    'email_id': email_id,
                    'servicerequest': servicerequest,
                    'complaintrequest': complaintrequest,
                    'connection_status': connection_status,
                    'action': action
                }
                final_list.append(consumer_data)
            data = {'success': 'true', 'data': final_list}
        except Exception as e:
            print 'Exception|consumerapp|views.py|get_consumer_list', e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|consumerapp|views.py|get_consumer_list', e
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_consumer_list', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_consumer(request):
    try:
        print 'consumerapp|views.py|edit_consumer'
        data = {}
        final_list = []
        try:
            consumer_obj = ConsumerDetails.objects.get(id=request.GET.get('consumer_id'))

            consumer_data = {
                'consumer_id': consumer_obj.id,
                'name': consumer_obj.name + ' (' + consumer_obj.consumer_no + ') ',
                'utility': consumer_obj.Utility.utility,
                'contact_no': consumer_obj.contact_no,
                'aadhar_no': consumer_obj.aadhar_no,
                'email_id': consumer_obj.email_id,
                'address_line_1': consumer_obj.address_line_1,
                'address_line_2': consumer_obj.address_line_2,
                'city_id': str(consumer_obj.city.id),
                'pincode_id': str(consumer_obj.pin_code.id),
                'branch_id': str(consumer_obj.branch.id),
                'bill_cycle_id': str(consumer_obj.bill_cycle.id),
                'route_id': str(consumer_obj.route.id),
                'zone_id': str(consumer_obj.zone.id),
                'meter_no': consumer_obj.meter_no,
                'meter_category': consumer_obj.meter_category,
                'sanction_load': consumer_obj.sanction_load
            }
            data = {'success': 'true', 'data': consumer_data}
        except Exception as e:
            print 'Exception|consumerapp|views.py|edit_consumer', e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|consumerapp|views.py|edit_consumer', e
    except Exception, e:
        print 'Exception|consumerapp|views.py|edit_consumer', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_consumer_profile(request):
    try:
        print 'consumerapp|views.py|save_consumer_profile'
        consumer_obj = ConsumerDetails.objects.get(id=request.POST.get('consumer_id'))
        consumer_obj.contact_no = request.POST.get('edit_contact')
        consumer_obj.email_id = request.POST.get('edit_email')
        consumer_obj.aadhar_no = request.POST.get('edit_aadhar')
        consumer_obj.address_line_1 = request.POST.get('edit_address1')
        consumer_obj.address_line_2 = request.POST.get('edit_address2')
        consumer_obj.meter_no = request.POST.get('edit_meter_no')
        consumer_obj.sanction_load = request.POST.get('edit_sanction_load')
        consumer_obj.city = City.objects.get(
            id=request.POST.get('edit_city')) if request.POST.get(
            'edit_city') else None
        consumer_obj.pin_code = Pincode.objects.get(
            id=request.POST.get('edit_pincode')) if request.POST.get(
            'edit_pincode') else None
        consumer_obj.branch = Branch.objects.get(
            id=request.POST.get('edit_branch')) if request.POST.get(
            'edit_branch') else None
        consumer_obj.zone = Zone.objects.get(
            id=request.POST.get('edit_zone')) if request.POST.get(
            'edit_zone') else None
        consumer_obj.bill_cycle = BillCycle.objects.get(
            id=request.POST.get('edit_bill_cycle')) if request.POST.get(
            'edit_bill_cycle') else None
        consumer_obj.route = RouteDetail.objects.get(
            id=request.POST.get('edit_route')) if request.POST.get(
            'edit_route') else None            
        consumer_obj.updated_on = datetime.now()
        consumer_obj.save();

        data = {
            'success': 'true',
            'message': 'User Updated Successfully.'
        }
    except Exception, e:
        print 'Exception|consumerapp|views.py|save_consumer_profile', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


def consumer_details(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        try:
            print 'consumerapp|views.py|consumer_details'
            data = {}
            final_list = []
            try:
                last_month_list = []
                month_list1 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
                month_list2 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                pre_Date = datetime.now()
                pre_Month = pre_Date.month
                pre_Year = pre_Date.year
                for i in range(6):
                    last_Year = pre_Year
                    last_Month = pre_Month - i
                    if last_Month <= 0:
                        last_Month = 12 + last_Month
                        last_Year = pre_Year - 1
                    month1 = month_list1[last_Month - 1] + '-' + str(last_Year)
                    month2 = month_list2[last_Month - 1] + '-' + str(last_Year)
                    last_month_list.append({'month1': month1, 'month2': month2})

                consumer_obj = ConsumerDetails.objects.get(id=request.GET.get('consumer_id'))
                address_line_1 = consumer_obj.address_line_1
                address_line_2 = consumer_obj.address_line_2
                address = address_line_1 + ', ' + address_line_2

                vigilanceType = VigilanceType.objects.filter(is_deleted=False)
                complaintType = ComplaintType.objects.filter(is_deleted=False)
                serviceType = ServiceRequestType.objects.filter(is_deleted=False)
                consumer_data = {
                    'consumer_id': request.GET.get('consumer_id'),
                    'name': consumer_obj.name,
                    'consumer_no': consumer_obj.consumer_no,
                    'aadhar_no': consumer_obj.aadhar_no,
                    'address': address,
                    'contact_no': consumer_obj.contact_no,
                    'email_id': consumer_obj.email_id,
                    'zone_name': str(consumer_obj.zone.zone_name),
                    'billcycle': str(consumer_obj.bill_cycle.bill_cycle_code),
                    'route': str(consumer_obj.route.route_code),
                    'utility': consumer_obj.Utility.utility,
                    'meter_no': consumer_obj.meter_no,
                    'meter_category': consumer_obj.meter_category,
                    'sanction_load': consumer_obj.sanction_load,
                    'pole_no': consumer_obj.pole_no,
                    'latitude': consumer_obj.latitude,
                    'longitude': consumer_obj.longitude,
                    'special_remark_location': consumer_obj.special_remark_location,
                }

                try:
                    meter_obj = MeterReadingDetail.objects.filter(consumer_id=consumer_obj).last()
                    # payment_obj = PaymentDetail.objects.filter(consumer_id=request.GET.get('consumer_id')).first()

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
                        'consumer_no': consumer_obj.name,
                        'address': consumer_address,
                        'bill_month': str(meter_obj.bill_month),
                        'consumption': str(total_reading),
                        'current_month_reading': str(meter_obj.current_month_reading),
                        'previous_month_reading': str(meter_obj.previous_month_reading),
                        'current_reading_date': meter_obj.current_reading_date.strftime('%d %b %Y'),
                        'prompt_date': meter_obj.prompt_date.strftime('%d %b %Y'),
                        'current_amount': str(total_charges),
                        'tariff_rate': str(meter_obj.tariff),
                        'net_amount': str(net_bill_amount),
                        'bill_amount_after_due_date': meter_obj.bill_amount_after_due_date,
                        'prompt_amount': str(meter_obj.prompt_amount),
                        'due_date': meter_obj.due_date.strftime('%d %b %Y'),
                    }
                except Exception, e:
                    print 'Exception|consumerapp|views.py|consumer_details', e
                    payment_data = {}

                data = {
                    'success': 'true',
                    'data': consumer_data,
                    'last_month_list': last_month_list,
                    'vigilanceType': vigilanceType,
                    'complaintType': complaintType,
                    'serviceType': ServiceRequestType.objects.filter(is_deleted=False),
                    'payment_data': payment_data
                }
            except Exception as e:
                print 'Exception|consumerapp|views.py|consumer_details', e
                data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
        except Exception, e:
            print 'Exception|consumerapp|views.py|consumer_details', e
        return render(request, 'consumer_details.html', data)


@csrf_exempt
def get_meter_details(request):
    try:
        print '\n\n\n\nconsumerapp|views.py|get_meter_details'
        data = {}
        final_list = []
        try:
            consumer_id = request.POST.get('consumer_id')
            monthList = request.POST.get('monthList')
            month = monthList.split('-')

            try:
                reading_obj = MeterReadingDetail.objects.get(consumer_id=consumer_id, bill_month=str(month[0]),
                                                             bill_months_year=str(month[1]))
                unit_consumed = reading_obj.unit_consumed
                current_reading = reading_obj.current_month_reading
                previous_reading = reading_obj.previous_month_reading
                current_reading_date = reading_obj.current_reading_date
                previous_month_reading_date = reading_obj.previous_month_reading_date
                billed_days = abs((current_reading_date - previous_month_reading_date).days)
                current_reading_date = current_reading_date.strftime("%d %b %Y")
                previous_month_reading_date = previous_month_reading_date.strftime("%d %b %Y")
                if reading_obj.meter_reading_image:
                    meter_reading_image = "http://" + get_current_site(
                        request).domain + reading_obj.meter_reading_image.url
                else:
                    meter_reading_image = ""


                consumer_data = {
                    'unit_consumed': unit_consumed,
                    'current_reading': current_reading,
                    'previous_reading': previous_reading,
                    'current_reading_date': current_reading_date,
                    'previous_month_reading_date': previous_month_reading_date,
                    'billed_days': billed_days,
                    'meter_reading_image': meter_reading_image
                }
            except Exception, e:
                print 'Exception|consumerapp|views.py|get_meter_details', e
                consumer_data = {}

            data = {'success': 'true', 'data': consumer_data}
        except Exception as e:
            print 'Exception|consumerapp|views.py|get_meter_details', e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|consumerapp|views.py|get_meter_details', e
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_meter_details', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_consumer_details(request):
    try:
        print 'consumerapp|views.py|save_consumer_details'
        consumer_obj = ConsumerDetails.objects.get(id=request.POST.get('consumer_id'))
        consumer_obj.meter_no = request.POST.get('meter_no')
        consumer_obj.meter_category = request.POST.get('category')
        consumer_obj.sanction_load = request.POST.get('saction_load')
        consumer_obj.pole_no = request.POST.get('panel_no')
        consumer_obj.latitude = request.POST.get('latitude')
        consumer_obj.longitude = request.POST.get('longitude')
        consumer_obj.special_remark_location = request.POST.get('special_instruction')
        consumer_obj.updated_on = datetime.now()
        consumer_obj.save();

        data = {
            'success': 'true',
            'message': 'Meter Details Updated Successfully.'
        }
    except Exception, e:
        print 'Exception|consumerapp|views.py|save_consumer_details', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

# TO GET THE Pincode
def get_pincode_front(request):
    print 'consumerapp|views.py|get_pincode'
    city_id = request.GET.get('city_id')
    pincode_list = []
    try:
        pincode_objs = Pincode.objects.filter(city=city_id)
        for pincode in pincode_objs:
            options_data = '<option value=' + str(
                pincode.id) + '>' + pincode.pincode + '</option>'
            pincode_list.append(options_data)
        data = {'pincode_list': pincode_list}
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_pincode', e
        data = {'pincode_list': 'No Pincodes available'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# TO GET THE Branch
def get_branch_front(request):
    print 'consumerapp|views.py|get_branch_front'
    city_id = request.GET.get('city_id')
    branch_list = []
    try:
        branch_objs = Branch.objects.filter(city=city_id)
        for branch in branch_objs:
            options_data = '<option value=' + str(
                branch.id) + '>' + branch.branch_name + '</option>'
            branch_list.append(options_data)
        data = {'branch_list': branch_list}
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_branch_front', e
        data = {'branch_list': 'No Branch available'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# TO GET THE Zone
def get_zone_front(request):
    print 'consumerapp|views.py|get_zone_front'
    branch_id = request.GET.get('branch_id')
    zone_list = []
    try:
        zone_objs = Zone.objects.filter(branch=branch_id)
        for zone in zone_objs:
            options_data = '<option value=' + str(
                zone.id) + '>' + zone.zone_name + '</option>'
            zone_list.append(options_data)
        data = {'zone_list': zone_list}
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_zone_front', e
        data = {'zone_list': 'No Zone available'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# TO GET THE Bill Cycle
def get_billcycle_front(request):
    print 'consumerapp|views.py|get_billcycle_front'
    zone_id = request.GET.get('zone_id')
    billcycle_list = []
    try:
        billcycle_objs = BillCycle.objects.filter(zone=zone_id)
        for bill in billcycle_objs:
            options_data = '<option value=' + str(
                bill.id) + '>' + bill.bill_cycle_code + '</option>'
            billcycle_list.append(options_data)
        data = {'billcycle_list': billcycle_list}
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_billcycle_front', e
        data = {'billcycle_list': 'No Zone available'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# TO GET THE Bill Cycle
def get_route_front(request):
    print 'consumerapp|views.py|get_route_front'
    bill_cycle_id = request.GET.get('bill_cycle_id')
    route_list = []
    try:
        route_objs = RouteDetail.objects.filter(billcycle=bill_cycle_id)
        for route in route_objs:
            options_data = '<option value=' + str(
                route.id) + '>' + route.route_code + '</option>'
            route_list.append(options_data)
        data = {'route_list': route_list}
    except Exception, e:
        print 'Exception|consumerapp|views.py|get_route_front', e
        data = {'route_list': 'No Route available'}
    return HttpResponse(json.dumps(data), content_type='application/json')
