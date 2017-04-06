from django.contrib import admin
import models
# Register your models here.

admin.site.register(models.VigilanceType)
admin.site.register(models.VigilanceDetail)
admin.site.register(models.VigilancePenalyDetail)
admin.site.register(models.CourtCaseDetail)
#admin.site.register(models.ConsumerVigilanceImage)