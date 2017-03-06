from complaintapp import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.complaint, name='Complaint'),
    url(r'^get-complaint-datatable/',views.get_complaint_datatable, name='getcomplaintdatatable'),
    url(r'^get-complaint-id-modal/',views.get_complaint_id_modal),
    url(r'^get-consumer-modal/',views.get_consumer_modal),
    url(r'^complaint-reading-export-to-excel/',views.complaint_reading_export,name='complaint_reading_export'),
    url(r'^get-complaint-count/',views.get_complaint_count,name='get_complaint_count'),

    ]