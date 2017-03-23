 $("#system_user_anchor").prepend('<span class="selected"></span>');
 $("#system_user_menu").addClass("active open");
 $("#system_user_span").addClass("open");


 
 var initTable5 = function () {
     var table = $('#branch_agent_table');
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

			"ajax": "/branch_agent/",
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
     $('#branch_agent_tools > li > a.tool-action').on('click', function() {
         var action = $(this).attr('data-action');
         oTable.DataTable().button(action).trigger();
     });
 }
                 
 initTable5();                
    
 function add_branch_agent() {	
		//$( "#clear_div" ).load(" #clear_div" );
		$("#agent_city").append('<option value="">Select City</option>');
		$("#agent_branch_name").append('<option value="">Select Branch</option>');
		$('#agent_fname').val('');  	
		$('#agent_lname').val('');  	
		$('#agent_address').val('');  	
		$('#agent_emp_id').val('');  	
		$('#agent_contact_no').val('');  	
		$('#agent_email').val('');  	
		$('#agent_password').val('');  	
		$('#agent_re_password').val('');  	
		$("#add_branch_agent_modal").modal('show');         		         
	}          

function save_branch_agent_details() {
			var first_name = $('#agent_fname').val();
			var last_name = $('#agent_lname').val();
			var city = $('#agent_city').val();
			var branch = $('#agent_branch_name').val();
			var address = $('#agent_address').val();
			var emp_id = $('#agent_employee_id').val();
			var role = $('#agent_role').val();
			var contact_no = $('#agent_contact_no').val();
			var email = $('#agent_email').val();
			var user_status = $('#agent_user_status').val();
			var password = $('#agent_password').val();
			var re_password = $('#agent_re_password').val();
			
			if (validateAgentData()) {
					$.ajax({
			       type	: "GET",
			       url : '/save_system_user_details/',
			       data : {'user_status':user_status,'first_name':first_name,'last_name':last_name,'city':city,'branch':branch,'address':address,'emp_id':emp_id,'role':role,'contact_no':contact_no,'email':email,'password':password},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		  initTable5();
			     		  	$('#add_branch_agent_modal').modal('hide');
			     		  	$('#branch_agent_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });
			}
	}


function edit_branch_agent_modal(user_id) {
		   $.ajax({
		       type	: "GET",
		       url : '/get_system_user_details/',
		       data : {'user_id':user_id},       
		       success: function (response) {			  
		     		  if(response.success=='true'){
		     		  	$("#branch_agent_id").val(response.user_data.user_id);
						$("#branch_agent_first_name").val(response.user_data.first_name); 
						$("#branch_agent_last_name").val(response.user_data.last_name); 
						$("#branch_agent_address").val(response.user_data.address); 
						$("#branch_agent_email").val(response.user_data.email); 
						$("#branch_agent_emp_id").val(response.user_data.employee_id); 
						$("#branch_agent_contact_no").val(response.user_data.contact_no); 
						$("#branch_agent_city").val(response.user_data.city); 
						$("#branch_agent_status").val(response.user_data.user_status); 						
						
						$("#edit_branch_agent_modal").modal('show');   
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
	
	function update_agent_details() {
			var user_id = $('#branch_agent_id').val();
			var first_name = $('#branch_agent_first_name').val();
			var last_name = $('#branch_agent_last_name').val();
			var city = $('#branch_agent_city').val();
			var address = $('#branch_agent_address').val();
			var emp_id = $('#branch_agent_emp_id').val();
			var role = $('#branch_agent_role').val();
			var contact_no = $('#branch_agent_contact_no').val();
			var email = $('#branch_agent_email').val();
			var user_status = $('#branch_agent_status').val();
			var password = $('#branch_agent_password').val();
			var re_password = $('#branch_agent_re_password').val();
			
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
			     		  	$('#edit_branch_agent_modal').modal('hide');
			     		  	$('#branch_agent_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}


function get_agent_branch(){
    city = $("#agent_city").val();
    $("#agent_branch_name").html('');
    $("#agent_branch_name").append('<option value="">Select Branch</option>');
    //$("#branch_name").val("all").change();
    if(city != ""){
        $.ajax({
            type : "GET",
            url : '/get-branch/',
            data : {'city':city},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.branch_list, function (index, item) {
                        $("#agent_branch_name").append('<option value="'+item.branch_id+'">'+item.branch+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}   



function validateAgentData(){
	alert('in validateBranchAdminData');
	if(checkFirstName("#agent_fname")&checkLastName("#agent_lname")&CheckAddress("#agent_address")
	   &CheckCity("#agent_city")&checkEmail("#agent_email")&checkBranch("#agent_branch_name")
	   &CheckEmployeeID("#agent_employee_id")&checkContactNo("#agent_contact_no")&checkPassword("#agent_password")
	   &checkRePassword("#agent_re_password")
	  ){    
		return true;	
	}
	return false;
}

function checkFirstName(first_name){
 	var namePattern = /[A-Za-z]+/;  
	first_name = $(agent_fname).val()  
   if(namePattern.test(first_name)){
 	$(".agent_fname_error").css("display", "none");
   return true;
   }else{
    $(".agent_fname_error").css("display", "block");
    $(".agent_fname_error").text("Please enter valid first Name");
   return false; 
   }
}

function checkLastName(last_name){
 	var namePattern = /[A-Za-z]+/;  
	last_name = $(agent_lname).val()  
   if(namePattern.test(last_name)){
 	$(".agent_lname_error").css("display", "none");
   return true;
   }else{
    $(".agent_lname_error").css("display", "block");
    $(".agent_lname_error").text("Please enter valid last Name");
   return false; 
   }
}

function CheckEmployeeID(employee_id){
	employee_id = $(agent_employee_id).val()  
   if($(agent_employee_id).val()!='' && $(agent_employee_id).val()!=null)
   {
    $(".agent_employee_id_error").css("display", "none");
    return true;
   }else{
    $(".agent_employee_id_error").css("display", "block");
    $(".agent_employee_id_error").text("Please enter valid employee ID");
   return false; 
   }
}

function CheckAddress(address){
 	var namePattern = /[A-Za-z]+/;  
	address = $(agent_address).val()  
   if(namePattern.test(address)){
 	$(".agent_address_error").css("display", "none");
   return true;
   }else{
    $(".agent_address_error").css("display", "block");
    $(".agent_address_error").text("Please enter valid Address");
   return false; 
   }
}

function CheckCity(city){
	if($(agent_city).val()!=' ' && $(agent_city).val()!=null)
   {
    $(".agent_city_error").css("display", "none");
    return true;
   }else{
    $(".agent_city_error").css("display", "block");
    $(".agent_city_error").text("Please select City");
   return false; 
   }
}

function checkBranch(agent_branch_name){
	if($(agent_branch_name).val()!=' ' && $(agent_branch_name).val()!=null)
   {
    $(".agent_branch_name_error").css("display", "none");
    return true;
   }else{
    $(".agent_branch_name_error").css("display", "block");
    $(".agent_branch_name_error").text("Please select Branch");
   return false; 
   }
}

function checkEmail(email){
	Email = $(agent_email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   if(Email=='')
	{ 
	$(".agent_email_error").css("display", "none");
	return true;	
	}  
   else if(namePattern.test(Email)){
      $(".agent_email_error").css("display", "none");
   return true;
   }else{
 	$(".agent_email_error").css("display", "block");
   $(".agent_email_error").text("Please enter valid email");
   return false; 
   }
}

function checkContactNo(contact_no){
    contact_no = $(agent_contact_no).val()     
   var phoneNumberPattern = /^[789]\d{9}$/; 
  
   if(phoneNumberPattern.test(contact_no)){
    $(".agent_contact_no_error").parent().children('.error').css("display", "none");
   return true;
   }else if($(contact_no).val()==' ' && $(contact_no).val()==null){
    $(".agent_contact_no_error").css("display", "block");
    $(".agent_contact_no_error").text("Please enter valid employee ID");
   return false; 
   }
   else{
    $(".agent_contact_no_error").css("display", "block");
    $(".agent_contact_no_error").text("Please enter valid Contact Number");
   return false; 
   }
}

function checkPassword(password){
    password = $(agent_password).val()     
    re_password = $(agent_re_password).val()   
   if (password == ' ' && password==null) {		
		$(".agent_password_error").css("display", "block");
    	$(".agent_password_error").text("Password does not match");
    	return false;
   }
   else{
   	return true; 
   }
}

function checkRePassword(re_password){
    password = $(agent_password).val()  
    re_password = $(agent_re_password).val()     
   if (password == re_password) {		
		return true;
   }
   else{   	 
   	$(".agent_re_password_error").css("display", "block");
    	$(".agent_re_password_error").text("Password does not match");
    	return false;
   }
}
