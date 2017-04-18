# __author__='Vikas Kumawat' Date: 09/03/2016
import traceback
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
from BynryConsumerModuleapp.models import *
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Branch
from consumerapp.models import ConsumerDetails
import datetime
from django.contrib.sites.shortcuts import get_current_site

# To view vigilance page
def vigilance(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        try:
            print 'vigilanceapp|views.py|complaint'
            # total, open and closed vigilance count
            total = VigilanceDetail.objects.filter(is_deleted=False).count()
            open = VigilanceDetail.objects.filter(vigilance_status='Open', is_deleted=False).count()
            closed = VigilanceDetail.objects.filter(vigilance_status='Closed', is_deleted=False).count()

            vigilanceType = VigilanceType.objects.filter(is_deleted=False) # vigilance type
            branch_list = Branch.objects.filter(is_deleted=False) # branch list
            if request.session['branch_id']:
                branch_obj = Branch.objects.get(id=request.session['branch_id'])
                zones = Zone.objects.filter(is_deleted=False, branch=branch_obj)
            else:
                zones = ''

            data = {
                'total': total,
                'open': open,
                'closed': closed,
                'vigilanceType': vigilanceType,
                'branch_list': branch_list,
                'zones': zones
            }
        except Exception, e:
            print 'Exception|vigilanceapp|views.py|vigilance', e
            data = {}
        return render(request, 'vigilance_cases.html', data)

# To get vigilance data (filter parameters: vigilance type, status, source, zone, bill cycle, route, consumer)
def get_vigilance_data(request):
    try:
        print 'vigilanceapp|views.py|get_vigilance_data'
        vigilance_list = []
        vigilance_obj = VigilanceDetail.objects.all()

        # filter vigilance data by vigilance type
        if request.GET.get('vigilance_type'):
            if request.GET.get('vigilance_type') == 'all':
                vigilanceType = VigilanceType.objects.filter(is_deleted=False)
            else:
                vigilanceType = VigilanceType.objects.filter(is_deleted=False, id=request.GET.get('vigilance_type'))
            vigilance_obj = vigilance_obj.filter(vigilance_type_id__in=vigilanceType)

        # filter vigilance data by vigilance status
        if request.GET.get('vigilance_status') and request.GET.get('vigilance_status') != "all":
            vigilance_obj = vigilance_obj.filter(vigilance_status=request.GET.get('vigilance_status'))

        # filter vigilance data by vigilance source
        if request.GET.get('vigilance_source') and request.GET.get('vigilance_source') != "all":
            vigilance_obj = vigilance_obj.filter(vigilance_source=request.GET.get('vigilance_source'))

        # filter vigilance data by consumer
        if request.GET.get('consumer_id'):
            vigilance_obj = vigilance_obj.filter(consumer_id=request.GET.get('consumer_id'))
        else:
            # filter vigilance data by branch
            if request.GET.get('branch') and request.GET.get('branch') != "all":
                consumer = ConsumerDetails.objects.filter(branch=request.GET.get('branch'))
                vigilance_obj = vigilance_obj.filter(consumer_id__in=consumer)
            # filter vigilance data by zone
            if request.GET.get('zone') and request.GET.get('zone') != "all":
                consumer = ConsumerDetails.objects.filter(zone=request.GET.get('zone'))
                vigilance_obj = vigilance_obj.filter(consumer_id__in=consumer)
            # filter vigilance data by bill cycle
            if request.GET.get('bill_cycle') and request.GET.get('bill_cycle') != "all":
                consumer = ConsumerDetails.objects.filter(bill_cycle=request.GET.get('bill_cycle'))
                vigilance_obj = vigilance_obj.filter(consumer_id__in=consumer)
            # filter vigilance data by route
            if request.GET.get('route') and request.GET.get('route') != "all":
                consumer = ConsumerDetails.objects.filter(route=request.GET.get('route'))
                vigilance_obj = vigilance_obj.filter(consumer_id__in=consumer)

        # filter vigilance data by date range
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59, second=59)
            vigilance_obj = vigilance_obj.filter(created_on__range=[start_date, end_date])

        # vigilance data result
        for vigilance in vigilance_obj:
            vigilance_data = {
                'case_id': '<a onclick="vigilance_details(' + str(
                    vigilance.id) + ')">' + vigilance.case_id + '</a>',
                'vigilance_type': vigilance.vigilance_type_id.vigilance_type,
                'registered_date': vigilance.created_on.strftime('%B %d, %Y %I:%M %p'),
                'consumer_no': '<a onclick="consumer_details(' + str(
                    vigilance.consumer_id.id) + ')">' + vigilance.consumer_id.consumer_no + '</a>',
                'consumer_name': vigilance.consumer_id.name,
                'vigilance_source': vigilance.vigilance_source,
                'vigilance_status': vigilance.vigilance_status,
            }
            vigilance_list.append(vigilance_data)
        data = {'data': vigilance_list}
    except Exception, e:
        print 'Exception|vigilanceapp|views.py|get_vigilance_data', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


@login_required(login_url='/')
def get_vigilance_details(request):
    try:
        print 'vigilanceapp|views.py|get_vigilance_details'
        vigilance = VigilanceDetail.objects.get(id=request.GET.get('vigilance_id'))
        theftaddress = vigilance.address+ ', '+vigilance.city.city+ ', '+vigilance.pin_code.pincode

        # vigilance image path with server url
        vigilance_images = ConsumerVigilanceImage.objects.filter(vigilance_id = vigilance)

        image_list = []
        if vigilance_images:
            for vigilance_image in vigilance_images:
                image_address = "http://" + get_current_site(request).domain + vigilance_image.document_files.url
                image_list.append(image_address)
        else:
            image_address = "http://" + get_current_site(request).domain + '/static/assets/placeholder.png'
            image_list.append(image_address)        

        # vigilance details
        vigilanceDetail = {
            'caseID': vigilance.case_id,
            'vigilanceType': vigilance.vigilance_type_id.vigilance_type,
            'registeredDate': vigilance.created_on.strftime('%d/%m/%Y'),
            'registeredSource': vigilance.vigilance_source,
            'caseStatus': vigilance.vigilance_status,
            'theftFound': vigilance.theft_found,
            'theftname':vigilance.theft_name,
            'theftaddress':theftaddress,
            'vigilanceRemark': vigilance.vigilance_remark,
            'penaltyAmount': '',
            'paymentStatus': '',
            'paymentMethod': '',
            'courtRemark': '',
            'courtCaseStatus': '',
            'vigilance_img' : image_list,
        }
        try:
            # vigilance penalty details
            vigilancePenalty = VigilancePenalyDetail.objects.get(vigilance_id=request.GET.get('vigilance_id'))
            vigilanceDetail['penaltyAmount'] = vigilancePenalty.payment
            vigilanceDetail['paymentStatus'] = vigilancePenalty.payment_status
            vigilanceDetail['paymentMethod'] = vigilancePenalty.payment_method
        except:
            pass
        try:
            #vigilance court case details
            courtCase = CourtCaseDetail.objects.get(vigilance_id=request.GET.get('vigilance_id'))
            vigilanceDetail['courtRemark'] = courtCase.court_remark
            vigilanceDetail['courtCaseStatus'] = courtCase.case_status
        except:
            pass

        data = {'success': 'true', 'vigilanceDetail': vigilanceDetail}
    except Exception, e:
        print 'Exception|vigilanceapp|views.py|get_vigilance_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')