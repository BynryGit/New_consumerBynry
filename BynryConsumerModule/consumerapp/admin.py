from django.contrib import admin
import models
# Register your models here.
class ConsumerDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'consumer_no', 'meter_no', 'bill_cycle', 'is_active', 'is_deleted')
    search_fields = ('name', 'consumer_no')
    list_filter = ('is_new', 'is_active', 'is_deleted')

admin.site.register(models.ConsumerDetails,ConsumerDetailsAdmin)
admin.site.register(models.MeterReadingDetail)