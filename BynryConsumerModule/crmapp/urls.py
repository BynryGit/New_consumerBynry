__author__ = 'Swapnil Kadu'
from crmapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.home, name='login'),
    url(r'^verify-new-consumer/', views.verify_new_consumer, name='verify_new_consumer'),
    url(r'^save-new-consumer/', views.save_new_consumer, name='save_new_consumer'),
    url(r'^complaints/', views.complaints, name='complaints'),
    url(r'^get-consumer-complaints/', views.get_consumer_complaints, name='get_consumer_complaints'),
    url(r'^get-complaint-details/', views.get_complaint_details, name='get_complaint_details'),
    url(r'^save-complaint-details/', views.save_complaint_details, name='save_complaint_details'),
    url(r'^services/', views.services, name='services'),
    url(r'^service-request/', views.service_request, name='service_request'),
    url(r'^vigilance/', views.vigilance, name='vigilance'),
    url(r'^save-vigilance-complaint/', views.save_vigilance_complaint, name='save_vigilance_complaint'),
    url(r'^bills/', views.bills, name='bills'),
    url(r'^get-bill-history/', views.get_bill_history, name='get_bill_history'),
    url(r'^view-bill/', views.view_bill, name='view_bill'),
]
