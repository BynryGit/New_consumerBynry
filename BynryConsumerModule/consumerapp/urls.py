from.import views
# from django.conf.urls import include, url
from django.conf.urls import include, url


urlpatterns = [
    url(r'^consumer-jobcard/$',views.consumer_jobcard, name='consumer-jobcard'),
    url(r'^get-pc-accordingtoBU/$',views.get_pc_accordingtoBU, name='get-pc-accordingtoBU'),
    url(r'^consumer-jobcard-list-view/$', views.consumer_jobcard_list_view, name='consumer-jobcard-list-view'),
    url(r'^get-jobcard-byfilter-zone/(?P<consumer_id>\d+)/$', views.consumerdetail,name='filter_jobcard'),
    url(r'^consumer-card-search-filter/', views.consumer_card_search_filter,name='consumer-card-search-filter'),
    url(r'^consumer-card-filter/$', views.consumer_card_filter,name='consumer-card-filter'),
    # url(r'^consumer-jobcard/(?P<filterBy_BillingUnit>\d+)/(?P<filterBy_ProcessingCycle>\d+)/(?P<filterfromDate>\d+)/(?P<filtertoDate>\d+)/(?P<city>\d+)/$', views.consumer_jobcard,name='consumer-jobcard'),
    url(r'^get-consumer-list-view-detail/', views.get_consumer_list_view_detail),
    url(r'^get-consumer-card-list/', views.get_consumer_card_list),

    url(r'^get-consumer-count/', views.get_consumer_count),
    url(r'^get-service-count/', views.get_service_count),
    url(r'^get-complaint-count/', views.get_compliant_count),


    url(r'^consumerdetail/$', views.consumerdetail, name='consumerdetail'),
    url(r'^get-consumer-account-filterBy/',views.get_consumer_account_filterBy),
    url(r'^consumer-card-export-to-excel/',views.consumer_card_export_to_excel),
    url(r'^get-consumer-bill-payment-list/', views.get_consumer_bill_payment_list),
	url(r'^get-consumer-service-request-list/',views.get_consumer_service_request_list),
    url(r'^request-idDetail/', views.request_idDetail),
    url(r'^get-consumer-complaint-raised-list/',views.get_consumer_complaint_raised_list),
    url(r'^get-complaint-id-modal/', views.get_complaint_id_modal),
    url(r'^consumer-service-request-export-to-excel/',views.consumer_service_request_export_to_excel,name='consumer-service-request-export-to-excel'),
    url(r'^consumer-complaint-request-export-to-excel/',views.consumer_complaint_raised_export_to_excel,name='consumer-complaint-request-export-to-excel'),
]