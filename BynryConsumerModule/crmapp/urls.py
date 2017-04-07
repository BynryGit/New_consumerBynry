__author__ = 'Swapnil Kadu'
from crmapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.home, name='login'),
    url(r'^verify-new-consumer/', views.verify_new_consumer, name='verify_new_consumer'),
    url(r'^save-new-consumer/', views.save_new_consumer, name='save_new_consumer'),
]
