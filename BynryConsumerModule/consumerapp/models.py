import django
from django.db import models
from decimal import Decimal
from datetime import date

from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail


IS_DELETED = (
    (True, True),
    (False, False),
)

ROLE_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

class ConsumerDetails(models.Model):
    name = models.CharField(max_length=200, blank=False, null=True)
    consumer_no = models.CharField(max_length=200, blank=False, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    email_id = models.CharField(max_length=50, blank=True, null=True)
    contact_no = models.CharField(max_length=50, blank=True, null=True)

    address_line_1 = models.CharField(max_length=500, blank=True, null=True)
    address_line_2 = models.CharField(max_length=500, blank=True, null=True)
    address_line_3 = models.CharField(max_length=500, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.ForeignKey(City, blank=False, null=True)
    bill_cycle = models.ForeignKey(BillCycle, blank=True, null=True)
    feeder_code = models.CharField(max_length=20, blank=True, null=True)
    feeder_name = models.CharField(max_length=255, blank=True, null=True)

    meter_no = models.CharField(max_length=30, blank=True, null=True)
    dtc = models.CharField(max_length=30, blank=True, null=False)
    dtc_dec = models.CharField(max_length=255, blank=True, null=True)
    pole_no = models.CharField(max_length=30, blank=True, null=True)

    meter_digit = models.CharField(max_length=5, blank=True, null=True)
    meter_phase = models.CharField(max_length=100, blank=True, null=True)
    meter_make = models.CharField(max_length=100, blank=True, null=True)
    meter_type = models.CharField(max_length=100, blank=True, null=True)
    connection_status = models.CharField(max_length=100, blank=True, null=True)

    alternate_mobile =models.CharField(max_length=15,null=True,blank=True)
    alternate_email=models.CharField(max_length=100,null=True,blank=True)
    B_U = models.CharField(max_length=20, blank=True, null=True)
    P_C = models.CharField(max_length=20, blank=True, null=True)

    nearest_pole_no = models.CharField(max_length=200, blank=True, null=True)
    nearest_consumer_no = models.CharField(max_length=200, blank=True, null=True)

    register_date = models.DateField(default=django.utils.timezone.now)

    is_new = models.BooleanField(default=False)
    is_parent = models.BooleanField(choices=IS_DELETED, default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    created_by = models.CharField(max_length=500, blank=False, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.name)+'-'+str(self.consumer_no))
