from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from consumerapp.views import get_city, get_pincode
from nscapp.models import NewConsumerRequest
from BynryConsumerModuleapp.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from consumerapp.models import ConsumerDetails
from nscapp.models import *


# Create your views here.
def new_connection_list(request):
    try:
        print 'nscapp|views.py|new_connection'
        status_list = ['Registered', 'KYC', 'Technical', 'Payment']
        data = {
            'total': NewConsumerRequest.objects.all().count(),
            'open': NewConsumerRequest.objects.filter(status__in=status_list).count(),
            'closed': NewConsumerRequest.objects.filter(status='Closed').count(),
            'route_list': RouteDetail.objects.filter(is_deleted=False)
        }

    except Exception, e:
        data = {}
        print 'Exception|nscapp|views.py|new_connection', e
    return render(request, 'nsc_template/new_connection_list.html', data)


def add_new_consumer(request):
    try:
        print 'nscapp|views.py|add_new_consumer'
        data = {

            'city_list': get_city(request),
            'pincode_list': get_pincode(request)
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|add_new_consumer', e
    return render(request, 'nsc_template/add_new_consumer.html', data)


def get_nsc_data(request):
    try:
        nsc_list = []
        nsc_obj = NewConsumerRequest.objects.all()

        # filter complaint data by nsc category
        if request.GET.get('consumer_category') and request.GET.get('consumer_category') != "All":
            nsc_obj = nsc_obj.filter(consumer_category=request.GET.get('consumer_category'))

        # filter complaint data by nsc sub category
        if request.GET.get('consumer_sub_category') and request.GET.get('consumer_sub_category') != "All":
            nsc_obj = nsc_obj.filter(consumer_subcategory=request.GET.get('consumer_sub_category'))

        # filter complaint data by nsc supply type
        if request.GET.get('supply_type') and request.GET.get('supply_type') != "All":
            nsc_obj = nsc_obj.filter(supply_type=request.GET.get('supply_type'))

        # filter complaint data by nsc status
        if request.GET.get('nsc_status') and request.GET.get('nsc_status') != "All":
            nsc_obj = nsc_obj.filter(status=request.GET.get('nsc_status'))

        # filter complaint data by nsc registration date
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59,
                                                                                          second=59)
            nsc_obj = nsc_obj.filter(date_of_registration__range=[start_date, end_date])

        for nsc in nsc_obj:
            if nsc.closed_date:
                closed_date = nsc.closed_date.strftime('%d/%m/%Y')
            else:
                closed_date = ''
            if nsc.status == 'Registered':
                other_action = '&nbsp;<a title="KYC"> <i class="fa icon-user-following" aria-hidden="true" onclick="KYC_verify(' + str(
                    nsc.id) + ')"></i> </a>'
            elif nsc.status == 'KYC':
                other_action = '&nbsp;<a title="Technical"> <i class="fa icon-wrench" aria-hidden="true" onclick="Technical_verify(' + str(
                    nsc.id) + ')"></i> </a>'
            elif nsc.status == 'Technical':
                other_action = '&nbsp;<a title="Payment"> <i class="fa icon-wallet" aria-hidden="true" onclick="Payment_verify(' + str(
                    nsc.id) + ')"></i> </a>'
            elif nsc.status == 'Payment':
                other_action = '&nbsp;<a title="Meter Details"> <i class="fa icon-user-follow" aria-hidden="true" onclick="consumer_details(' + str(
                    nsc.id) + ')"></i> </a>'
            elif nsc.status == 'Closed':
                other_action = ''
            nsc_data = {
                'registration_id': nsc.registration_no,
                'applicant_name': nsc.applicant_name,
                'aadhar_no': nsc.aadhar_no,
                'contact_no': nsc.meter_mobile_no,
                'category': nsc.consumer_category,
                'sub_category': nsc.consumer_subcategory,
                'supply_type': nsc.supply_type,
                'registration_date': nsc.date_of_registration.strftime('%d/%m/%Y'),
                'status': nsc.status,
                'closed_date': closed_date,
                'actions': '<a class="icon-note" title="Review" href="/nscapp/review-consumer-form/?nsc_id=' + str(
                    nsc.id) + '"></a>&nbsp;' + '&nbsp;<a href="/nscapp/nsc-form/?nsc_id=' + str(
                    nsc.id) + '" target="_blank" class="fa fa-print" title="Print"></a>&nbsp;'
                           + other_action
            }
            nsc_list.append(nsc_data)
        print 'nscapp|views.py|get_nsc_data'
        data = {'data': nsc_list}
    except Exception, e:
        print 'Exception|nscapp|views.py|get_nsc_data', e
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


