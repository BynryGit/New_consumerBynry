from nscapp import views
from django.conf.urls import include, url


urlpatterns = [
#SHUBHAM NEW
    url(r'^$', views.new_connection_list,name='new_connection'),    
    url(r'^add-new-consumer/', views.add_new_consumer,name='add_new_consumer'),        
]
