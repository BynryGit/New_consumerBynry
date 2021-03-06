from django.contrib import admin
import models
# Register your models here.

class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_id', 'consumer_id', 'bill_amount_paid', 'created_on', 'payment_by')
    search_fields = ('id', 'transaction_id', 'consumer_id')
    list_filter = ('payment_by', 'is_deleted')

admin.site.register(models.PaymentDetail,PaymentDetailAdmin)