# __author__='Swapnil Kadu'
import traceback
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from serviceapp.models import *
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Zone, Branch
from consumerapp.models import ConsumerDetails
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# To view service page
def service_request(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        print 'serviceapp|views.py|service_request'
        # total, open and closed service details count
        total = ServiceRequest.objects.filter(is_deleted=False).count()
        open = ServiceRequest.objects.filter(status='Open', is_deleted=False).count()
        closed = ServiceRequest.objects.filter(status='Closed', is_deleted=False).count()

        serviceType = ServiceRequestType.objects.filter(is_deleted=False) # Service Types
        branch_list = Branch.objects.filter(is_deleted=False) # Branch List
        if request.session['branch_id']:
            branch_obj = Branch.objects.get(id=request.session['branch_id'])
            zones = Zone.objects.filter(is_deleted=False, branch=branch_obj)
        else:
            zones = ''
        data = {
            'total': total,
            'open': open,
            'closed': closed,
            'ServiceType': serviceType,
            'branch_list': branch_list,
            'zones': zones
        }
        return render(request, 'services.html', data)

# To get service data (filter parameters: service type, status, source, zone, bill cycle, route, consumer)
def get_service_data(request):
    try:
        print 'serviceapp|views.py|get_service_data'
        service_list = []
        service_obj = ServiceRequest.objects.all()

        # filter service data by service type
        if request.GET.get('service_type') == 'all':
            serviceType = ServiceRequestType.objects.filter(is_deleted=False)
        else:
            serviceType = ServiceRequestType.objects.filter(is_deleted=False, id=request.GET.get('service_type'))
        service_obj = service_obj.filter(service_type__in=serviceType)
        # filter service data by service status
        if request.GET.get('service_status') and request.GET.get('service_status') != "all":
            service_obj = service_obj.filter(status=request.GET.get('service_status'))
        # filter service data by service source
        if request.GET.get('service_source') and request.GET.get('service_source') != "all":
            service_obj = service_obj.filter(source=request.GET.get('service_source'))
        # filter service data by service consumer
        if request.GET.get('consumer_id'):
            service_obj = service_obj.filter(consumer_id=request.GET.get('consumer_id'))
        else:
            # filter service data by service branch
            if request.GET.get('branch') and request.GET.get('branch') != "all":
                consumer = ConsumerDetails.objects.filter(branch=request.GET.get('branch'))
                service_obj = service_obj.filter(consumer_id__in=consumer)
            # filter service data by service zone
            if request.GET.get('zone') and request.GET.get('zone') != "all":
                consumer = ConsumerDetails.objects.filter(zone=request.GET.get('zone'))
                service_obj = service_obj.filter(consumer_id__in=consumer)
            # filter service data by service bill cycle
            if request.GET.get('bill_cycle') and request.GET.get('bill_cycle') != "all":
                consumer = ConsumerDetails.objects.filter(bill_cycle=request.GET.get('bill_cycle'))
                service_obj = service_obj.filter(consumer_id__in=consumer)
            # filter service data by service route
            if request.GET.get('route') and request.GET.get('route') != "all":
                consumer = ConsumerDetails.objects.filter(route=request.GET.get('route'))
                service_obj = service_obj.filter(consumer_id__in=consumer)
        # filter service data by date range
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y') + datetime.timedelta(days=1)
            service_obj = service_obj.filter(request_date__range=[start_date, end_date])
        # filtered service data list

        #SHubham S Need to chage==>>>>>
        service_data = {
            'service_no': '1025',
            'service_type' : '  Meter Change',
            'raised_date' : 'September 09, 2017 08:56 AM',
            'consumer_no' : '11111111111',
            'consumer_name' : 'ASD',
            'service_source' : 'Mobile',
            'service_status' : '<a data-toggle="modal" data-target="#assign_job">Open</a>',

        } 
        service_list.append(service_data)
        #=========>>>>>>
        for service in service_obj:
        	print '------service-----',service
        	service_data = {
        		'service_no': '<a onclick="service_details(' + str(service.id) + ')">' + service.service_no + '</a>',
        		'service_type' :service.service_type.request_type,
                # 'service_type' : '<a onclick="service_details_reconnection(' + str(service.id) + ')">' + service.service_type.request_type+ '</a>',
        		'raised_date' : service.request_date.strftime('%B %d, %Y %I:%M %p'),
        		'consumer_no' : '<a onclick="consumer_details(' + str(service.consumer_id.id) + ')">' + service.consumer_id.consumer_no + '</a>',
        		'consumer_name' : service.consumer_id.name,
                'service_source' : service.source,
        		'service_status' : service.status            
        	}
        	service_list.append(service_data)        

        	# service_data = {
        	# 	'service_no': '<a onclick="service_details(' + str(
			      #   service.id) + ')">' + service.service_no + '</a>',
        	# 	'service_type': service.service_type.request_type,
        	# 	'raised_date': service.request_date.strftime('%B %d, %Y %I:%M %p'),
        	# 	'consumer_no': '<a onclick="consumer_details(' + str(
			      #   service.consumer_id.id) + ')">' + service.consumer_id.consumer_no + '</a>',
        	# 	'consumer_name': service.consumer_id.name,
        	# 	'service_source': service.source,
        	# 	'service_status': service.status
        	# 	}
        	# service_list.append(service_data)
		data = {'data': service_list}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|serviceapp|views.py|get_service_datatable', e
        data = {'msg': 'error'}
        print e
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

# To get service details
@csrf_exempt
def get_service_details(request):
    try:
        print 'serviceapp|views.py|get_service_details'
        # filter service data by service id
        service = ServiceRequest.objects.get(id=request.POST.get('service_id'))
        # get service details by service object
        serviceIdDetail = {
            'serviceID': service.service_no,
            'serviceType': service.service_type.request_type,
            'serviceStatus': str(service.status),
            'serviceConsumerName': service.consumer_id.name,
            'serviceConsumerNo': service.consumer_id.consumer_no,
            'serviceRequest': service.consumer_remark,
        }

        data = {'success': 'true', 'serviceDetail': serviceIdDetail}
        print 'Request show history out service request with---', data

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|serviceapp|views.py|get_service_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')

# To get consumer details
@csrf_exempt
def get_consumer_details(request):
    try:
        print 'serviceapp|views.py|get_consumer_details'
        # filter consumer details by consumer id
        consumerDetails = ConsumerDetails.objects.get(id=request.POST.get('consumer_id'))
        consumer_address = consumerDetails.address_line_1 # Consumer address line 1
        if consumerDetails.address_line_2:
            consumer_address = consumer_address + ', ' + consumerDetails.address_line_2 # Consumer address line 2
        if consumerDetails.pin_code:
            consumer_address = consumer_address + ', ' \
                               + consumerDetails.city.city + ' - ' + consumerDetails.pin_code.pincode + '.'

        # get consumer details by consumer object
        getConsumer = {
            'billCycle': consumerDetails.bill_cycle.bill_cycle_code,
            'consumerBranch' : consumerDetails.branch.branch_name,
            'consumerRoute': consumerDetails.route.route_code,
            'consumerZone': consumerDetails.bill_cycle.zone.zone_name,
            'consumerNo': consumerDetails.consumer_no,
            'consumerName': consumerDetails.name,
            'consumerAddress': consumer_address
        }
        data = {'success': 'true', 'consumerDetail': getConsumer}
        print 'Request show history out service request with---', data

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|serviceapp|views.py|get_consumer_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')

