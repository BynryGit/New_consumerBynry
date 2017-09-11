    $("#consumer_anchor").prepend('<span class="selected"></span>');
    $("#consumer_menu").addClass("active open");
    $("#consumer_span").addClass("open");
    $("#service_list").addClass("active open");

    var initTable1 = function () {
        var table = $('#service_table');
        service_type = $("#select_service_type").val();
        service_status = $("#select_service_status").val();
        service_source = $("#select_service_source").val();
        branch = $("#select_branch").val();
        zone = $("#select_zone").val();
        bill_cycle = $("#select_bill_cycle").val();
        route = $("#select_route").val();
        start_date = $("#start_date").val();
        end_date = $("#end_date").val();
        
        var fixedHeaderOffset = 0;
        if (App.getViewPort().width < App.getResponsiveBreakpoint('md')) {
            if ($('.page-header').hasClass('page-header-fixed-mobile')) {
                fixedHeaderOffset = $('.page-header').outerHeight(true);
            }
        } else if ($('.page-header').hasClass('navbar-fixed-top')) {
            fixedHeaderOffset = $('.page-header').outerHeight(true);
        }

        var oTable = table.dataTable({
				"bDestroy" : true,
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

            // setup rowreorder extension: http://datatables.net/extensions/fixedheader/
            fixedHeader: {
                header: true,
                headerOffset: fixedHeaderOffset
            },

				"ajax": "/serviceapp/get-service-data/?service_type="+service_type+"&service_status="+service_status+"&service_source="+service_source+"&branch="+branch+"&zone="+zone+"&route="+route+"&bill_cycle="+bill_cycle+"&start_date="+start_date+"&end_date="+end_date,
            "columns": [
                {"data": "service_no"},
                {"data": "service_type"},
                {"data": "raised_date"},
                {"data": "consumer_no"},
                {"data": "consumer_name"},
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
                [5, 10, 15, 20, "All"] // change per page values here
            ],
            // set the initial value
            "pageLength": 20,

            //"dom": "<'row' <'col-md-12'B>><'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r><'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>", // horizobtal scrollable datatable
      });
      $('#service_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });
    }

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
                    $("#request_status").val(serviceDetail.serviceStatus);
                    $("#cons_name").text(serviceDetail.serviceConsumerName);
                    $("#cons_no").text(serviceDetail.serviceConsumerNo);
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
        $("#service_details").modal('show');
    }
	 
    function consumer_details(consumer_id){
        $.ajax({
            type : "POST",
            url : "/serviceapp/get-consumer-details/",
            data : {'consumer_id':consumer_id},
            success: function (response) {
                if(response.success =='true'){
                    consumerDetail = response.consumerDetail;
                    $("#bill_cycle").val(consumerDetail.billCycle);
                    $("#route_code").val(consumerDetail.consumerRoute);
                    $("#consumer_branch").val(consumerDetail.consumerBranch);
                    $("#consumer_zone").val(consumerDetail.consumerZone);
                    $("#consumer_no").text(consumerDetail.consumerNo);
                    $("#consumer_name").text(consumerDetail.consumerName);
                    $("#consumer_address").text(consumerDetail.consumerAddress);
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
        $("#consumer_details").modal('show');
    }
    
    function filter_services(){
        initTable1();
    }
    
    function reload_complaints(){
			location.reload();        
        //initTable1();
    }

    initTable1();
    



 function get_zone(){
    branch = $("#select_branch").val();
//    $( "#clear_zone_list" ).load(" #clear_zone_list" );
//    $( "#clear_bill_cycle" ).load(" #clear_bill_cycle" );
    $("#select_zone").html('');
    $("#select_zone").append('<option value="all">All</option>');
    $("#select_bill_cycle").html('');
    $("#select_bill_cycle").append('<option value="all">All</option>');
    $("#select_bill_cycle").val("all").change();
    $("#select_route").html('');
    $("#select_route").append('<option value="all">All</option>');
    $("#select_route").val("all").change();
    if(branch != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-zone/',
            data : {'branch':branch},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.zone, function (index, item) {
                        $("#select_zone").append('<option value="'+item.zone_id+'">'+item.zone_name+'</option>')
                    });
                    $("#select_zone").val("all").change();
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}
    
function get_bill_cycle(){
    zone = $("#select_zone").val();
    branch = $("#select_branch").val();
    $("#select_bill_cycle").html('');
    $("#select_bill_cycle").append('<option value="all">All</option>');
    $("#select_bill_cycle").val("all").change();
    $("#select_route").html('');
    $("#select_route").append('<option value="all">All</option>');
    $("#select_route").val("all").change();
    if(zone != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-bill-cycle/',
            data : {'zone':zone,'branch':branch},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.bill_cycle, function (index, item) {
                        $("#select_bill_cycle").append('<option value="'+item.bill_cycle_id+'">'+item.bill_cycle+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}

function get_route(){
    bill_cycle = $("#select_bill_cycle").val();
    zone = $("#select_zone").val();
    branch = $("#select_branch").val();
    $("#select_route").html('');
    $("#select_route").append('<option value="all">All</option>');
    $("#select_route").val("all").change();
    if(bill_cycle != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-route/',
            data : {'zone':zone,'branch':branch,'bill_cycle':bill_cycle},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.route_list, function (index, item) {
                        $("#select_route").append('<option value="'+item.route_id+'">'+item.route+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}