$("#consumer_anchor").prepend('<span class="selected"></span>');
$("#consumer_menu").addClass("active open");
$("#consumer_span").addClass("open");
$("#complaint_list").addClass("active open");


var initTable1 = function () {
    var table = $('#vigilance_table');
    vigilance_type = $("#select_vigilance_type").val();
    vigilance_status = $("#select_vigilance_status").val();
    vigilance_source = $("#select_vigilance_source").val();
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

        "ajax": "/vigilanceapp/get-vigilance-data/?vigilance_type="+vigilance_type+"&vigilance_status="+vigilance_status+"&vigilance_source="+vigilance_source+"&zone="+zone+"&route="+route+"&bill_cycle="+bill_cycle+"&start_date="+start_date+"&end_date="+end_date,
        "columns": [
            {"data": "case_id"},
            {"data": "vigilance_type"},
            {"data": "registered_date"},
            {"data": "consumer_no"},
            {"data": "consumer_name"},
            {"data": "vigilance_source"},
            {"data": "vigilance_status"},
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
    $('#vigilance_table_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });
}

initTable1();

function vigilance_details(vigilance_id){
    $.ajax({
        type : "GET",
        url : '/vigilanceapp/get-vigilance-details/',
        data : {'vigilance_id':vigilance_id},
        success: function (response) {
            if(response.success =='true'){
                vigilanceDetail = response.vigilanceDetail;
                $("#case_id").val(vigilanceDetail.caseID);
                $("#vigilance_type").val(vigilanceDetail.vigilanceType);
                $("#registered_date").val(vigilanceDetail.registeredDate);
                $("#registered_source").val(vigilanceDetail.registeredSource);
                $("#case_status").val(vigilanceDetail.caseStatus);
                $("#theft_found").val(vigilanceDetail.theftFound);
                $("#vigilance_remark").text(vigilanceDetail.vigilanceRemark);
                $("#penalty_amount").val(vigilanceDetail.penaltyAmount);
                $("#payment_status").val(vigilanceDetail.paymentStatus);
                $("#payment_method").val(vigilanceDetail.paymentMethod);
                $("#court_case_status").val(vigilanceDetail.courtCaseStatus);
                $("#court_remark").text(vigilanceDetail.courtRemark);
            }
        },
        error : function(response){
            alert("_Error");
        }
    });
    $("#vigilance_details").modal('show');
}

function consumer_details(consumer_id){
    $.ajax({
        type : "GET",
        url : '/complaintapp/get-consumer-details/',
        data : {'consumer_id':consumer_id},
        success: function (response) {
            if(response.success =='true'){
                consumerDetail = response.consumerDetail;
                $("#bill_cycle").val(consumerDetail.billCycle);
                $("#route_code").val(consumerDetail.consumerRoute);
                $("#consumer_zone").val(consumerDetail.consumerZone);
                $("#consumer_city").val(consumerDetail.consumerCity);
                $("#consumer_no").val(consumerDetail.consumerNo);
                $("#consumer_name").val(consumerDetail.consumerName);
                $("#consumer_address").text(consumerDetail.consumerAddress);
            }
        },
        error : function(response){
            alert("_Error");
        }
    });
    $("#consumer_details").modal('show');
}

function filter_vigilance(){
    initTable1();
}

function reload_vigilance(){
    initTable1();
}



function get_bill_cycle(){
    zone = $("#select_zone").val();
    $("#select_bill_cycle").html('');
    $("#select_bill_cycle").append('<option value="all">All</option>');
    $("#select_route").html('');
    $("#select_route").append('<option value="all">All</option>');
    $("#select_route").val("all").change();
    if(zone != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-bill-cycle/',
            data : {'zone':zone},
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
    $("#select_route").html('');
    $("#select_route").append('<option value="all">All</option>');
    $("#select_route").val("all").change();
    if(bill_cycle != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-route/',
            data : {'bill_cycle':bill_cycle},
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