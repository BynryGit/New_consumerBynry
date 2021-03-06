function getUrlParam(param, url) {
  param = param.replace(/([\[\](){}*?+^$.\\|])/g, "\\$1");
  var regex = new RegExp("[?&]" + param + "=([^&#]*)");
  url   = url || decodeURIComponent(window.location.href);
  var match = regex.exec(url);
  return match ? match[1] : "";
}

var complaintTable = function () {
    var table = $('#complaint_table');
    complaint_type = $("#select_complaint_type").val();
    consumer_id = getUrlParam("consumer_id", window.location.href);
    start_date = $("#complaint_start_date").val();
    end_date = $("#complaint_end_date").val();

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

        "ajax": "/complaintapp/get-complaint-data/?complaint_type="+complaint_type+"&consumer_id="+consumer_id+"&start_date="+start_date+"&end_date="+end_date,
        "columns": [
            {"data": "complaint_no"},
            {"data": "complaint_type"},
            {"data": "raised_date"},
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

complaintTable();

function complaint_details(complaint_id){
    $.ajax({
        type : "GET",
        url : '/complaintapp/get-complaint-details/',
        data : {'complaint_id':complaint_id},
        success: function (response) {
            if(response.success =='true'){
                $(".complaint-slider").html('');
                complaintDetail = response.complaintDetail;
                $("#complaint_id").val(complaintDetail.complaintID);
                $("#complaint_type").val(complaintDetail.complaintType);
                $("#complaint_status").val(complaintDetail.complaintStatus);
                $("#complaint_remark").text(complaintDetail.consumerRemark);
                $("#cons_name").text(complaintDetail.complaintConsumerName);
                $("#cons_no").text(complaintDetail.complaintConsumerNo);
                $.each(complaintDetail.complaint_img, function( index, value ) {
                    $(".complaint-slider").append('<img class="mySlides" src="'+value+'" style="width:100%;height:200px;">');
                });
                if(complaintDetail.complaint_img.length > 1)
                {
                    $(".complaint-slider").append('<button class="w3-button w3-black w3-display-left" onclick="comPlusDivs(-1)">&#10094;</button>');
                    $(".complaint-slider").append('<button class="w3-button w3-black w3-display-right" onclick="comPlusDivs(1)">&#10095;</button>');
                    compShowDivs(compSlideIndex);
                }
            }
            else {
                $("#complaint_id").val('');
                $("#complaint_type").val('');
                $("#complaint_status").val('');
                $("#complaint_image").attr("src",'');
                $("#complaint_remark").text('');
                $("#cons_name").text('');
                $("#cons_no").text('');
            }
        },
        error : function(response){
            alert("_Error");
        }
    });
    $("#complaint_details").modal('show');
}

function filter_complaints(){
    complaintTable();
}

function reload_complaints(){
    complaintTable();
}

function clear_complaint_filter(){
    $("#select_complaint_type").val('all').change();
    $("#complaint_start_date").val("");
    $("#complaint_end_date").val("");
    complaintTable();
}

var compSlideIndex = 1;


function comPlusDivs(n) {
    compShowDivs(compSlideIndex += n);
}

function compShowDivs(n) {
    var i;
    var x = document.getElementsByClassName("mySlides");
    if (n > x.length) {compSlideIndex = 1}
    if (n < 1) {compSlideIndex = x.length}
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[compSlideIndex-1].style.display = "block";
}