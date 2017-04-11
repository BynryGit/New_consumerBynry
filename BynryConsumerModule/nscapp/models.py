import django
from django.db import models
from decimal import Decimal
from datetime import date

from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Pincode, Zone, Utility
# Create your models here.
CONSUMER_DOCS_PATH ='images/consumer_docs_file/'

CONSUMER_CATEGORY = (
    ('1-LT-SUPPLY', '1-LT-SUPPLY'),
    ('2-HT-SUPPLY', '2-HT-SUPPLY'),
    ('3-EHV', '3-EHV'),
)
SERVICE_REQUESTED = (
    ('001-New-Connection (Permanent)', '001-New-Connection (Permanent)'),
    ('002-New-Connection (Temporary)', '002-New-Connection (Temporary)'),
)
SUPPLY_TYPE = (
    ('SINGLE-SINGLE-PHASE', 'SINGLE-SINGLE-PHASE'),
    ('THREE-THREE-PHASE', 'THREE-THREE-PHASE'),
    ('HT-HT-SUPPLY', 'HT-HT-SUPPLY'),
)
CONSUMER_SUBCATEGORY = (
    ('30-PWW', '30-PWW'),
    ('40-Residential', '40-Residential'),
    ('50-Commercial', '50-Commercial'),
    ('60-LT industrial', '60-LT industrial'),
    ('70-LT powerloom', '70-LT powerloom'),
    ('80-Street Light', '80-Street Light'),
    ('90-Agriculture', '90-Agriculture'),
    ('91-LT poultry', '91-LT poultry'),
    ('92-LT Advertisement and Hoarding', '92-LT Advertisement and Hoarding'),
    ('93-LT Precooling', '93-LT Precooling'),
    ('94-LT temporary Religious', '94-LT temporary Religious'),
    ('95-LT temporary others', '95-LT temporary others'),
    ('165-Temp-Construction', '165-Temp-Construction'),
    ('166-Crematorium And Burial', '166-Crematorium And Burial'),
    ('167-Public Services', '167-Public Services'),
    ('207-LT IV A AG ZONE 1', '207-LT IV A AG ZONE 1'),
    ('209-LT IV A AG ZONE 2', '209-LT IV A AG ZONE 2'),

)
PREMISES_TYPE = (
    ('1-OWNED', '1-OWNED'),
    ('2-RENTED', '2-RENTED'),
    ('3-LEASE', '3-LEASE'),
    ('4-LIS/OTHERS', '4-LIS/OTHERS'),
)
REQUESTED_LOAD_TYPE = (
    ('KW', 'KW'),
    ('HP', 'HP'),
)
CONTRACT_DEMAND_TYPE = (
    ('KWA', 'KWA'),
)
IS_DELETED = (
    (True, True),
    (False, False),
)
OCCUPATION = (
    ('SERVICES', 'SERVICES'),
    ('PROFESSION/BUSINESS', 'PROFESSION/BUSINESS'),
    ('OTHERS', 'OTHERS'),
)
NSC_STATUS = (
    ('Registered', 'Registered'),
    ('KYC', 'KYC'),
    ('KYC Rejected', 'KYC Rejected'),
    ('Technical', 'Technical'),
    ('Technical Rejected', 'Technical Rejected'),
    ('Payment', 'Payment'),
    ('Closed', 'Closed'),
)
KYC_STATUS = (
    ('Verified', 'Verified'),
    ('Rejected', 'Rejected'),
)
TECHNICAL_STATUS = (
    ('Pass', 'Pass'),
    ('Failed', 'Failed'),
)  
PAYMENT_MODE = (
    ('Cheque', 'Cheque'),
    ('DD', 'DD'),
)

