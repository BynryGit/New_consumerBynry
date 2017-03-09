import django
from django.db import models
from decimal import Decimal
from datetime import date

from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail, Pincode, Zone, Utility


IS_DELETED = (
    (True, True),
    (False, False),
)

CONNECTION_STATUS = (
    ('Connected', 'Connected'),
    ('Disconnected', 'Disconnected'),
)
METER_CATEGORY = (
    ('HT', 'HT'),
    ('LT', 'LT'),
)


class ConsumerDetails(models.Model):
    name            = models.CharField(max_length=200, blank=False, null=True)
    consumer_no     = models.CharField(max_length=200, blank=False, null=True)
    email_id        = models.CharField(max_length=50, blank=True, null=True)
    contact_no      = models.CharField(max_length=50, blank=True, null=True)
    address_line_1  = models.CharField(max_length=500, blank=True, null=True)
    address_line_2  = models.CharField(max_length=500, blank=True, null=True)
    city            = models.ForeignKey(City, blank=False, null=True)
    pin_code        = models.ForeignKey(Pincode, blank=False, null=True)
    zone            = models.ForeignKey(Zone, blank=False, null=True)
    bill_cycle      = models.ForeignKey(BillCycle, blank=True, null=True)
    route           = models.ForeignKey(RouteDetail, blank=True, null=True)
    feeder_code     = models.CharField(max_length=20, blank=True, null=True)
    feeder_name     = models.CharField(max_length=255, blank=True, null=True)
    meter_no        = models.CharField(max_length=30, blank=True, null=True)
    aadhar_no       = models.CharField(max_length=30, blank=True, null=True)
    sanction_load   = models.CharField(max_length=30, blank=True, null=True)
    meter_category  = models.CharField(max_length=200, choices=METER_CATEGORY,default='HT')
    consumer_age    = models.CharField(max_length=5, blank=True, null=True)
    Utility         = models.ForeignKey(Utility, blank=False, null=True)
    dtc             = models.CharField(max_length=30, blank=True, null=False)
    dtc_dec         = models.CharField(max_length=255, blank=True, null=True)
    pole_no         = models.CharField(max_length=30, blank=True, null=True)
    meter_digit     = models.CharField(max_length=5, blank=True, null=True)
    meter_phase     = models.CharField(max_length=100, blank=True, null=True)
    meter_make      = models.CharField(max_length=100, blank=True, null=True)
    meter_type      = models.CharField(max_length=100, blank=True, null=True)
    connection_status = models.CharField(max_length=200, choices=CONNECTION_STATUS,default='Connected')
    alternate_mobile=models.CharField(max_length=15,null=True,blank=True)
    alternate_email =models.CharField(max_length=100,null=True,blank=True)
    nearest_pole_no = models.CharField(max_length=200, blank=True, null=True)
    nearest_consumer_no = models.CharField(max_length=200, blank=True, null=True)
    register_date   = models.DateField(default=django.utils.timezone.now)
    is_new          = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_deleted      = models.BooleanField(choices=IS_DELETED, default=False)
    created_by      = models.CharField(max_length=500, blank=False, null=True)
    updated_by      = models.CharField(max_length=500, blank=True, null=True)
    created_on      = models.DateTimeField(default=django.utils.timezone.now)
    updated_on      = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.consumer_no))

class MeterReadingDetail(models.Model):
    consumer_id= models.ForeignKey(ConsumerDetails, blank=False)
    bill_month = models.CharField(max_length=20, blank=False, null=True)
    bill_months_year = models.CharField(max_length=20, blank=False, null=True)
    unit_consumed = models.CharField(max_length=100, blank=False, null=True)
    current_month_reading = models.CharField(max_length=100, blank=False, null=True)
    previous_month_reading = models.CharField(max_length=100, blank=False, null=True)
    current_reading_date = models.DateField(blank=True, null=True)
    previous_month_reading_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=500, blank=False, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
     return unicode(self.id)