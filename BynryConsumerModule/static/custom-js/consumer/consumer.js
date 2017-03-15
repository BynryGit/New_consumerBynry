 $("#consumer_anchor").prepend('<span class="selected"></span>');
    $("#consumer_menu").addClass("active open");
    $("#consumer_span").addClass("open");
    $("#consumer_list").addClass("active open");
    
    // Clear Selected Filter
    function clear_filter(){
 	  		filter_branch 	 = $("#filter_branch").val('all').change();
 	  		filter_zone 	 = $("#filter_zone").val('all').change();
			filter_bill 	 = $("#filter_bill").val('all').change();
			filter_route 	 = $("#filter_route").val('all').change();
			filter_category = $("#filter_category").val('HT').change();
			filter_service  = $("#filter_service").val('Connected').change();
			filter_from 	 = $("#filter_from").val('');
			filter_to 		 = $("#filter_to").val('');		  
    }
    
   // Edit Consumer From Edit button click
	function edit_consumer(var1) {

        var  consumer_id = var1;
        $.ajax({
            type: 'GET',
            url: '/consumerapp/edit-consumer/',
            data: {'consumer_id': consumer_id},
            success: function (response) {
      
            console.log(response);
                if (response.success == 'true') {                	
						$('#edit_name').text(response.data.name)
						$('#consumer_id').val(response.data.consumer_id)						
						$('#edit_utility').val(response.data.utility)
						$('#edit_contact').val(response.data.contact_no)
						$('#edit_email').val(response.data.email_id)
						$('#edit_aadhar').val(response.data.aadhar_no)
						$('#edit_address1').val(response.data.address_line_1)
						$('#edit_address2').val(response.data.address_line_2)
						$('#edit_city').val(response.data.city_id).change();
						$('#edit_pincode').val(response.data.pincode_id).change();
						$('#edit_zone').val(response.data.zone_id).change();
						$('#edit_meter_no').val(response.data.meter_no)
						$('#edit_category').val(response.data.meter_category)
						$('#edit_sanction_load').val(response.data.sanction_load)
                  $("#edituser_model").modal('show');
                }
                if (response.success == 'false') {
                    alert(response.message);
                }
            },

            error: function (response) {
            console.log(response);
                alert('error');
            },
        });            
		}

 // Save edited consumer on edit button click 
$("#save-consumer").click(function(event)  {

	event.preventDefault();  
													
	   var formData= new FormData();

		formData.append("consumer_id",$('#consumer_id').val());		
		formData.append("edit_contact",$('#edit_contact').val());    
		formData.append("edit_email",$('#edit_email').val());    
		formData.append("edit_aadhar",$('#edit_aadhar').val()); 
		formData.append("edit_address1",$('#edit_address1').val()); 
		formData.append("edit_address2",$('#edit_address2').val()); 
		formData.append("edit_pincode",$('#edit_pincode').val()); 
		formData.append("edit_zone",$('#edit_zone').val()); 
		formData.append("edit_meter_no",$('#edit_meter_no').val());    
		formData.append("edit_sanction_load",$('#edit_sanction_load').val()); 
	
  			$.ajax({  				  
				  type	: "POST",
				   url : '/consumerapp/save-consumer-profile/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,                       
              success: function (response) {   
	              if(response.success=='true'){
	           	  		$("#edituser_model").modal('hide');
	           	  		location.reload();
	              	}
	      			if (response.success == "false") {
							$("#edituser_model").modal('hide');     
							location.reload()            
	       			}							                        		                      		                       		
               },
               	beforeSend: function () {
            $("#processing").css('display','block');
            },
            complete: function () {
                $("#processing").css('display','none');
            },
               error : function(response){
                  	alert("_Error");
            	}              
           });            
});


	// Search consumer based on selected filter
	function search_consumer(){
	    initTable1();    
	}		       
		
	 var initTable1 = function () {
	 		
	 		filter_branch 	 = $("#filter_branch").val();
 	  		filter_zone 	 = $("#filter_zone").val();
			filter_bill 	 = $("#filter_bill").val();
			filter_route 	 = $("#filter_route").val();
			filter_category = $("#filter_category").val();
			filter_service  = $("#filter_service").val();
			filter_from 	 = $("#filter_from").val();
			filter_to 		 = $("#filter_to").val();
		
        var table = $('#consumer_list1');

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

            "order": [
                [0, 'asc']
            ],

            "ajax": "/consumerapp/get-consumer-list/?filter_branch="+filter_branch+"&filter_zone="+filter_zone+"&filter_bill="+filter_bill+"&filter_route="+filter_route+"&filter_category="+filter_category+"&filter_service="+filter_service+"&filter_from="+filter_from+"&filter_to="+filter_to+"",
            "columns": [
                {"data": "consumer_no","sClass": "text-center"},
                {"data": "consumer_name","sClass": "text-center"},
                {"data": "contact_no","sClass": "text-center"},
                {"data": "email_id","sClass": "text-center"},
                {"data": "servicerequest","sClass": "text-center"},
                {"data": "complaintrequest","sClass": "text-center"},                                                        
                {"data": "connection_status","sClass": "text-center"}  ,
                {"data": "action","sClass": "text-center"}                                                       
            ],                                                    
                                                        
            buttons: [
                { extend: 'pdf', className: 'btn green btn-outline' },
                { extend: 'excel', className: 'btn yellow btn-outline ' },
            ],

            "lengthMenu": [
                [5, 10, 15, 20, -1],
                [5, 10, 15, 20, "All"] // change per page values here
            ],
            // set the initial value
            "pageLength": 20,

            "dom": "<'row' <'col-md-12'B>><'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r><'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>", // horizobtal scrollable datatable
      });
    }
    initTable1();
    
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