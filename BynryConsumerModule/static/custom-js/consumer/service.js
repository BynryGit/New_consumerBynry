function getUrlParam(param, url) {
  param = param.replace(/([\[\](){}*?+^$.\\|])/g, "\\$1");
  var regex = new RegExp("[?&]" + param + "=([^&#]*)");
  url   = url || decodeURIComponent(window.location.href);
  var match = regex.exec(url);
  return match ? match[1] : "";
}

var serviceTable = function () {
	
    var table = $('#service_table');
    service_type = $("#select_service_type").val();
    consumer_id = getUrlParam("consumer_id", window.location.href);
    start_date = $("#service_start_date").val();
    end_date = $("#service_end_date").val();

    var fixedHeaderOffset = 0;
    if (App.getViewPort().width < App.getResponsiveBreakpoint('md')) {
        if ($('.page-header').hasClass('page-header-fixed-mobile')) {
            fixedHeaderOffset = $('.page-header').outerHeight(true);
        }
    } else if ($('.page-header').hasClass('navbar-fixed-top')) {
        fixedHeaderOffset = $('.page-header').outerHeight(true);
    }

    var oTable = table.dataTable({
        "bDestroy":true,
        "language": {
            "aria": {
                "sortAscending": ": activate to sort column ascending",
                "sortDescending": ": activate to sort column descending"
            },
            "emptyTable": "No data available in table",
            "info": "Showing _START_ to _END_ of _TOTAL_ entries",
            "infoEmpty": "No entries found",
            "infoFiltered": "(filtered1 from _MAX_ total entries)",
            "lengthMenu": "_MENU_ entries",
            "search": "Search:",
            "zeroRecords": "No matching records found"
        },

        fixedHeader: {
            header: true,
            headerOffset: fixedHeaderOffset
        },

			"ajax": "/serviceapp/get-service-data/?service_type="+service_type+"&consumer_id="+consumer_id+"&start_date="+start_date+"&end_date="+end_date,
            "columns": [
                {"data": "service_no"},
                {"data": "service_type"},
                {"data": "raised_date"},
                {"data": "service_source"},
                {"data": "service_status"},
            ],

        "order": [
            [0, 'asc']
        ],

        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
        ],

        "lengthMenu": [
            [5, 10, 15, 20, -1],
            [5, 10, 15, 20, "All"]
        ],
        "pageLength": 20,

    });
    $('#service_table_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });
}

serviceTable();

function service_details(service_id){
        $.ajax({
            type : "POST",
            url : '/serviceapp/get-service-details/',
            data : {'service_id':service_id},
            success: function (response) {
                if(response.success =='true'){
                    serviceDetail = response.serviceDetail;
                    $("#request_id").val(serviceDetail.serviceID);
                    $("#request_type").val(serviceDetail.serviceType);
                    $("#service_request").val(serviceDetail.serviceRequest);
                    $("#c_name").text(serviceDetail.serviceConsumerName);
                    $("#c_no").text(serviceDetail.serviceConsumerNo);
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
        $("#service_details").modal('show');
    }

function filter_services(){
    serviceTable();
}

function reload_services(){
    serviceTable();
}

function clear_service_filter(){
    $("#select_service_type").val('all').change();
    $("#service_start_date").val("");
    $("#service_end_date").val("");
    serviceTable();
}
