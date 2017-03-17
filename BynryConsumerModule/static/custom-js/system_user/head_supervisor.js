 $("#system_user_anchor").prepend('<span class="selected"></span>');
 $("#system_user_menu").addClass("active open");
 $("#system_user_span").addClass("open");


 var initTable2 = function () {
     var table = $('#head_supervisor_table');
     var oTable = table.dataTable({
         // Internationalisation. For more info refer to http://datatables.net/manual/i18n
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
         "ajax": "/head_supervisor/",
                  "columns": [
                {"data": "id"},
                {"data": "name"}, 
                {"data": "contact"}, 
                {"data" : "email"},      
                {"data" : "status"},      
                {"data" : "actions"}                             
		            ],

         buttons: [
             { extend: 'print', className: 'btn dark btn-outline' },
             { extend: 'pdf', className: 'btn green btn-outline' },
             { extend: 'excel', className: 'btn yellow btn-outline ' },
         ],
         // setup responsive extension: http://datatables.net/extensions/responsive/
         responsive: true,
         "order": [
             [0, 'asc']
         ],

         "lengthMenu": [
             [5, 10, 15, 20, -1],
             [5, 10, 15, 20, "All"] // change per page values here
         ],
         // set the initial value
         "pageLength": 10,
		});

     // handle datatable custom tools
     $('#head_supervisor_tools > li > a.tool-action').on('click', function() {
         var action = $(this).attr('data-action');
         oTable.DataTable().button(action).trigger();
     });
 }
 
               
 initTable2();                
    
 
 function add_head_supervisor() {	
		//$( "#clear_div" ).load(" #clear_div" );
		$("#city").append('<option value="">Select City</option>');
		$('#first_name').val('');  	
		$('#last_name').val('');  	
		$('#address').val('');  	
		$('#emp_id').val('');  	
		$('#contact_no').val('');  	
		$('#email').val('');  	
		$('#password').val('');  	
		$('#re_password').val('');  	
		$("#add_supervisor_modal").modal('show');         		         
	}          

function save_head_supervisor_details() {
	alert('in supervisor');
	alert($('#hs_fname').val());
	alert($('#hs_lname').val());
			var first_name = $('#hs_fname').val();
			var last_name = $('#hs_lname').val();
			var city = $('#hs_city').val();
			var address = $('#hs_address').val();
			var emp_id = $('#hs_employee_id').val();
			var role = $('#hs_role').val();
			var contact_no = $('#hs_contact_no').val();
			var email = $('#hs_email').val();
			var user_status = $('#hs_user_status').val();
			var password = $('#hs_password').val();
			var re_password = $('#hs_re_password').val();
			alert(password+''+re_password);
			
			if (password != re_password) {
				$('.error').text("Password does not match");		
				return false;
			}
			else {
					$.ajax({
			       type	: "GET",
			       url : '/save_system_user_details/',
			       data : {'user_status':user_status,'first_name':first_name,'last_name':last_name,'city':city,'address':address,'emp_id':emp_id,'role':role,'contact_no':contact_no,'email':email,'password':password},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		  initTable2();
			     		  	$('#add_supervisor_modal').modal('hide');
			     		  	$('#hs_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });
			}
	}


function edit_supervisor_modal(user_id) {
		   $.ajax({
		       type	: "GET",
		       url : '/get_system_user_details/',
		       data : {'user_id':user_id},       
		       success: function (response) {			  
		     		  if(response.success=='true'){
		     		  	$("#hs_user_id").val(response.user_data.user_id);
						$("#hs_user_first_name").val(response.user_data.first_name); 
						$("#hs_user_last_name").val(response.user_data.last_name); 
						$("#hs_user_address").val(response.user_data.address); 
						$("#hs_user_email").val(response.user_data.email); 
						$("#hs_user_emp_id").val(response.user_data.employee_id); 
						$("#hs_user_contact_no").val(response.user_data.contact_no); 
						$("#hs_user_city").val(response.user_data.city); 
						$("#hs_user_status").val(response.user_data.user_status); 						
						
						$("#edit_supervisor_modal").modal('show');   
		     		  }
		     		  if(response.success=='false'){
							$('.error').text("");												    
							$('.error1').text("");												    
							$('.error2').text("No Data Available");												    
		     		  }
		       },
		       
		       error : function(response){
		       alert("_Error");
		       }
		   });	
		}
	
	function update_head_supervisor_details() {
			var user_id = $('#hs_user_id').val();
			var first_name = $('#hs_user_first_name').val();
			var last_name = $('#hs_user_last_name').val();
			var city = $('#hs_user_city').val();
			var address = $('#hs_user_address').val();
			var emp_id = $('#hs_user_emp_id').val();
			var role = $('#hs_user_role').val();
			var contact_no = $('#hs_user_contact_no').val();
			var email = $('#hs_user_email').val();
			var user_status = $('#hs_update_user_status').val();
			var password = $('#hs_user_password').val();
			var re_password = $('#hs_user_re_password').val();
			alert(password+''+re_password);
			
			if (password != re_password) {
				$('.error').text("Password does not match");		
				return false;
			}
			else {
					$.ajax({
			       type	: "GET",
			       url : '/update_system_user_details/',
			       data : {'user_id':user_id,'user_status':user_status,'first_name':first_name,'last_name':last_name,'city':city,'address':address,'emp_id':emp_id,'role':role,'contact_no':contact_no,'email':email,'password':password},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		  initTable2();
			     		  	$('#edit_supervisor_modal').modal('hide');
			     		  	$('#hs_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}

