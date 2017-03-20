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
    url(r'^get-kyc-data/', views.get_kyc_data,name='get_kyc_data'),
    url(r'^save-consumer-kyc/', views.save_consumer_kyc,name='save_consumer_kyc'),
    url(r'^get-technical-data/', views.get_technical_data,name='get_technical_data'),
    url(r'^save-consumer-technical/', views.save_consumer_technical,name='save_consumer_technical'),
]
