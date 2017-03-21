 $("#system_user_anchor").prepend('<span class="selected"></span>');
 $("#system_user_menu").addClass("active open");
 $("#system_user_span").addClass("open");

 var initTable1 = function () {
     var table = $('#head_admin_table');

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
         
         "ajax": "/head_admin/",
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
     $('#head_admin_tools > li > a.tool-action').on('click', function() {
         var action = $(this).attr('data-action');
         oTable.DataTable().button(action).trigger();
     });
 }

 

 
   
 
	
 initTable1();                
     
 
 function add_admin() {	
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
		$("#add_admin_model").modal('show');         		         
	}          

function save_head_admin_details() {
			var first_name = $('#fname').val();
			var last_name = $('#lname').val();
			var city = $('#city').val();
			var address = $('#address').val();
			var emp_id = $('#employee_id').val();
			var role = $('#role').val();
			var contact_no = $('#contact_no').val();
			var email = $('#email').val();
			var user_status = $('#user_status').val();
			var password = $('#password').val();
			var re_password = $('#re_password').val();
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
			     		  initTable1();
			     		  	$('#add_admin_model').modal('hide');
			     		  	$('#success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}


function edit_admin_modal(user_id) {
		   $.ajax({
		       type	: "GET",
		       url : '/get_system_user_details/',
		       data : {'user_id':user_id},       
		       success: function (response) {			  
		     		  if(response.success=='true'){
						$("#user_id").val(response.user_data.user_id); 
						$("#user_first_name").val(response.user_data.first_name); 
						$("#user_last_name").val(response.user_data.last_name); 
						$("#user_address").val(response.user_data.address); 
						$("#user_email").val(response.user_data.email); 
						$("#user_emp_id").val(response.user_data.employee_id); 
						$("#user_contact_no").val(response.user_data.contact_no); 
						$("#user_city").val(response.user_data.city); 
						$("#user_status").val(response.user_data.user_status); 						
						
						$("#edit_admin_modal").modal('show');   
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
	
function update_head_admin_details() {
			var user_id = $('#user_id').val();
			var first_name = $('#user_first_name').val();
			var last_name = $('#user_last_name').val();
			var city = $('#user_city').val();
			var address = $('#user_address').val();
			var emp_id = $('#user_emp_id').val();
			var role = $('#user_role').val();
			var contact_no = $('#user_contact_no').val();
			var email = $('#user_email').val();
			var user_status = $('#update_user_status').val();
			var password = $('#user_password').val();
			var re_password = $('#user_re_password').val();
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
			     		  initTable1();
			     		  	$('#edit_admin_modal').modal('hide');
			     		  	$('#success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}
