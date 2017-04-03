__author__ = 'Vikas Kumawat'
from selfserviceapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.log_in, name='login'),
    url(r'^log-in/',views.signin,name='signin'),
    url(r'^index/', views.home_screen, name='home_screen'),
    url(r'^register-new-user/', views.register_new_user, name='register_new_user'),
    url(r'^my-bills/', views.my_bills, name='my_bills'),
    url(r'^get-graph1-data/', views.get_graph1_data,name='get_graph1_data'),
    url(r'^get-graph2-data/', views.get_graph2_data,name='get_graph2_data'),
    url(r'^get-bill-history/', views.get_bill_history,name='get_bill_history'),
    url(r'^manage-accounts/', views.manage_accounts, name='manage_accounts'),
    url(r'^add-new-account/', views.add_new_account, name='add_new_account'),
    url(r'^complaints/', views.complaints, name='complaints'),
    url(r'^services/', views.services, name='services'),
    url(r'^service-request/', views.service_request, name='service_request'),
    url(r'^vigilance/', views.vigilance, name='vigilance'),
    url(r'^contact-us/', views.contact_us, name='contact_us'),
    # url(r'^my-bills/', views.my_bills, name='my_bills'),
    url(r'^quick-pay/', views.quick_pay, name='quick_pay'),
    url(r'^my-tariff/', views.my_tariff, name='my_tariff'),
    url(r'^get-consumer-bill-data/', views.get_consumer_bill_data, name='get_consumer_bill_data'),
    url(r'^get-consumer-complaint-details/', views.get_consumer_complaint_details, name='get_consumer_complaint_details'),
    url(r'^save-consumer-complaint-details/', views.save_consumer_complaint_details, name='save_consumer_complaint_details'),
    url(r'^upload-complaint-img/', views.upload_complaint_img, name='upload_complaint_img'),
    url(r'^remove-complaint-img/', views.remove_complaint_img, name='remove_complaint_img'),
    url(r'^save-attachments/', views.save_attachments, name='save_attachments'),
    url(r'^FAQS/', views.FAQS, name='FAQS'),
    url(r'^verify-new-consumer/', views.verify_new_consumer, name='verify_new_consumer'),
    url(r'^verify-OTP/', views.verify_OTP, name='verify_OTP'),
    url(r'^save-consumer/', views.save_consumer, name='save_consumer'),
    url(r'^save-vigilance-complaint/', views.save_vigilance_complaint, name='save_vigilance_complaint'),
    url(r'^upload-vigilance-image/', views.upload_vigilance_image,name='upload_vigilance_image'),    
]
 