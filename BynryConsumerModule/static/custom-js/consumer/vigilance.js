
var vigilanceTable = function () {
    var table = $('#vigilance_table');
    vigilance_type = $("#select_vigilance_type").val();
    start_date = $("#vigilance_start_date").val();
    end_date = $("#vigilance_end_date").val();
    consumer_id = getUrlParam("consumer_id", window.location.href);

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

        "ajax": "/vigilanceapp/get-vigilance-data/?vigilance_type="+vigilance_type+"&consumer_id="+consumer_id+"&start_date="+start_date+"&end_date="+end_date,
        "columns": [
            {"data": "case_id"},
            {"data": "vigilance_type"},
            {"data": "registered_date"},
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

vigilanceTable();

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

function filter_vigilance(){
    vigilanceTable();
}

function clear_vigilance_filter(){
    $("#select_vigilance_type").val('all').change();
    $("#vigilance_start_date").val("");
    $("#vigilance_end_date").val("");
    vigilanceTable();
}

function reload_vigilance(){
    vigilanceTable();
}