class NewConsumerRequest(models.Model):
    applicant_name = models.CharField(max_length=200, blank=False, null=True)
    aadhar_no = models.CharField(max_length=20, blank=False, null=True)
    occupation = models.CharField(max_length=200, choices=OCCUPATION, default='1-LT-SUPPLY')
    other_occupation = models.CharField(max_length=100, blank=False, null=True)
    consumer_category = models.CharField(max_length=200, choices=CONSUMER_CATEGORY, default='1-LT-SUPPLY')
    service_requested = models.CharField(max_length=200, choices=SERVICE_REQUESTED,
                                         default='001-New-Connection (Permanent)')
    supply_type = models.CharField(max_length=200, choices=SUPPLY_TYPE, default='SINGLE-SINGLE-PHASE')
    consumer_subcategory = models.CharField(max_length=200, choices=CONSUMER_SUBCATEGORY, default='30-PWW')
    registration_no = models.CharField(max_length=100, blank=True, null=True)
    date_of_registration = models.DateTimeField(blank=True, null=True)
    meter_building_name = models.CharField(max_length=200, blank=False, null=True)
    meter_address_line_1 = models.CharField(max_length=500, blank=True, null=True)
    meter_address_line_2 = models.CharField(max_length=500, blank=True, null=True)
    meter_landmark = models.CharField(max_length=500, blank=True, null=True)
    meter_city = models.ForeignKey(City, blank=False, null=True, related_name='meter_city')
    meter_pin_code = models.ForeignKey(Pincode, blank=False, null=True, related_name='meter_pincode')
    meter_email_id = models.CharField(max_length=50, blank=True, null=True)
    meter_mobile_no = models.CharField(max_length=50, blank=True, null=True)
    meter_phone_no = models.CharField(max_length=50, blank=True, null=True)
    meter_nearest_consumer_no = models.CharField(max_length=50, blank=True, null=True)
    is_same_address = models.BooleanField(default=True)
    billing_building_name = models.CharField(max_length=200, blank=False, null=True)
    billing_address_line_1 = models.CharField(max_length=500, blank=True, null=True)
    billing_address_line_2 = models.CharField(max_length=500, blank=True, null=True)
    billing_landmark = models.CharField(max_length=500, blank=True, null=True)
    billing_city = models.ForeignKey(City, blank=False, null=True)
    billing_pin_code = models.ForeignKey(Pincode, blank=False, null=True)
    billing_email_id = models.CharField(max_length=50, blank=True, null=True)
    billing_mobile_no = models.CharField(max_length=50, blank=True, null=True)
    billing_phone_no = models.CharField(max_length=50, blank=True, null=True)
    billing_nearest_consumer_no = models.CharField(max_length=50, blank=True, null=True)
    type_of_premises = models.CharField(max_length=200, choices=PREMISES_TYPE, default='1-OWNED')
    other_premises = models.CharField(max_length=100, blank=True, null=True)
    requested_load = models.CharField(max_length=100, blank=True, null=True)
    requested_load_type = models.CharField(max_length=200, choices=REQUESTED_LOAD_TYPE, default='1-LT-SUPPLY')
    contarct_demand = models.CharField(max_length=100, blank=True, null=True)
    contarct_demand_type = models.CharField(max_length=200, choices=CONTRACT_DEMAND_TYPE, default='1-LT-SUPPLY')
    address_proof_list = models.CharField(max_length=2000, blank=True, null=True)
    identity_proof_list = models.CharField(max_length=2000, blank=True, null=True)
    
    status = models.CharField(max_length=200, choices=NSC_STATUS)
    closed_date = models.DateTimeField(blank=True, null=True)
    is_new = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    created_by = models.CharField(max_length=500, blank=False, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.registration_no))

class ConsumerDocsImage(models.Model):
    consumer_id		= models.ForeignKey(NewConsumerRequest,blank=True,null=True)
    document_files 	= models.FileField(upload_to=CONSUMER_DOCS_PATH, max_length=500, null=True, blank=True)
    creation_date 	= models.DateTimeField(null=True,blank=True)
    created_by 		= models.CharField(max_length=500,null=True,blank=True)
    updated_by 		= models.CharField(max_length=500,null=True,blank= True)
    updation_date	= models.DateTimeField(null=True,blank=True)
    
    def __unicode__(self):
        return unicode(self.id) 

class KycVerification(models.Model):
    consumer_id     = models.ForeignKey(NewConsumerRequest,blank=True,null=True)
    status          = models.CharField(max_length=200, choices=KYC_STATUS, default='NotVerified')
    remark          = models.CharField(max_length=500, blank=True, null=True)
    creation_date   = models.DateTimeField(null=True,blank=True)
    created_by      = models.CharField(max_length=500,null=True,blank=True)
    updated_by      = models.CharField(max_length=500,null=True,blank= True)
    updation_date   = models.DateTimeField(null=True,blank=True)
    
    def __unicode__(self):
        return unicode(self.id) 

class TechnicalVerification(models.Model):
    consumer_id = models.ForeignKey(NewConsumerRequest,blank=True,null=True)
    checkbox = models.CharField(max_length=2000, blank=True, null=True)
    technician_name = models.CharField(max_length=200, blank=False, null=True)
    technician_mobile_no = models.CharField(max_length=50, blank=True, null=True)
    status          = models.CharField(max_length=200, choices=TECHNICAL_STATUS, default='Failed')
    remark          = models.CharField(max_length=500, blank=True, null=True)
    creation_date   = models.DateTimeField(null=True,blank=True)
    created_by      = models.CharField(max_length=500,null=True,blank=True)
    updated_by      = models.CharField(max_length=500,null=True,blank= True)
    updation_date   = models.DateTimeField(null=True,blank=True)
    
    def __unicode__(self):
        return unicode(self.id)     

class PaymentVerification(models.Model):
    consumer_id = models.ForeignKey(NewConsumerRequest,blank=True,null=True)
    amount_paid = models.CharField(max_length=200, blank=False, null=True)
    payment_mode = models.CharField(max_length=200, choices=PAYMENT_MODE, default='Cheque')
    cheque_no = models.CharField(max_length=50, blank=True, null=True)
    name_on_cheque = models.CharField(max_length=100, blank=True, null=True)
    DD_no = models.CharField(max_length=50, blank=True, null=True)
    DD = models.CharField(max_length=50, blank=True, null=True)
    creation_date   = models.DateTimeField(null=True,blank=True)
    created_by      = models.CharField(max_length=500,null=True,blank=True)
    updated_by      = models.CharField(max_length=500,null=True,blank= True)
    updation_date   = models.DateTimeField(null=True,blank=True)
    
    def __unicode__(self):
        return unicode(self.id)                            

