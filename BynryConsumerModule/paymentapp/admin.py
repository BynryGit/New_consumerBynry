from django.contrib import admin
import models
# Register your models here.

class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_id', 'consumer_id', 'bill_month', 'unit_consumed', 'bill_amount_paid', 'payment_date', 'payment_by')
    search_fields = ('id', 'transaction_id', 'consumer_id')
    list_filter = ('bill_month', 'payment_by', 'is_deleted')

admin.site.register(models.PaymentDetail,PaymentDetailAdmin)