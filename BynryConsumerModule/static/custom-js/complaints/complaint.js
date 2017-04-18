$("#consumer_anchor").prepend('<span class="selected"></span>');
$("#consumer_menu").addClass("active open");
$("#consumer_span").addClass("open");
$("#complaint_list").addClass("active open");

var initTable1 = function () {
    var table = $('#complaint_table');
    complaint_type = $("#select_complaint_type").val();
    complaint_status = $("#select_complaint_status").val();
    complaint_source = $("#select_complaint_source").val();
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
        "bDestroy":true,
        "language": {
            "aria": {
                "sortAscending": ": activate to sort column ascending",
                "sortDescending": ": activate to sort column descending"
            },
            "emptyTable": "No matching records found",
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

        "ajax": "/complaintapp/get-complaint-data/?complaint_type="+complaint_type+"&complaint_status="+complaint_status+"&complaint_source="+complaint_source+"&branch="+branch+"&zone="+zone+"&route="+route+"&bill_cycle="+bill_cycle+"&start_date="+start_date+"&end_date="+end_date,
        "columns": [
            {"data": "complaint_no"},
            {"data": "complaint_type"},
            {"data": "raised_date"},
            {"data": "consumer_no"},
            {"data": "consumer_name"},
            {"data": "complaint_source"},
            {"data": "complaint_status"},
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
    $('#complaint_table_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });
}

initTable1();

function complaint_details(complaint_id){
    $.ajax({
        type : "GET",
        url : '/complaintapp/get-complaint-details/',
        data : {'complaint_id':complaint_id},
        success: function (response) {
            if(response.success =='true'){
                $(".w3-content").html('');
                complaintDetail = response.complaintDetail;
                $("#complaint_id").val(complaintDetail.complaintID);
                $("#complaint_type").val(complaintDetail.complaintType);
                $("#complaint_status").val(complaintDetail.complaintStatus);
                $("#complaint_remark").text(complaintDetail.consumerRemark);
                $("#cons_name").text(complaintDetail.complaintConsumerName);
                $("#cons_no").text(complaintDetail.complaintConsumerNo);
                $("#complaint_details").modal('show');
                $.each(complaintDetail.complaint_img, function( index, value ) {
                    $(".w3-content").append('<img class="mySlides" src="'+value+'" style="width:100%;height:200px;">');
                });
                if(complaintDetail.complaint_img.length > 1)
                {
                    $(".w3-content").append('<button class="w3-button w3-black w3-display-left" onclick="plusDivs(-1)">&#10094;</button>');
                    $(".w3-content").append('<button class="w3-button w3-black w3-display-right" onclick="plusDivs(1)">&#10095;</button>');
                    showDivs(slideIndex);
                }
            }
        },
        error : function(response){
            alert("_Error");
            $("#complaint_details").modal('hide');
        }
    });
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



function filter_complaints(){
    initTable1();
}

function reload_complaints(){
    location.reload();
    //initTable1();
}

function get_zone(){
    branch = $("#select_branch").val();
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
    zone = $("#select_zone").val();
    branch = $("#select_branch").val();
    bill_cycle = $("#select_bill_cycle").val();
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

var slideIndex = 1;


function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("mySlides");
    if (n > x.length) {slideIndex = 1}
    if (n < 1) {slideIndex = x.length}
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex-1].style.display = "block";
}