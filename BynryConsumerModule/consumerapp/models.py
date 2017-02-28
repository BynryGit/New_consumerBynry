import django
from django.db import models
from decimal import Decimal
from datetime import date

from adminapp.models import City, BillCycle, RouteDetail


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


class PaymentDetail(models.Model):
    PAYMENT_MODE = (
        ('Paid By Cash', 'Paid By Cash'),
        ('Paid By Card', 'Paid By Card'),
    )

    PAYMENT_BY=(
        ('Register Consumer', 'Register Consumer'),
        ('Quick Pay', 'Quick Pay'),
    )
    consumer_id = models.ForeignKey(ConsumerDetails, blank=True, null=True)
    transaction_id = models.CharField(max_length=50, blank=False, null=True)
    bill_month = models.CharField(max_length=20, blank=False, null=True)
    unit_consumed = models.CharField(max_length=100, blank=False, null=True)
    current_amount = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    net_amount = models.CharField(max_length=100, blank=True, null=True)
    bill_amount_paid = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    due_amount = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    arriers =models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    payment_date = models.DateField(blank=True, null=True)
    due_date =models.DateField(blank=True, null=True)
    payment_mode=models.CharField(max_length=200, choices=PAYMENT_MODE,blank=True, null=True)
    payment_by=models.CharField(max_length=200, choices=PAYMENT_BY,default='Register Consumer')
    created_by = models.CharField(max_length=500, blank=False, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
     return unicode(self.payment_by)
