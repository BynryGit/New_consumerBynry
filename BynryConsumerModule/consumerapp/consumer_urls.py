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
    url(r'^save-consumer-details/', views.save_consumer_details,name='save_consumer_details'),
    url(r'^get-pincode/', views.get_pincode_front,name='get_pincode'),
    url(r'^get-branch/', views.get_branch_front,name='get_branch'),
    url(r'^get-zone/', views.get_zone_front,name='get_zone'),
    url(r'^get-billcycle/', views.get_billcycle_front,name='get_billcycle_front'),
    url(r'^get-route/', views.get_route_front,name='get_route_front'),
]

