from consumerapp import views
# from django.conf.urls import include, url
from django.conf.urls import include, url


urlpatterns = [
#SHUBHAM NEW
    url(r'^consumer-list/', views.consumer_list,name='consumer_list'),    
    url(r'^get-consumer-list/', views.get_consumer_list,name='get_consumer_list'),    
    url(r'^edit-consumer/', views.edit_consumer,name='edit_consumer'),    
    url(r'^save-consumer-profile/', views.save_consumer_profile,name='save_consumer_profile'),    
    url(r'^consumer-details/', views.consumer_details,name='consumer_details'),
    url(r'^get-meter-details/', views.get_meter_details,name='get_meter_details'),
]