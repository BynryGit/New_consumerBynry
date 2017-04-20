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
			filter_category = $("#filter_category").val('all').change();
			filter_service  = $("#filter_service").val('all').change();
			filter_from 	 = $("#filter_from").val('');
			filter_to 		 = $("#filter_to").val('');	
			initTable1();	  
    }

    pin_flag  = 0
    branch_flag  = 0
    zone_flag  = 0
    cycle_flag = 0
    route_flag = 0
    $('#edit_city').on("change", function(e) {
			getPincode();
			getBranch();
    });
    $('#edit_branch').on("change", function(e) {
			getZone();			
    });    
    $('#edit_zone').on("change", function(e) {
			getBillCycle();			
    });     
    $('#edit_bill_cycle').on("change", function(e) {
			getRoute();			
    });            
    
    function getPincode() {
		 if (pin_flag!=0) {

          city_id = $('#edit_city :selected').val();

          if (city_id) {
            $.ajax({
                type: 'GET',
                url: '/consumerapp/get-pincode/',
                data: {'city_id': city_id},
                success: function (response) {
          
                    $('#edit_pincode').html('');
                    $('#edit_pincode').append("<option value=''>Select Pincode</option>");
                    $.each(response.pincode_list, function (index, item) {
                        $('#edit_pincode').append(item);
                    });
                    $('#edit_pincode').val("").change();

                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }
        else {
            $('#edit_pincode').html('');
            $('#edit_pincode').append("<option value=''>Select Pincode</option>");
            $('#edit_pincode').val("").change();
        }
      }
      pin_flag=1
    }
    function getBranch() {
		 if (branch_flag!=0) {

          city_id = $('#edit_city :selected').val();

          if (city_id) {
            $.ajax({
                type: 'GET',
                url: '/consumerapp/get-branch/',
                data: {'city_id': city_id},
                success: function (response) {
          
                    $('#edit_branch').html('');
                    $('#edit_branch').append("<option value=''>Select Branch</option>");
                    $.each(response.branch_list, function (index, item) {
                        $('#edit_branch').append(item);
                    });
                    $('#edit_branch').val("").change();

                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }
        else {
            $('#edit_branch').html('');
            $('#edit_branch').append("<option value=''>Select Branch</option>");
            $('#edit_branch').val("").change();
        }
      }
      branch_flag=1
    }    
    function getZone() {
		 if (zone_flag!=0) {

          branch_id = $('#edit_branch :selected').val();

          if (branch_id) {
            $.ajax({
                type: 'GET',
                url: '/consumerapp/get-zone/',
                data: {'branch_id': branch_id},
                success: function (response) {
          
                    $('#edit_zone').html('');
                    $('#edit_zone').append("<option value=''>Select Zone</option>");
                    $.each(response.zone_list, function (index, item) {
                        $('#edit_zone').append(item);
                    });
                    $('#edit_zone').val("").change();

                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }
        else {
            $('#edit_zone').html('');
            $('#edit_zone').append("<option value=''>Select Zone</option>");
            $('#edit_zone').val("").change();
        }
      }
      zone_flag=1
    }        

    function getBillCycle() {
		 if (cycle_flag!=0) {

          zone_id = $('#edit_zone :selected').val();

          if (zone_id) {
            $.ajax({
                type: 'GET',
                url: '/consumerapp/get-billcycle/',
                data: {'zone_id': zone_id},
                success: function (response) {
          
                    $('#edit_bill_cycle').html('');
                    $('#edit_bill_cycle').append("<option value=''>Select Bill Cycle</option>");
                    $.each(response.billcycle_list, function (index, item) {
                        $('#edit_bill_cycle').append(item);
                    });
                    $('#edit_bill_cycle').val("").change();

                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }
        else {
            $('#edit_bill_cycle').html('');
            $('#edit_bill_cycle').append("<option value=''>Select Bill Cycle</option>");
            $('#edit_bill_cycle').val("").change();
        }
      }
      cycle_flag=1
    }      
    function getRoute() {
		 if (route_flag!=0) {

          bill_cycle_id = $('#edit_bill_cycle :selected').val();
				
          if (bill_cycle_id) {
            $.ajax({
                type: 'GET',
                url: '/consumerapp/get-route/',
                data: {'bill_cycle_id': bill_cycle_id},
                success: function (response) {
          
                    $('#edit_route').html('');
                    $('#edit_route').append("<option value=''>Select Route</option>");
                    $.each(response.route_list, function (index, item) {
                        $('#edit_route').append(item);
                    });
                    $('#edit_route').val("").change();

                },
                error: function (response) {
                    alert("Error!");
                },
            });
        }
        else {
            $('#edit_route').html('');
            $('#edit_route').append("<option value=''>Select Route</option>");
            $('#edit_route').val("").change();
        }
      }
      route_flag=1
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
						$('#edit_branch').val(response.data.branch_id).change();
						$('#edit_zone').val(response.data.zone_id).change();
						$('#edit_bill_cycle').val(response.data.bill_cycle_id).change();
						$('#edit_route').val(response.data.route_id).change();
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

function validate_data() {		
		if (checkContactNo("#edit_contact")&checkEmail("#edit_email")&CheckAadharNo("#edit_aadhar")&CheckAddress1("#edit_address1")&CheckAddress2("#edit_address2")&CheckCity()&CheckPincode()&CheckBranch()&CheckZone()&CheckBillCycle()&CheckRoute()&CheckMeterNo()&CheckSactionLoad()) {
		 	return true;	
		}
		return false;
	}
function checkContactNo(mobile){
    mobile = $(mobile).val()     
   var phoneNumberPattern = /^[789]\d{9}$/; 
   if(phoneNumberPattern.test(mobile)){
    $(mobile_error).css("display", "none");
   return true;
   }else{
    $(mobile_error).css("display", "block");
    $(mobile_error).text("Please enter valid Mobile Number");
   return false; 
   }
 }	
 function CheckAadharNo(applicant_aadhar_no){
   applicant_aadhar_no = $(applicant_aadhar_no).val()     
   var Pattern = /^\d{12}$/; 
 
   if(Pattern.test(applicant_aadhar_no)){
    $(edit_aadhar_error).css("display", "none");
   return true;
   }
   else{
    $(edit_aadhar_error).css("display", "block");
    $(edit_aadhar_error).text("Please enter valid Aadhar Number");
   return false; 
   }
   }
function CheckAddress1(address_line1){
 	var namePattern = /[A-Za-z]+/;  
	address_line1 = $(address_line1).val()  
   if(namePattern.test(address_line1)){
 	$(edit_address1_error).css("display", "none");
   return true;
   }else{
    $(edit_address1_error).css("display", "block");
    $(edit_address1_error).text("Please enter valid Address");
   return false; 
   }
}   
function checkEmail(email){
	Email = $(email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   if(Email=='')
	{ 
	$(edit_email_error).css("display", "none");
	return true;	
	}  
   else if(namePattern.test(Email)){
      $(email_error).css("display", "none");
   return true;
   }else{
 	$(edit_email_error).css("display", "block");
   $(edit_email_error).text("Please enter valid email");
   return false; 
   }
}
function CheckAddress2(address_line2){

 	var namePattern = /[A-Za-z]+/;  
 	address_line2 = $(edit_address2).val()
	if(address_line2=='')
    {
    $(edit_address2_error).css("display", "none");
    return true;    
    }  		  
   else if(namePattern.test(address_line2)){
 	$(edit_address2_error).css("display", "none");
   return true;
   }else{
    $(edit_address2_error).css("display", "block");
    $(edit_address2_error).text("Please enter valid Address");
   return false; 
   }
}
function CheckCity(edit_city){
	if($("#edit_city").val()!='' && $("#edit_city").val()!=null)
   {
    $(edit_city_error).css("display", "none");
    return true;
   }else{
    $(edit_city_error).css("display", "block");
    $(edit_city_error).text("Please select City");
   return false; 
   }
}
function CheckPincode(edit_pincode){
	if($("#edit_pincode").val()!='' && $("#edit_pincode").val()!=null)
   {
    $(edit_pincode_error).css("display", "none");
   return true;
   }else{
    $(edit_pincode_error).css("display", "block");
    $(edit_pincode_error).text("Please select Pincode");
   return false; 
   }
}
function CheckBranch(edit_branch){
	if($("#edit_branch").val()!='' && $("#edit_branch").val()!=null)
   {
    $(edit_branch_error).css("display", "none");
   return true;
   }else{
    $(edit_branch_error).css("display", "block");
    $(edit_branch_error).text("Please select Branch");
   return false; 
   }
}
function CheckZone(edit_zone){
	if($("#edit_zone").val()!='' && $("#edit_zone").val()!=null)
   {
    $(edit_zone_error).css("display", "none");
   return true;
   }else{
    $(edit_zone_error).css("display", "block");
    $(edit_zone_error).text("Please select Zone");
   return false; 
   }
}
function CheckBillCycle(edit_bill_cycle){
	if($("#edit_bill_cycle").val()!='' && $("#edit_bill_cycle").val()!=null)
   {
    $(edit_bill_cycle_error).css("display", "none");
   return true;
   }else{
    $(edit_bill_cycle_error).css("display", "block");
    $(edit_bill_cycle_error).text("Please select Bill Cycle");
   return false; 
   }
}
function CheckRoute(edit_route){
	if($("#edit_route").val()!='' && $("#edit_route").val()!=null)
   {
    $(edit_route_error).css("display", "none");
   return true;
   }else{
    $(edit_route_error).css("display", "block");
    $(edit_route_error).text("Please select Route");
   return false; 
   }
}
 function CheckMeterNo(){

	if($("#edit_meter_no").val()!='' && $("#edit_meter_no").val()!=null)
   {
    $(edit_meter_error).css("display", "none");
   return true;
   }else{
    $(edit_meter_error).css("display", "block");
    $(edit_meter_error).text("Please Enter Meter No.");
   return false; 
   }
   }
 function CheckSactionLoad(){

	if($("#edit_sanction_load").val()!='' && $("#edit_sanction_load").val()!=null)
   {
    $(edit_sanction_load_error).css("display", "none");
   return true;
   }else{
    $(edit_sanction_load_error).css("display", "block");
    $(edit_sanction_load_error).text("Please Enter Saction Load");
   return false; 
   }
   }   
 // Save edited consumer on edit button click 
$("#save-consumer").click(function(event)  {
	if (validate_data()) {
   	event.preventDefault();  
													
	   var formData= new FormData();

		formData.append("consumer_id",$('#consumer_id').val());		
		formData.append("edit_contact",$('#edit_contact').val());    
		formData.append("edit_email",$('#edit_email').val());    
		formData.append("edit_aadhar",$('#edit_aadhar').val()); 
		formData.append("edit_address1",$('#edit_address1').val()); 
		formData.append("edit_address2",$('#edit_address2').val()); 
		formData.append("edit_city",$('#edit_city').val());
		formData.append("edit_pincode",$('#edit_pincode').val());
		formData.append("edit_branch",$('#edit_branch').val()); 
		formData.append("edit_zone",$('#edit_zone').val()); 
		formData.append("edit_bill_cycle",$('#edit_bill_cycle').val());
		formData.append("edit_route",$('#edit_route').val());
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
	           	  		$("#success_modal").modal('show');
	              	}
	      			if (response.success == "false") {
	      				$("#edituser_model").modal('hide');
							$("#error-modal").modal('show');     
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
    }  
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
                "emptyTable": "No matching records found",
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
            { extend: 'print', className: 'btn dark btn-outline', 
                 filename: 'Consumer List  Bynry', "title": "Consumer List | Bynry",
                 exportOptions: {
                     columns: [ 0, 1, 2, 3, 4, 5, 6 ]
                 },
             },
            { extend: 'pdf', className: 'btn green btn-outline',
                 filename: 'Consumer List  Bynry', "title": "Consumer List | Bynry",
                 customize: function(doc) {
                     doc.defaultStyle.fontSize = 12; 
                     doc.defaultStyle.alignment= 'center';
                     doc.styles.tableHeader.fontSize = 14; 
                 },
                 exportOptions: {
                     columns: [ 0, 1, 2, 3, 4, 5, 6 ]
                 },
             },
             { extend: 'excel', className: 'btn yellow btn-outline',
                 filename: 'Consumer List  Bynry', "title": "Consumer List | Bynry",
                 customize: function(doc) {
                     doc.defaultStyle.alignment= 'center';
                 },
                 exportOptions: {
                     columns: [ 0, 1, 2, 3, 4, 5, 6 ]
                 },
             },
             { extend: 'csv', className: 'btn purple btn-outline',
                 filename: 'Consumer List  Bynry', "title": "Consumer List | Bynry",
                 customize: function(doc) {
                     doc.defaultStyle.alignment= 'center';
                 },
                 exportOptions: {
                     columns: [ 0, 1, 2, 3, 4, 5, 6 ]
                 },
             },
        ],

            "lengthMenu": [
                [5, 10, 15, 20, -1],
                [5, 10, 15, 20, "All"] // change per page values here
            ],
            // set the initial value
            "pageLength": 20,

            //"dom": "<'row' <'col-md-12'B>><'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r><'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>", // horizobtal scrollable datatable            
    });
    $('#consumer_table_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
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