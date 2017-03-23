__auther__ = "Vikas Kumawat"
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from .models import ComplaintType, ComplaintDetail
from BynryConsumerModuleapp.models import Zone, BillCycle, RouteDetail, Branch
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render


def complaint(request):
    """To view complaints page"""
    try:
        print 'complaintapp|views.py|complaint'
        # total, open and closed complaint details count
        total = ComplaintDetail.objects.filter(is_deleted=False).count()
        open_case = ComplaintDetail.objects.filter(
            complaint_status='Open', is_deleted=False).count()
        closed = ComplaintDetail.objects.filter(
            complaint_status='Closed', is_deleted=False).count()
        complaint_type = ComplaintType.objects.filter(is_deleted=False)
        branch_list = Branch.objects.filter(is_deleted=False)

        if request.session['branch_id']:
            branch_obj = Branch.objects.get(id = request.session['branch_id'])
            zones = Zone.objects.filter(is_deleted=False,branch = branch_obj)
        else:
            zones = ''
        data = {
            'total' : total,
            'open' : open_case,
            'closed' : closed,
            'complaintType' : complaint_type,
            'branch_list' : branch_list,
            'zones' : zones
        }
    except Exception as exe:
        print 'Exception|comlpaintapp|views.py|complaint', exe
        data = {}
    return render(request, 'complaints.html', data)


