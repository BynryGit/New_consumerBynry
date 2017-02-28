from django.contrib import admin
import models
# Register your models here.
class ConsumerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'consumer_no', 'parent', 'meter_no', 'bill_cycle', 'is_active', 'is_deleted')
    search_fields = ('id', 'name', 'consumer_no')
    list_filter = ('is_new', 'is_parent', 'is_active', 'is_deleted')

class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_id', 'consumer_id', 'bill_month', 'unit_consumed', 'bill_amount_paid', 'payment_date', 'payment_by')
    search_fields = ('id', 'transaction_id', 'consumer_id')
    list_filter = ('bill_month', 'payment_by', 'is_deleted')


admin.site.register(models.ConsumerDetails,ConsumerDetailsAdmin)
admin.site.register(models.PaymentDetail,PaymentDetailAdmin)