def review_consumer_form(request):
    try:
        print 'nscapp|views.py|review_consumer_form'
        nsc_id = request.GET.get('nsc_id')
        nsc_obj = NewConsumerRequest.objects.get(id=nsc_id)
        address_document_list = []
        if nsc_obj.address_proof_list:
            address_proof_list = [str(x) for x in eval(nsc_obj.address_proof_list)]
            for address_proof in address_proof_list:
                docs = {
                    'document': address_proof,
                }
                address_document_list.append(docs)

        id_document_list = []
        if nsc_obj.identity_proof_list:
            identity_proof_list = [str(x) for x in eval(nsc_obj.identity_proof_list)]
            for identity_proof in identity_proof_list:
                docs = {
                    'document': identity_proof,
                }
                id_document_list.append(docs)
        data = {
            'consumer_category': nsc_obj.consumer_category,
            'service_requested': nsc_obj.service_requested,
            'supply_type': nsc_obj.supply_type,
            'consumer_sub_category': nsc_obj.consumer_subcategory,
            'registration_number': nsc_obj.registration_no,
            'registration_date': nsc_obj.date_of_registration.strftime('%d/%m/%Y'),
            'applicant_name': nsc_obj.applicant_name,
            'aadhar_number': nsc_obj.aadhar_no,
            'occupation': nsc_obj.occupation,
            'other_details': nsc_obj.other_occupation,
            'house_details': nsc_obj.meter_building_name,
            'address_line_1': nsc_obj.meter_address_line_1,
            'address_line_2': nsc_obj.meter_address_line_2,
            'landmark': nsc_obj.meter_landmark,
            'city': nsc_obj.meter_city,
            'pincode': nsc_obj.meter_pin_code,
            'email_id': nsc_obj.meter_email_id,
            'mobile_no': nsc_obj.meter_mobile_no,
            'phone_no': nsc_obj.meter_phone_no,
            'new_exst_cons_no': nsc_obj.meter_nearest_consumer_no,
            'is_same_address': nsc_obj.is_same_address,
            'billing_house_details': nsc_obj.billing_building_name,
            'billing_address_line_1': nsc_obj.billing_address_line_1,
            'billing_address_line_2': nsc_obj.billing_address_line_2,
            'billing_landmark': nsc_obj.billing_landmark,
            'billing_city': nsc_obj.billing_city,
            'billing_pincode': nsc_obj.billing_pin_code,
            'billing_email_id': nsc_obj.billing_email_id,
            'billing_mobile_no': nsc_obj.billing_mobile_no,
            'billing_phone_no': nsc_obj.billing_phone_no,
            'billing_new_exst_cons_no': nsc_obj.billing_nearest_consumer_no,
            'billing_premises': nsc_obj.type_of_premises,
            'billing_other_details': nsc_obj.other_premises,
            'requested_load': nsc_obj.requested_load,
            'requested_load_type': nsc_obj.requested_load_type,
            'contract_demand': nsc_obj.contarct_demand,
            'contract_demand_type': nsc_obj.contarct_demand_type,
            'address_proof': address_document_list,
            'id_proof': id_document_list,
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|review_consumer_form', e
        data = {}
    return render(request, 'nsc_template/review_consumer_form.html', data)


@csrf_exempt
def save_new_consumer(request):
    try:
        print 'nscapp|views.py|save_new_consumer'
        is_same = request.POST.get('checkbox1_44')
        if is_same == None:
            is_same = 0
        new_consumer_obj = NewConsumerRequest(
            applicant_name=request.POST.get('applicant_name'),
            aadhar_no=request.POST.get('applicant_aadhar_no'),
            occupation=request.POST.get('applicant_occupation'),
            other_occupation=request.POST.get('applicant_other_details'),
            consumer_category=request.POST.get('consumer_category'),
            service_requested=request.POST.get('consumer_service'),
            supply_type=request.POST.get('consumer_supply_type'),
            consumer_subcategory=request.POST.get('consumer_subcategory'),
            registration_no='NSC11110',  # Need to change logic
            date_of_registration=datetime.now(),
            meter_building_name=request.POST.get('flat_no'),
            meter_address_line_1=request.POST.get('address_line1'),
            meter_address_line_2=request.POST.get('address_line2'),
            meter_landmark=request.POST.get('landmark'),

            meter_city=City.objects.get(
                id=request.POST.get('city')) if request.POST.get(
                'city') else None,
            meter_pin_code=Pincode.objects.get(
                id=request.POST.get('pincode')) if request.POST.get(
                'pincode') else None,

            meter_email_id=request.POST.get('email'),
            meter_mobile_no=request.POST.get('mobile'),
            meter_phone_no=request.POST.get('phone_no'),
            meter_nearest_consumer_no=request.POST.get('existing_consumer_no'),
            is_same_address=is_same,
            billing_building_name=request.POST.get('bill_flat_no'),
            billing_address_line_1=request.POST.get('bill_address_line1'),
            billing_address_line_2=request.POST.get('bill_address_line2'),
            billing_landmark=request.POST.get('bill_landmark'),

            billing_city=City.objects.get(
                id=request.POST.get('bill_city')) if request.POST.get(
                'bill_city') else None,
            billing_pin_code=Pincode.objects.get(
                id=request.POST.get('bill_pincode')) if request.POST.get(
                'bill_pincode') else None,

            billing_email_id=request.POST.get('bill_email'),
            billing_mobile_no=request.POST.get('bill_mobile'),
            billing_phone_no=request.POST.get('bill_phone_no'),
            billing_nearest_consumer_no=request.POST.get('bill_existing_consumer_no'),
            type_of_premises=request.POST.get('premises_type'),
            other_premises=request.POST.get('bill_other_data'),
            requested_load=request.POST.get('requested_load'),
            requested_load_type=request.POST.get('load_type'),
            contarct_demand=request.POST.get('contract_demand'),
            contarct_demand_type=request.POST.get('contract_demand_type'),
            address_proof_list=request.POST.getlist('address_proof'),
            identity_proof_list=request.POST.getlist('id_proof'),
            status='Registered',
            created_on=datetime.now(),
            # created_by=request.session['login_user'],
        );
        new_consumer_obj.save();

        attachment_list = request.POST.get('attachments')
        save_attachments(attachment_list, new_consumer_obj)

        data = {
            'success': 'true',
            'message': 'Consumer created successfully.'
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|save_new_consumer', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


from xhtml2pdf import pisa
import cStringIO as StringIO
from cgi import escape
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def nsc_form(request):
    nsc_id = request.GET.get('nsc_id')
    nsc_obj = NewConsumerRequest.objects.get(id=nsc_id)
    address = ''
    billing_address = ''

    address = address + nsc_obj.meter_building_name + ', ' + nsc_obj.meter_address_line_1
    if nsc_obj.meter_address_line_2:
        address = address + ', ' + nsc_obj.meter_address_line_2
    if nsc_obj.meter_landmark:
        address = address + ', ' + nsc_obj.meter_landmark

    billing_address = billing_address + nsc_obj.billing_building_name + ', ' + nsc_obj.billing_address_line_1
    if nsc_obj.billing_address_line_2:
        billing_address = billing_address + ', ' + nsc_obj.billing_address_line_2
    if nsc_obj.billing_landmark:
        billing_address = address + ', ' + nsc_obj.billing_landmark

    document_list = []
    if nsc_obj.address_proof_list:
        address_proof_list = [str(x) for x in eval(nsc_obj.address_proof_list)]
        for address_proof in address_proof_list:
            docs = {
                'document': address_proof,
            }
            document_list.append(docs)

    if nsc_obj.identity_proof_list:
        identity_proof_list = [str(x) for x in eval(nsc_obj.identity_proof_list)]
        for identity_proof in identity_proof_list:
            docs = {
                'document': identity_proof,
            }
            document_list.append(docs)

    data = {
        'consumer_category': nsc_obj.consumer_category,
        'service_requested': nsc_obj.service_requested,
        'supply_type': nsc_obj.supply_type,
        'consumer_sub_category': nsc_obj.consumer_subcategory,
        'registration_number': nsc_obj.registration_no,
        'registration_date': nsc_obj.date_of_registration.strftime('%d/%m/%Y'),
        'applicant_name': nsc_obj.applicant_name,
        'aadhar_number': nsc_obj.aadhar_no,
        'occupation': nsc_obj.occupation,
        'other_details': nsc_obj.other_occupation,
        'address': address,
        'city': nsc_obj.meter_city.city,
        'pincode': nsc_obj.meter_pin_code.pincode,
        'email_id': nsc_obj.meter_email_id,
        'mobile_no': nsc_obj.meter_mobile_no,
        'phone_no': nsc_obj.meter_phone_no,
        'new_exst_cons_no': nsc_obj.meter_nearest_consumer_no,
        'billing_address': billing_address,
        'billing_city': nsc_obj.billing_city.city,
        'billing_pincode': nsc_obj.billing_pin_code.pincode,
        'billing_email_id': nsc_obj.billing_email_id,
        'billing_mobile_no': nsc_obj.billing_mobile_no,
        'billing_phone_no': nsc_obj.billing_phone_no,
        'billing_new_exst_cons_no': nsc_obj.billing_nearest_consumer_no,
        'billing_premises': nsc_obj.type_of_premises,
        'billing_other_details': nsc_obj.other_premises,
        'requested_load': nsc_obj.requested_load,
        'requested_load_type': nsc_obj.requested_load_type,
        'contract_demand': nsc_obj.contarct_demand,
        'contract_demand_type': nsc_obj.contarct_demand_type,
        'document_list': document_list
    }
    template = get_template('nsc_template/nsc_form.html')
    html = template.render(Context(data))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


@csrf_exempt
def upload_consumer_docs(request):
    try:
        print 'nscapp|views.py|upload_consumer_docs'
        if request.method == 'POST':
            attachment_file = ConsumerDocsImage()
            attachment_file.save()

            request.FILES['file[]'].name = 'consumerDocsID_' + str(attachment_file.id) + '_' + request.FILES[
                'file[]'].name
            attachment_file.document_files = request.FILES['file[]']
            attachment_file.save()
            data = {'success': 'true', 'attachid': attachment_file.id}
        else:
            data = {'success': 'false'}
    except MySQLdb.OperationalError, e:
        print 'Exception|nscapp|views.py|upload_consumer_docs', e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def remove_consumer_docs(request):
    try:
        print 'nscapp|views.py|remove_consumer_docs'
        image_id = request.GET.get('image_id')
        image = ConsumerDocsImage.objects.get(id=image_id)
        image.delete()

        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        print 'Exception|nscapp|views.py|remove_consumer_docs', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_attachments(attachment_list, consumer_id):
    try:
        print 'nscapp|views.py|save_attachments'
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        for attached_id in attachment_list:
            attachment_obj = ConsumerDocsImage.objects.get(id=attached_id)
            attachment_obj.consumer_id = consumer_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception|nscapp|views.py|save_attachments', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_verification_data(request):
    try:
        print 'nscapp|views.py|get_verification_data'
        data = {}
        final_list = []
        try:
            consumer_obj = NewConsumerRequest.objects.get(id=request.GET.get('registration_id'))
            meter_address_line_1 = consumer_obj.meter_address_line_1
            meter_address_line_2 = consumer_obj.meter_address_line_2
            if meter_address_line_2:
                address = meter_address_line_1 + ', ' + meter_address_line_2
            else:
                address = meter_address_line_1

            consumer_data = {
                'consumer_id': consumer_obj.id,
                'registration_no': consumer_obj.registration_no,
                'applicant_name': consumer_obj.applicant_name,
                'meter_mobile_no': consumer_obj.meter_mobile_no,
                'address': address,
                'consumer_category': consumer_obj.consumer_category,
                'consumer_subcategory': consumer_obj.consumer_subcategory,
                'supply_type': consumer_obj.supply_type,
                'type_of_premises': consumer_obj.type_of_premises,
                'pincode': str(consumer_obj.meter_pin_code.pincode),
                'city_name': str(consumer_obj.meter_city.city),
                'meter_email_id': consumer_obj.meter_email_id
            }

            data = {'success': 'true', 'data': consumer_data}
        except Exception as e:
            print 'Exception|nscapp|views.py|get_verification_data', e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|nscapp|views.py|get_verification_data', e
    except Exception, e:
        print 'Exception|nscapp|views.py|get_verification_data', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_consumer_kyc(request):
    try:
        print 'nscapp|views.py|save_consumer_kyc'
        new_KYC_obj = KycVerification(
            consumer_id=NewConsumerRequest.objects.get(
                id=request.POST.get('consumer_id')) if request.POST.get(
                'consumer_id') else None,
            status=request.POST.get('verify_KYC_status'),
            remark=request.POST.get('KYC_remark'),
            creation_date=datetime.now(),
            # created_by=request.session['login_user'],
        );
        new_KYC_obj.save();

        consumer_obj = NewConsumerRequest.objects.get(id=request.POST.get('consumer_id'))
        consumer_obj.status = 'KYC'
        consumer_obj.save();

        data = {
            'success': 'true',
            'message': 'KYC created successfully.'
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|save_consumer_kyc', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_consumer_technical(request):
    try:
        print 'nscapp|views.py|save_consumer_technical'
        checkbox1_1 = False
        checkbox1_2 = False
        checkbox1_3 = False
        checkbox1_4 = False
        if request.POST.get('checkbox1_1'):
            checkbox1_1 = True
        if request.POST.get('checkbox1_2'):
            checkbox1_2 = True
        if request.POST.get('checkbox1_3'):
            checkbox1_3 = True
        if request.POST.get('checkbox1_4'):
            checkbox1_4 = True

        new_Technical_obj = TechnicalVerification(
            consumer_id=NewConsumerRequest.objects.get(
                id=request.POST.get('tech_consumerid')) if request.POST.get(
                'tech_consumerid') else None,
            checkbox=request.POST.getlist('Checklist'),
            technician_mobile_no=request.POST.get('tech_contact_no'),
            status=request.POST.get('verify_technical'),
            remark=request.POST.get('tech_remark'),
            technician_name=request.POST.get('technician_name'),
            creation_date=datetime.now(),
            # created_by=request.session['login_user'],
        );
        new_Technical_obj.save();

        consumer_obj = NewConsumerRequest.objects.get(id=request.POST.get('tech_consumerid'))
        consumer_obj.status = 'Technical'
        consumer_obj.save();

        data = {
            'success': 'true',
            'message': 'Technical created successfully.'
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|save_consumer_technical', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_consumer_payment(request):
    try:
        print 'nscapp|views.py|save_consumer_payment', request.POST.get('pay_amount_paid')

        new_Payment_obj = PaymentVerification(
            consumer_id=NewConsumerRequest.objects.get(
                id=request.POST.get('pay_consumerid')) if request.POST.get(
                'pay_consumerid') else None,
            amount_paid=request.POST.get('pay_amount_paid'),
            payment_mode=request.POST.get('payment_mode'),
            cheque_no=request.POST.get('pay_cheque_no'),
            name_on_cheque=request.POST.get('pay_cheque_name'),
            DD_no=request.POST.get('pay_DD_no'),
            DD=request.POST.get('pay_DD'),
            creation_date=datetime.now(),
            # created_by=request.session['login_user'],
        );
        new_Payment_obj.save();

        consumer_obj = NewConsumerRequest.objects.get(id=request.POST.get('pay_consumerid'))
        consumer_obj.status = 'Payment'
        consumer_obj.save();

        new_Consumer_obj = ConsumerDetails(
            consumer_id=NewConsumerRequest.objects.get(
                id=request.POST.get('pay_consumerid')) if request.POST.get(
                'pay_consumerid') else None,
            name=consumer_obj.applicant_name,
            email_id=consumer_obj.meter_email_id,
            contact_no=consumer_obj.meter_mobile_no,
            address_line_1=consumer_obj.meter_address_line_1,
            address_line_2=consumer_obj.meter_address_line_2,
            consumer_no='CONS123456',

            city=City.objects.get(
                id=consumer_obj.meter_city.id) if consumer_obj.meter_city.id else None,
            pin_code=Pincode.objects.get(
                id=consumer_obj.meter_pin_code.id) if consumer_obj.meter_pin_code.id else None,

            aadhar_no=consumer_obj.aadhar_no,
            created_on=datetime.now(),
            # created_by=request.session['login_user'],
        );
        new_Consumer_obj.save();

        data = {
            'success': 'true',
            'message': 'Payment created successfully.'
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|save_consumer_payment', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_consumer_data(request):
    try:
        nsc_id = request.GET.get('registration_id')
        nsc_obj = NewConsumerRequest.objects.get(id=nsc_id)
        consumer_obj = ConsumerDetails.objects.get(consumer_id=nsc_id)
        address = ''
        address = address + nsc_obj.meter_building_name + ', ' + nsc_obj.meter_address_line_1
        if nsc_obj.meter_address_line_2:
            address = address + ', ' + nsc_obj.meter_address_line_2
        if nsc_obj.meter_landmark:
            address = address + ', ' + nsc_obj.meter_landmark
        if nsc_obj.meter_city:
            address = address + ', ' + nsc_obj.meter_city.city
        if nsc_obj.meter_pin_code.pincode:
            address = address + ' - ' + nsc_obj.meter_pin_code.pincode + '.'

        data = {
            'consumer_no': consumer_obj.consumer_no,
            'consumer_id': str(nsc_obj.id),
            'consumer_category': nsc_obj.consumer_category,
            'supply_type': nsc_obj.supply_type,
            'consumer_sub_category': nsc_obj.consumer_subcategory,
            'registration_number': nsc_obj.registration_no,
            'applicant_name': nsc_obj.applicant_name,
            'address': address,
            'mobile_no': nsc_obj.meter_mobile_no,
            'phone_no': nsc_obj.meter_phone_no,
            'success': 'true'
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|save_consumer_payment', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_meter_details(request):
    try:
        print 'nscapp|views.py|save_meter_details', request.POST

        route_obj = RouteDetail.objects.get(id=request.POST.get('meter_route'))
        bill_cycle_obj = BillCycle.objects.get(id=route_obj.billcycle.id)
        zone_obj = Zone.objects.get(id=bill_cycle_obj.zone.id)
        branch_obj = Branch.objects.get(id=zone_obj.branch.id)
        consumer_obj = NewConsumerRequest.objects.get(id=request.POST.get('consumer_id'))

        new_Consumer_obj = ConsumerDetails.objects.get(consumer_id=request.POST.get('consumer_id'))
        new_Consumer_obj.route = route_obj
        new_Consumer_obj.bill_cycle = bill_cycle_obj
        new_Consumer_obj.zone = zone_obj
        new_Consumer_obj.branch = branch_obj
        new_Consumer_obj.meter_no = request.POST.get('meter_no')
        new_Consumer_obj.meter_category = consumer_obj.consumer_category
        new_Consumer_obj.meter_connection_date = datetime.strptime(request.POST.get('meter_date'), '%d/%m/%Y')
        new_Consumer_obj.meter_digit = request.POST.get('meter_digit')
        new_Consumer_obj.meter_phase = consumer_obj.supply_type
        new_Consumer_obj.meter_make = request.POST.get('meter_make')
        new_Consumer_obj.meter_type = request.POST.get('meter_type')

        if request.POST.get('meter_status') == "Done":
            new_Consumer_obj.connection_status = 'Connected'

        new_Consumer_obj.save()
        consumer_obj.status = 'Closed'
        consumer_obj.save()

        data = {
            'success': 'true',
            'message': 'Meter details saved successfully.'
        }
    except Exception, e:
        print 'Exception|nscapp|views.py|save_meter_details', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')
