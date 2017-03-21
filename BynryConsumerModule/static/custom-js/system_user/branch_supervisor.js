 $("#system_user_anchor").prepend('<span class="selected"></span>');
 $("#system_user_menu").addClass("active open");
 $("#system_user_span").addClass("open");


var initTable4 = function () {
     var table = $('#branch_supervisor_table');
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
         
         "ajax": "/branch_supervisor/",
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
     $('#branch_supervisor_tools > li > a.tool-action').on('click', function() {
         var action = $(this).attr('data-action');
         oTable.DataTable().button(action).trigger();
     });
 }
                 
 initTable4();                
    
 function add_branch_admin() {	
		//$( "#clear_div" ).load(" #clear_div" );
		$("#branch_supervisor_city").append('<option value="">Select City</option>');
		$("#branch_supervisor_name").append('<option value="">Select Branch</option>');
		$('#branch_supervisor_first_name').val('');  	
		$('#branch_supervisor_last_name').val('');  	
		$('#branch_supervisor_address').val('');  	
		$('#branch_supervisor_emp_id').val('');  	
		$('#branch_supervisor_contact_no').val('');  	
		$('#branch_supervisor_email').val('');  	
		$('#branch_supervisor_password').val('');  	
		$('#branch_supervisor_re_password').val('');  	
		$("#add_branch_supervisor_modal").modal('show');         		         
	}          

function save_branch_supervisor_details() {
	alert('in branch admin');
	alert($('#branch_supervisor_fname').val());
	alert($('#branch_supervisor_lname').val());
			var first_name = $('#branch_supervisor_fname').val();
			var last_name = $('#branch_supervisor_lname').val();
			var city = $('#branch_supervisor_city').val();
			var branch = $('#branch_supervisor_name').val();
			var address = $('#branch_supervisor_address').val();
			var emp_id = $('#branch_supervisor_employee_id').val();
			var role = $('#branch_supervisor_role').val();
			var contact_no = $('#branch_supervisor_contact_no').val();
			var email = $('#branch_supervisor_email').val();
			var user_status = $('#branch_supervisor_user_status').val();
			var password = $('#branch_supervisor_password').val();
			var re_password = $('#branch_supervisor_re_password').val();
			alert(password+''+re_password);
			
			if (password != re_password) {
				$('.error').text("Password does not match");		
				return false;
			}
			else {
					$.ajax({
			       type	: "GET",
			       url : '/save_system_user_details/',
			       data : {'user_status':user_status,'first_name':first_name,'last_name':last_name,'city':city,'branch':branch,'address':address,'emp_id':emp_id,'role':role,'contact_no':contact_no,'email':email,'password':password},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		  initTable4();
			     		  	$('#add_branch_supervisor_modal').modal('hide');
			     		  	$('#branch_supervisor_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });
			}
	}


function edit_branch_supervisor_modal(user_id) {
		   $.ajax({
		       type	: "GET",
		       url : '/get_system_user_details/',
		       data : {'user_id':user_id},       
		       success: function (response) {			  
		     		  if(response.success=='true'){
		     		  	$("#bas_user_id").val(response.user_data.user_id);
						$("#bas_user_first_name").val(response.user_data.first_name); 
						$("#bas_user_last_name").val(response.user_data.last_name); 
						$("#bas_user_address").val(response.user_data.address); 
						$("#bas_user_email").val(response.user_data.email); 
						$("#bas_user_emp_id").val(response.user_data.employee_id); 
						$("#bas_user_contact_no").val(response.user_data.contact_no); 
						$("#bas_user_city").val(response.user_data.city); 
						$("#bas_user_status").val(response.user_data.user_status); 						
						
						$("#edit_branch_supervisor_modal").modal('show');   
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
	
	function update_branch_supervisor_details() {
			var user_id = $('#bas_user_id').val();
			var first_name = $('#bas_user_first_name').val();
			var last_name = $('#bas_user_last_name').val();
			var city = $('#bas_user_city').val();
			var address = $('#bas_user_address').val();
			var emp_id = $('#bas_user_emp_id').val();
			var role = $('#bas_user_role').val();
			var contact_no = $('#bas_user_contact_no').val();
			var email = $('#bas_user_email').val();
			var user_status = $('#bas_update_user_status').val();
			var password = $('#bas_user_password').val();
			var re_password = $('#bas_user_re_password').val();
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
			     		  	$('#edit_branch_supervisor_modal').modal('hide');
			     		  	$('#branch_supervisor_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}


function get_supervisor_branch(){
    city = $("#branch_supervisor_city").val();
    alert(city);
    $("#branch_supervisor_name").html('');
    $("#branch_supervisor_name").append('<option value="">Select Branch</option>');
    //$("#branch_name").val("all").change();
    if(city != ""){
        $.ajax({
            type : "GET",
            url : '/get-branch/',
            data : {'city':city},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.branch_list, function (index, item) {
                        $("#branch_supervisor_name").append('<option value="'+item.branch_id+'">'+item.branch+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}   
