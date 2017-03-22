from django.contrib import admin
import models

admin.site.register(models.NewConsumerRequest)
admin.site.register(models.ConsumerDocsImage)
admin.site.register(models.KycVerification)
admin.site.register(models.TechnicalVerification)
admin.site.register(models.PaymentVerification)
