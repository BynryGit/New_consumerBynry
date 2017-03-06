from serviceapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.service_request, name='Service-request'),
    # url(r'^service-request/', services.service_request, name='service-request'),
    # url(r'^get-user-service-request-list/',services.get_user_service_request_list),
    # url(r'^get-filterBy-service-request/',services.get_filterBy_service_request),
    # url(r'^request-idDetail/',services.request_idDetail),
    # url(r'^consumer-connection-history/',services.consumer_connection_history),
    # url(r'^reading-export-to-excel/',services.servicerequest_reading_export,name='reading_export'),
    # url(r'^get-service-count/',services.get_service_count,name='get_service_count'),

   ]