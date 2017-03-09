from django.db import models
import django
from decimal import Decimal
from datetime import date

from consumerapp.models import ConsumerDetails,MeterReadingDetail

# Create your models here.

class PaymentDetail(models.Model):
    PAYMENT_MODE = (
        ('Online Payment', 'Online Payment'),
        ('Paytm Wallet', 'Paytm Wallet'),
        ('Cash Payment', 'Cash Payment'),
    )

    PAYMENT_BY=(
        ('Register Consumer', 'Register Consumer'),
        ('Quick Pay', 'Quick Pay'),
    )

    BILL_STATUS=(
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )

    IS_DELETED = (
        (True, True),
        (False, False),
    )

    consumer_id = models.ForeignKey(ConsumerDetails, blank=True, null=True)
    transaction_id = models.CharField(max_length=50, blank=False, null=True)
    meter_reading_id= models.ForeignKey(MeterReadingDetail, blank=False)
    # bill_month = models.CharField(max_length=20, blank=False, null=True)
    # bill_months_year = models.CharField(max_length=20, blank=False, null=True)
    # unit_consumed = models.CharField(max_length=100, blank=False, null=True)
    # current_month_reading = models.CharField(max_length=100, blank=False, null=True)
    # previous_month_reading = models.CharField(max_length=100, blank=False, null=True)
    current_amount = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    tariff_rate = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    net_amount = models.CharField(max_length=100, blank=True, null=True)
    bill_amount = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    bill_amount_paid = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    due_amount = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    arriers =models.DecimalField(max_digits=8, decimal_places=2,default=Decimal(0.00))
    payment_date = models.DateField(blank=True, null=True)
    prompt_date = models.DateField(blank=True, null=True)
    due_date =models.DateField(blank=True, null=True)
    payment_mode=models.CharField(max_length=200, choices=PAYMENT_MODE,blank=True, null=True)
    payment_by=models.CharField(max_length=200, choices=PAYMENT_BY,default='Register Consumer')
    bill_status=models.CharField(max_length=200, choices=BILL_STATUS,default='')
    created_by = models.CharField(max_length=500, blank=False, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
     return unicode(self.id)
