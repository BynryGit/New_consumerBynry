$("#consumer_anchor").prepend('<span class="selected"></span>');
$("#consumer_menu").addClass("active open");
$("#consumer_span").addClass("open");
$("#payment_list").addClass("active open");

function add_payment() {	
		$( "#clear_div" ).load(" #clear_div" );
		$("#bill_month").append('<option value="">Select Bill Month</option>');
		document.getElementById("counter_bill").removeAttribute("hidden");
	   document.getElementById("counter_bill_footer").removeAttribute("hidden");	   
	   $("#counter_form").attr("hidden","hidden");           
		$("#counter_form_footer").attr("hidden","hidden");   		
		$('#consumer_no').val('');  	
		$('#paid_amt').val('');  	
		$("#responsive").modal('show');         
	}
	
	function reload_online_payments(){
        initTable1();
    }
    function reload_paytm_wallet(){
        initTable2();
    }
    function reload_cash_payments(){
        initTable3();
    }
	
	function search_consumer(){
	    initTable1();    
	    initTable2();    
	    initTable3();    
	}	
	
	 var initTable1 = function () {
		   filter_branch 	 = $("#filter_branch").val();
		   filter_zone 	 = $("#filter_zone").val();
		   filter_branch 	 = $("#filter_branch").val();
			filter_bill 	 = $("#filter_bill").val();
			filter_route 	 = $("#filter_route").val();			
			filter_from 	 = $("#filter_from").val();
			filter_to 		 = $("#filter_to").val();		     
        
        var table = $('#online_payment_table');

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

            //setup rowreorder extension: http://datatables.net/extensions/fixedheader/
            fixedHeader: {
                header: true,
                headerOffset: fixedHeaderOffset
            },
				
            "order": [
                [0, 'asc']
            ],
				"ajax": "/paymentapp/online_payments/?filter_branch="+filter_branch+"&filter_zone="+filter_zone+"&filter_bill="+filter_bill+"&filter_route="+filter_route+"&filter_from="+filter_from+"&filter_to="+filter_to+"",
                  "columns": [
                {"data": "payment_date"},
                {"data": "bill_amount_paid"}, 
                {"data": "transaction_id"}, 
                {"data" : "consumer_id"},      
                {"data" : "consumer_name"},      
                {"data" : "payment_mode"}                             
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
      $('#online_payment_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });
    }
    
     var initTable2 = function () {
     
     		filter_branch 	 = $("#filter_branch").val();
     		filter_zone 	 = $("#filter_zone").val();
			filter_bill 	 = $("#filter_bill").val();
			filter_route 	 = $("#filter_route").val();			
			filter_from 	 = $("#filter_from").val();
			filter_to 		 = $("#filter_to").val();	
			
        var table = $('#paytm_wallet_table');

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
				"ajax": "/paymentapp/paytm_payments/?filter_branch="+filter_branch+"&filter_zone="+filter_zone+"&filter_bill="+filter_bill+"&filter_route="+filter_route+"&filter_from="+filter_from+"&filter_to="+filter_to+"",
                  "columns": [
                {"data": "payment_date"},
                {"data": "bill_amount_paid"}, 
                {"data": "transaction_id"}, 
                {"data" : "consumer_id"},      
                {"data" : "consumer_name"},      
                {"data" : "payment_mode"}                             
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
      });
      $('#paytm_wallet_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });
    }

    //Cash Counter Table initialization
     var initTable3 = function () {     
     	 	filter_branch 	 = $("#filter_branch").val();
     	 	filter_zone 	 = $("#filter_zone").val();
			filter_bill 	 = $("#filter_bill").val();
			filter_route 	 = $("#filter_route").val();			
			filter_from 	 = $("#filter_from").val();
			filter_to 		 = $("#filter_to").val();	
			
        var table = $('#cash_payment_table');

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
				"ajax": "/paymentapp/cash_payments/?filter_branch="+filter_branch+"&filter_zone="+filter_zone+"&filter_bill="+filter_bill+"&filter_route="+filter_route+"&filter_from="+filter_from+"&filter_to="+filter_to+"",
                  "columns": [
                {"data": "payment_date"},
                {"data": "bill_amount_paid"}, 
                {"data": "transaction_id"}, 
                {"data" : "consumer_id"},      
                {"data" : "consumer_name"},      
                {"data" : "payment_mode"}                             
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
      $('#cash_payment_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            oTable.DataTable().button(action).trigger();
        });
    }	
    
    function clear_filter(){
        filter_zone 	 = $("#filter_zone").val('all').change();
        filter_branch 	 = $("#filter_branch").val('all').change();
			filter_bill 	 = $("#filter_bill").val('all').change();
			filter_route 	 = $("#filter_route").val('all').change();
			filter_from 	 = $("#filter_from").val('');
			filter_to 		 = $("#filter_to").val('');	
        initTable1();
        initTable2();
        initTable3();
    }

	function save_payment_details() {
			$(".error2").css("display", "none");	
			var paid_amount = $('#paid_amt').val();
			if (paid_amount == '') {
				$('.error2').text("Please enter amount");		
				return false;
			}
			else {
					$.ajax({
			       type	: "GET",
			       url : '/paymentapp/payments_save_payment_details/',
			       data : {'paid_amount':paid_amount,'consumer_no':$("#consumer_number").val(),'bill_month':$("#consumer_bill_month1").val()},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		  initTable3();
			     		  	$('#responsive').modal('hide');
			     		  	$('#success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}

	function get_payment_details() {
		$(".error2").css("display", "none");	
		$(".error").css("display", "none");	
		$(".error1").css("display", "none");	
		var consumer_number = $('#consumer_no').val(); 
		var bill_month = $('#bill_month').val(); 
		
		if (consumer_number == '' && bill_month == '') {			
			$('.error').text("Please enter Consumer Number");		
			$('.error1').text("Please select bill month");
			$(".error").css("display", "block");	
			$(".error1").css("display", "block");			
			return false;
		}
		else if (consumer_number == '') {
			$('.error1').text("");		
			$('.error').text("Please enter Consumer Number");	
			$(".error").css("display", "block");			
			return false;
		}
		else if (bill_month == '') {
			$('.error').text("");	
			$('.error1').text("Please select bill month");	
			$(".error1").css("display", "block");			
			return false;
		}
		else {			
	 
		   $.ajax({
		       type	: "GET",
		       url : '/paymentapp/payments_get_payment_details/',
		       data : {'consumer_no':consumer_number,'bill_month':bill_month},       
		       success: function (response) {			  
		     		  if(response.success=='true'){
						$("#consumer_number").val(response.payment_data.consumer_no); 
						$("#consumer_bill_month").text(response.payment_data.bill_month); 
						$("#consumer_bill_month1").val(response.payment_data.bill_month); 
						$("#meter_number").val(response.payment_data.meter_no); 
						$("#tariff_rate").val(response.payment_data.tariff_rate); 
						$("#current_reading").val(response.payment_data.current_month_reading); 
						$("#prev_month_reading").val(response.payment_data.previous_month_reading); 
						$("#consumption").val(response.payment_data.consumption); 
						$("#prompt_date").val(response.payment_data.payment_date); 
						$("#due_date").val(response.payment_data.due_date); 
						$("#arrears").val(response.payment_data.arriers); 
						$("#current_amt").val(response.payment_data.current_amount); 
						$("#prompt_amt").val(response.payment_data.bill_amount_paid); 
						$("#net_amt").val(response.payment_data.net_amount); 
						$("#due_date_amt").val(response.payment_data.amount_after_due_date); 	
						
						document.getElementById("counter_form").removeAttribute("hidden");
						document.getElementById("counter_form_footer").removeAttribute("hidden");	  	
		     		  	
		     			$("#counter_bill").attr("hidden","hidden");           
						$("#counter_bill_footer").attr("hidden","hidden");     
		     		  }
		     		  if(response.success=='false'){
							$('.error').text("");												    
							$('.error1').text("");												    
							$('.error').text("No Data Available");		
							$(".error").css("display", "block");													    
		     		  }
		       },
		       
		       error : function(response){
		       alert("_Error");
		       }
		   });	
		}
	}

 function consumer_details_modal(consumer_id){
     $.ajax({
         type : "GET",
         url : '/paymentapp/payments_get_consumer_details/',
         data : {'consumer_id':consumer_id},
         success: function (response) {
             if(response.success =='true'){
             	 $("#bill_cycle").val(response.consumerData.billCycle); 
		          $("#route_code").val(response.consumerData.consumerRoute); 
		          $("#consumer_zone").val(response.consumerData.consumerZone); 
		          $("#cNo").text(response.consumerData.consumerNo); 
		          $("#cName").text(response.consumerData.consumerName); 
		          $("#consumer_city").val(response.consumerData.consumerCity); 
		          $("#consumer_address").text(response.consumerData.consumerAddress); 
              	$("#consumer_details_modal").modal('show');  
             }
         },
         error : function(response){
             alert("_Error");
         }
     });        
  }
    
    initTable1();
    initTable2();
    initTable3();


function counter_submit() {
	document.getElementById("counter_form").removeAttribute("hidden");
	document.getElementById("counter_form_footer").removeAttribute("hidden");
	//document.getElementById("counter_bill").setAttributeNode("hidden"); 
	
	consumer_number = $('#consumer_number').val(); 
	bill_month = $('#bill_month').val(); 
 
   $.ajax({
       type	: "POST",
       url : '/paymentapp/payments_get_consumer_details/',
       data : {'consumer_no':consumer_no,'bill_month':bill_month},
       cache: false,
       processData: false,
       contentType: false,
       success: function (response) {			  
     		  if(response.success=='true'){
				$("#consumer_number").text(response.consumer_no);     		  	
     		  	
     			$("#counter_bill").attr("hidden","hidden");           
				$("#counter_bill_footer").attr("hidden","hidden");     
     		  }
       },
       
       error : function(response){
       alert("_Error");
       }
   });		      	
}

    $("#consumer_anchor").prepend('<span class="selected"></span>');
    $("#consumer_menu").addClass("active open");
    $("#consumer_span").addClass("open");
    $("#payment_list").addClass("active open");

   
 function get_zone(){
    branch = $("#filter_branch").val();
    $("#filter_zone").html('');
    $("#filter_zone").append('<option value="all">All</option>');
    $("#filter_bill").html('');
    $("#filter_bill").append('<option value="all">All</option>');
    $("#filter_route").html('');
    $("#filter_route").append('<option value="all">All</option>');
    $("#filter_route").val("all").change();
    if(branch != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-zone/',
            data : {'branch':branch},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.zone, function (index, item) {
                        $("#filter_zone").append('<option value="'+item.zone_id+'">'+item.zone_name+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}
    
function get_bill_cycle(){
	
    zone = $("#filter_zone").val();
    $("#filter_bill").html('');
    $("#filter_bill").append('<option value="all">All</option>');
    $("#filter_route").html('');
    $("#filter_route").append('<option value="all">All</option>');
    $("#filter_route").val("all").change();
    if(zone != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-bill-cycle/',
            data : {'zone':zone},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.bill_cycle, function (index, item) {
                        $("#filter_bill").append('<option value="'+item.bill_cycle_id+'">'+item.bill_cycle+'</option>')
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
    bill_cycle = $("#filter_bill").val();
    $("#filter_route").html('');
    $("#filter_route").append('<option value="all">All</option>');
    $("#filter_route").val("all").change();
    if(bill_cycle != ""){
        $.ajax({
            type : "GET",
            url : '/complaintapp/get-route/',
            data : {'bill_cycle':bill_cycle},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.route_list, function (index, item) {
                        $("#filter_route").append('<option value="'+item.route_id+'">'+item.route+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}    
    