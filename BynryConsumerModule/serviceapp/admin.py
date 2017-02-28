from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.ServiceRequestType)
admin.site.register(models.ServiceRequest)
admin.site.register(models.ServiceRequestSubType)


