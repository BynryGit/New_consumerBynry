from nscapp import views
from django.conf.urls import include, url


urlpatterns = [
#SHUBHAM NEW
    url(r'^$', views.new_connection_list,name='new_connection'),    
    url(r'^add-new-consumer/', views.add_new_consumer,name='add_new_consumer'),        
    url(r'^review-consumer-form/', views.review_consumer_form,name='review_consumer_form'),
    url(r'^get-nsc-data/', views.get_nsc_data,name='get_nsc_data'),
    url(r'^save-new-consumer/', views.save_new_consumer,name='save_new_consumer'),
    url(r'^nsc-form/', views.nsc_form,name='nsc_form'),
    url(r'^upload-consumer-docs/', views.upload_consumer_docs,name='upload_consumer_docs'),
    url(r'^remove-consumer-docs/', views.remove_consumer_docs,name='remove_consumer_docs'),
    url(r'^get-verification-data/', views.get_verification_data,name='get_verification_data'),
    url(r'^save-consumer-kyc/', views.save_consumer_kyc,name='save_consumer_kyc'),    
    url(r'^save-consumer-technical/', views.save_consumer_technical,name='save_consumer_technical'),
    url(r'^save-consumer-payment/', views.save_consumer_payment,name='save_consumer_payment'),
    url(r'^get-consumer-data/', views.get_consumer_data,name='get_consumer_data'),
]