def get_complaint_data(request):
    """ To get complaint data
    (filter parameters : complaint type, status,
    source,zone, bill cycle, route, consumer)"""
    try:
        print 'complaintapp|views.py|get_complaint_data'
        complaint_list = []
        complaint_obj = ComplaintDetail.objects.all()

        # filter complaint data by date range
        if request.GET.get('start_date') and \
                request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(
                request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(
                request.GET.get('end_date'), '%d/%m/%Y').replace(
                hour=23, minute=59, second=59)
            complaint_obj = complaint_obj.filter(
                complaint_date__range=[start_date, end_date])
        # filter complaint data by complaint type
        elif request.GET.get('complaint_type'):
            if request.GET.get('complaint_type') == 'all':
                complaint_type = ComplaintType.objects.filter(is_deleted=False)
            else:
                complaint_type = ComplaintType.objects.filter(
                    is_deleted=False, id=request.GET.get('complaint_type'))
            complaint_obj = complaint_obj.filter(
                complaint_type_id__in=complaint_type)

        # filter complaint data by complaint status
        elif request.GET.get('complaint_status') and \
                        request.GET.get('complaint_status') != "all":
            complaint_obj = complaint_obj.filter(
                complaint_status=request.GET.get('complaint_status'))

        # filter complaint data by complaint source
        elif request.GET.get('complaint_source') and \
                        request.GET.get('complaint_source') != "all":
            complaint_obj = complaint_obj.filter(
                complaint_source=request.GET.get('complaint_source'))

        # filter complaint data by consumer
        # if not consumer than by zone, bill cycle, route
        elif request.GET.get('consumer_id'):
            complaint_obj = complaint_obj.filter(
                consumer_id=request.GET.get('consumer_id'))
        else:
            # filter complaint data by branch
            if request.GET.get('branch') and \
                            request.GET.get('branch') != "all":
                # filter consumer by branch
                consumer = ConsumerDetails.objects.filter(
                    branch=request.GET.get('branch'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
            # filter complaint data by zone
            elif request.GET.get('zone') and \
                            request.GET.get('zone') != "all":
                # filter consumer by zone
                consumer = ConsumerDetails.objects.filter(
                    zone=request.GET.get('zone'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
            # filter complaint data by bill cycle
            elif request.GET.get('bill_cycle') and \
                            request.GET.get('bill_cycle') != "all":
                # filter consumer by bill cycle
                consumer = ConsumerDetails.objects.filter(
                    bill_cycle=request.GET.get('bill_cycle'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
            # filter complaint data by route
            elif request.GET.get('route') and \
                            request.GET.get('route') != "all":
                # filter consumer by bill cycle
                consumer = ConsumerDetails.objects.filter(
                    route=request.GET.get('route'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)

        # complaint data result
        for complaints in complaint_obj:
            complaint_data = {
                'complaint_no' : '<a onclick="complaint_details(' + str(
                    complaints.id) + ')">' + complaints.complaint_no + '</a>',
                'complaint_type' : complaints.complaint_type_id.complaint_type,
                'raised_date' : complaints.complaint_date.strftime('%d/%m/%Y'),
                'consumer_no' : '<a onclick="consumer_details(' + str(
                    complaints.consumer_id.id) + ')">' +
                               complaints.consumer_id.consumer_no + '</a>',
                'consumer_name' : complaints.consumer_id.name,
                'complaint_source' : complaints.complaint_source,
                'complaint_status' : complaints.complaint_status,
            }
            complaint_list.append(complaint_data)
        data = {'data' : complaint_list}
    except Exception as exe:
        print 'Exception|comlpaintapp|views.py|get_complaint_data', exe
        data = {'msg' : 'error'}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder),
                        content_type='application/json')


@login_required(login_url='/')
def get_complaint_details(request):
    """to get complaint details"""
    try:
        print 'complaintapp|views.py|get_complaint_details'
        # filter complaint by complaint id
        complaints = ComplaintDetail.objects.get(
            id=request.GET.get('complaint_id'))
        # complaint image path with server url
        image_address = "http://" + get_current_site(request).domain \
                        + "/" + complaints.complaint_img.url

        # complaint detail result
        complaint_detail = {
            'complaintID' : complaints.complaint_no,
            'complaintType' : complaints.complaint_type_id.complaint_type,
            'complaintConsumerName' : complaints.consumer_id.name,
            'complaintConsumerNo' : complaints.consumer_id.consumer_no,
            'complaintStatus' : complaints.complaint_status,
            'consumerRemark' : complaints.remark,
            'closureRemark' : complaints.closure_remark,
            'complaint_img' : image_address,
        }
        data = {'success' : 'true', 'complaintDetail' : complaint_detail}
    except Exception as exe:
        print 'Exception|comlpaintapp|views.py|get_complaint_details', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/')
def get_consumer_details(request):
    """ to get consumer details"""
    try:
        print 'complaintapp|views.py|get_consumer_details'
        # filter consumer detail by consumer id
        consumer_details = ConsumerDetails.objects.get(
            id=request.GET.get('consumer_id'))
        # consumer address
        consumer_address = consumer_details.address_line_1
        if consumer_details.address_line_2:
            consumer_address = consumer_address + ', ' \
                               + consumer_details.address_line_2
        if consumer_details.pin_code:
            consumer_address = consumer_address + ' - ' \
                               + consumer_details.pin_code.pincode + '.'

        # consumer details result
        consumer_data = {
            'billCycle' : consumer_details.bill_cycle.bill_cycle_code,
            'consumerCity' : consumer_details.city.city,
            'consumerRoute' : consumer_details.route.route_code,
            'consumerZone' : consumer_details.bill_cycle.zone.zone_name,
            'consumerNo' : consumer_details.consumer_no,
            'consumerName' : consumer_details.name,
            'consumerAddress' : consumer_address
        }
        data = {
            'success' : 'true',
            'consumerDetail' : consumer_data
        }
    except Exception as exe:
        print 'Exception|comlpaintapp|views.py|get_consumer_details', exe
        data = {'success' : 'false', 'error' : 'Exception ' + str(exe)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_zone(request):
    """to get zone wrt branch"""
    try:
        print 'complaintapp|views.py|get_zone'
        zone_list = []
        # filer zone by branch_id
        if request.GET.get('zone') != 'all':
            zone_obj = Zone.objects.filter(
                is_deleted=False, branch=request.GET.get('branch'))
        else:
            zone_obj = Zone.objects.filter(is_deleted=False)
        # zone result
        for zone in zone_obj:
            zone_data = {
                'zone_id' : zone.id,
                'zone_name' : zone.zone_name
            }
            zone_list.append(zone_data)
        data = {'success' : 'true', 'zone' : zone_list}
    except Exception as exe:
        print "Exception|comlpaintapp|views.py|get_zone", exe
        data = {'success' : 'false', 'zone' : []}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_bill_cycle(request):
    """to get bill cycle wrt zone"""
    try:
        print 'complaintapp|views.py|get_bill_cycle'
        bill_cycle_list = []
        # filer bill cycle by zone_id
        if request.GET.get('zone') != 'all':
            bill_cycle_obj = BillCycle.objects.filter(
                is_deleted=False, zone=request.GET.get('zone'))
        else:
            bill_cycle_obj = BillCycle.objects.filter(is_deleted=False)

        # bill cycle result
        for bill_cycle in bill_cycle_obj:
            bill_cycle_data = {
                'bill_cycle_id' : bill_cycle.id,
                'bill_cycle' : bill_cycle.bill_cycle_code
            }
            bill_cycle_list.append(bill_cycle_data)
        data = {'success' : 'true', 'bill_cycle' : bill_cycle_list}
    except Exception as exe:
        print "Exception|comlpaintapp|views.py|get_bill_cycle", exe
        data = {'success' : 'false', 'bill_cycle' : []}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_route(request):
    """to get bill cycle wrt bill cycle"""
    try:
        print 'complaintapp|views.py|get_route'
        route_list = []
        # filer bill cycle by bill cycle
        if request.GET.get('bill_cycle') != 'all':
            route_obj = RouteDetail.objects.filter(
                is_deleted=False, billcycle=request.GET.get('bill_cycle'))
        else:
            route_obj = RouteDetail.objects.filter(is_deleted=False)

        # route result
        for route in route_obj:
            route_data = {
                'route_id' : route.id,
                'route' : route.route_code
            }
            route_list.append(route_data)
        data = {'success' : 'true', 'route_list' : route_list}
    except Exception as exe:
        print "Exception|comlpaintapp|views.py|get_route", exe
        data = {'success' : 'false', 'route_list' : []}
    return HttpResponse(json.dumps(data), content_type='application/json')
