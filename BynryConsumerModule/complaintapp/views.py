# __author__='Vikas Kumawat' Date: 09/03/2016
import traceback
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from .models import ComplaintType, ComplaintDetail
from BynryConsumerModuleapp.models import *
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
import datetime


# To view complaints page
def complaint(request):
    try:
        print 'complaintapp|views.py|complaint'
        # total, open and closed complaint details count
        total = ComplaintDetail.objects.filter(is_deleted=False).count()
        open = ComplaintDetail.objects.filter(complaint_status='Open', is_deleted=False).count()
        closed = ComplaintDetail.objects.filter(complaint_status='Closed', is_deleted=False).count()

        complaintType = ComplaintType.objects.filter(is_deleted=False)  # complaint types
        zone = Zone.objects.filter(is_deleted=False)  # zone list

        data = {
            'total': total,
            'open': open,
            'closed': closed,
            'complaintType': complaintType,
            'zones': zone
        }
    except Exception, e:
        print 'Exception|comlpaintapp|views.py|complaint', e
        data = {}
    return render(request, 'complaints.html', data)


# To get complaint data (filter parameters: complaint type, status, source, zone, bill cycle, route, consumer)
def get_complaint_data(request):
    try:
        print 'complaintapp|views.py|get_complaint_data'
        complaint_list = []
        complaint_obj = ComplaintDetail.objects.all()

        # filter complaint data by complaint type
        if request.GET.get('complaint_type'):
            if request.GET.get('complaint_type') == 'all':
                complaintType = ComplaintType.objects.filter(is_deleted=False)
            else:
                complaintType = ComplaintType.objects.filter(is_deleted=False, id=request.GET.get('complaint_type'))
            complaint_obj = complaint_obj.filter(complaint_type_id__in=complaintType)

        # filter complaint data by complaint status
        if request.GET.get('complaint_status') and request.GET.get('complaint_status') != "all":
            complaint_obj = complaint_obj.filter(complaint_status=request.GET.get('complaint_status'))

        # filter complaint data by complaint source
        if request.GET.get('complaint_source') and request.GET.get('complaint_source') != "all":
            complaint_obj = complaint_obj.filter(complaint_source=request.GET.get('complaint_source'))

        # filter complaint data by consumer if not consumer than by zone, bill cycle, route
        if request.GET.get('consumer_id'):
            complaint_obj = complaint_obj.filter(consumer_id=request.GET.get('consumer_id'))
        else:
            # filter complaint data by zone
            if request.GET.get('zone') and request.GET.get('zone') != "all":
                # filter consumer by zone
                consumer = ConsumerDetails.objects.filter(zone=request.GET.get('zone'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
            # filter complaint data by bill cycle
            if request.GET.get('bill_cycle') and request.GET.get('bill_cycle') != "all":
                # filter consumer by bill cycle
                consumer = ConsumerDetails.objects.filter(bill_cycle=request.GET.get('bill_cycle'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)
            # filter complaint data by route
            if request.GET.get('route') and request.GET.get('route') != "all":
                # filter consumer by bill cycle
                consumer = ConsumerDetails.objects.filter(route=request.GET.get('route'))
                complaint_obj = complaint_obj.filter(consumer_id__in=consumer)

        # filter complaint data by date range
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y') + datetime.timedelta(days=1)
            complaint_obj = complaint_obj.filter(complaint_date__range=[start_date, end_date])

        # complaint data result
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
        print 'Exception|comlpaintapp|views.py|get_complaint_data', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


# to get complaint details
@login_required(login_url='/')
def get_complaint_details(request):
    try:
        print 'complaintapp|views.py|get_complaint_details'
        # filter complaint by complaint id
        complaint = ComplaintDetail.objects.get(id=request.GET.get('complaint_id'))
        # complaint image path with server url
        image_address = "http://" + get_current_site(request).domain + "/" + complaint.complaint_img.url

        # complaint detail result
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
    except Exception, e:
        print 'Exception|comlpaintapp|views.py|get_complaint_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# to get consumer details
@login_required(login_url='/')
def get_consumer_details(request):
    try:
        print 'complaintapp|views.py|get_consumer_details'
        # filter consumer detail by consumer id
        consumerDetails = ConsumerDetails.objects.get(id=request.GET.get('consumer_id'))
        # consumer address
        consumer_address = consumerDetails.address_line_1
        if consumerDetails.address_line_2:
            consumer_address = consumer_address + ', ' + consumerDetails.address_line_2
        if consumerDetails.pin_code:
            consumer_address = consumer_address + ' - ' + consumerDetails.pin_code.pincode + '.'

        # consumer details result
        consumerDetail = {
            'billCycle': consumerDetails.bill_cycle.bill_cycle_code,
            'consumerCity': consumerDetails.city.city,
            'consumerRoute': consumerDetails.route.route_code,
            'consumerZone': consumerDetails.bill_cycle.zone.zone_name,
            'consumerNo': consumerDetails.consumer_no,
            'consumerName': consumerDetails.name,
            'consumerAddress': consumer_address
        }
        data = {'success': 'true', 'consumerDetail': consumerDetail}
    except Exception, e:
        print 'Exception|comlpaintapp|views.py|get_consumer_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# to get bill cycle wrt zone
def get_bill_cycle(request):
    try:
        print 'complaintapp|views.py|get_bill_cycle'
        bill_cycle_list = []
        # filer bill cycle by zone_id
        if request.GET.get('zone') != 'all':
            bill_cycle_obj = BillCycle.objects.filter(is_deleted=False, zone=request.GET.get('zone'))
        else:
            bill_cycle_obj = BillCycle.objects.filter(is_deleted=False)

        # bill cycle result
        for bill_cycle in bill_cycle_obj:
            bill_cycle_data = {
                'bill_cycle_id': bill_cycle.id,
                'bill_cycle': bill_cycle.bill_cycle_code
            }
            bill_cycle_list.append(bill_cycle_data)
        data = {'success': 'true', 'bill_cycle': bill_cycle_list}
    except Exception, e:
        print "Exception|comlpaintapp|views.py|get_bill_cycle", e
        data = {'success': 'false', 'bill_cycle': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


# to get bill cycle wrt bill cycle
def get_route(request):
    try:
        print 'complaintapp|views.py|get_route'
        route_list = []
        # filer bill cycle by bill cycle
        if request.GET.get('bill_cycle') != 'all':
            route_obj = RouteDetail.objects.filter(is_deleted=False, billcycle=request.GET.get('bill_cycle'))
        else:
            route_obj = RouteDetail.objects.filter(is_deleted=False)

        # route result
        for route in route_obj:
            route_data = {
                'route_id': route.id,
                'route': route.route_code
            }
            route_list.append(route_data)
        data = {'success': 'true', 'route_list': route_list}
    except Exception, e:
        print "Exception|comlpaintapp|views.py|get_route", e
        data = {'success': 'false', 'route_list': []}
    return HttpResponse(json.dumps(data), content_type='application/json')
