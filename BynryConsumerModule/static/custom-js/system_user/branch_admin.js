 $("#system_user_anchor").prepend('<span class="selected"></span>');
 $("#system_user_menu").addClass("active open");
 $("#system_user_span").addClass("open");


 var initTable3 = function () {
     var table = $('#branch_admin_table');
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
         
         "ajax": "/branch_admin/",
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
     $('#branch_admin_tools > li > a.tool-action').on('click', function() {
         var action = $(this).attr('data-action');
         oTable.DataTable().button(action).trigger();
     });
 }
                
 initTable3();                
    
 function add_branch_admin() {	
		//$( "#clear_div" ).load(" #clear_div" );
		$("#branch_city").append('<option value="">Select City</option>');
		$("#branch_name").append('<option value="">Select Branch</option>');
		$('#branch_first_name').val('');  	
		$('#branch_last_name').val('');  	
		$('#branch_address').val('');  	
		$('#branch_emp_id').val('');  	
		$('#branch_contact_no').val('');  	
		$('#branch_email').val('');  	
		$('#branch_password').val('');  	
		$('#branch_re_password').val('');  	
		$("#add_branch_admin_modal").modal('show');         		         
	}          

function save_branch_admin_details() {
			var first_name = $('#branch_fname').val();
			var last_name = $('#branch_lname').val();
			var city = $('#branch_city').val();
			var branch = $('#branch_name').val();
			var address = $('#branch_address').val();
			var emp_id = $('#branch_employee_id').val();
			var role = $('#branch_role').val();
			var contact_no = $('#branch_contact_no').val();
			var email = $('#branch_email').val();
			var user_status = $('#branch_user_status').val();
			var password = $('#branch_password').val();
			var re_password = $('#branch_re_password').val();
			
			if (validateBranchAdminData()) {
					$.ajax({
			       type	: "GET",
			       url : '/save_system_user_details/',
			       data : {'user_status':user_status,'first_name':first_name,'last_name':last_name,'city':city,'branch':branch,'address':address,'emp_id':emp_id,'role':role,'contact_no':contact_no,'email':email,'password':password},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		  initTable3();
			     		  	$('#add_branch_admin_modal').modal('hide');
			     		  	$('#branch_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });
			}
	}


function edit_branch_admin_modal(user_id) {
		   $.ajax({
		       type	: "GET",
		       url : '/get_system_user_details/',
		       data : {'user_id':user_id},       
		       success: function (response) {			  
		     		  if(response.success=='true'){
		     		  	$("#ba_user_id").val(response.user_data.user_id);
						$("#ba_user_first_name").val(response.user_data.first_name); 
						$("#ba_user_last_name").val(response.user_data.last_name); 
						$("#ba_user_address").val(response.user_data.address); 
						$("#ba_user_email").val(response.user_data.email); 
						$("#ba_user_emp_id").val(response.user_data.employee_id); 
						$("#ba_user_contact_no").val(response.user_data.contact_no); 
						$("#ba_user_city").val(response.user_data.city); 
						$("#ba_user_status").val(response.user_data.user_status); 						
						
						$("#edit_branch_admin_modal").modal('show');   
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
	
	function update_branch_admin_details() {
			var user_id = $('#ba_user_id').val();
			var first_name = $('#ba_user_first_name').val();
			var last_name = $('#ba_user_last_name').val();
			var city = $('#ba_user_city').val();
			var address = $('#ba_user_address').val();
			var emp_id = $('#ba_user_emp_id').val();
			var role = $('#ba_user_role').val();
			var contact_no = $('#ba_user_contact_no').val();
			var email = $('#ba_user_email').val();
			var user_status = $('#ba_update_user_status').val();
			var password = $('#ba_user_password').val();
			var re_password = $('#ba_user_re_password').val();
			
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
			     		  	$('#edit_branch_admin_modal').modal('hide');
			     		  	$('#branch_success_modal').modal('show');
			     		  }
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}


function get_branch(){
    city = $("#branch_city").val();
    $("#branch_name").html('');
    $("#branch_name").append('<option value="">Select Branch</option>');
    //$("#branch_name").val("all").change();
    if(city != ""){
        $.ajax({
            type : "GET",
            url : '/get-branch/',
            data : {'city':city},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.branch_list, function (index, item) {
                        $("#branch_name").append('<option value="'+item.branch_id+'">'+item.branch+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}   



function validateBranchAdminData(){
	alert('in validateBranchAdminData');
	if(check_FirstName("#branch_fname")&check_LastName("#branch_lname")&check_Address("#branch_address")
	   &check_City("#branch_city")&check_Email("#branch_email")&check_Branch("#branch_name")
	   &check_EmployeeID("#branch_employee_id")&check_ContactNo("#branch_contact_no")&check_Password("#branch_password")
	   &check_RePassword("#branch_re_password")
	  ){    
		return true;	
	}
	return false;
}

function check_FirstName(first_name){
 	var namePattern = /[A-Za-z]+/;  
	first_name = $(branch_fname).val()  
   if(namePattern.test(first_name)){
 	$(".branch_fname_error").css("display", "none");
   return true;
   }else{
    $(".branch_fname_error").css("display", "block");
    $(".branch_fname_error").text("Please enter valid first Name");
   return false; 
   }
}

function check_LastName(last_name){
 	var namePattern = /[A-Za-z]+/;  
	last_name = $(branch_lname).val()  
   if(namePattern.test(last_name)){
 	$(".branch_lname_error").css("display", "none");
   return true;
   }else{
    $(".branch_lname_error").css("display", "block");
    $(".branch_lname_error").text("Please enter valid last Name");
   return false; 
   }
}

function check_EmployeeID(branch_employee_id){
	employee_id = $(branch_employee_id).val()  
   if($(branch_employee_id).val()!='' && $(branch_employee_id).val()!=null)
   {
    $(".branch_employee_id_error").css("display", "none");
    return true;
   }else{
    $(".branch_employee_id_error").css("display", "block");
    $(".branch_employee_id_error").text("Please enter valid employee ID");
   return false; 
   }
}

function check_Address(address){
 	var namePattern = /[A-Za-z]+/;  
	address = $(branch_address).val()  
   if(namePattern.test(address)){
 	$(".branch_address_error").css("display", "none");
   return true;
   }else{
    $(".branch_address_error").css("display", "block");
    $(".branch_address_error").text("Please enter valid Address");
   return false; 
   }
}

function check_City(city){
	if($(branch_city).val()!=' ' && $(branch_city).val()!=null)
   {
    $(".branch_city_error").css("display", "none");
    return true;
   }else{
    $(".branch_city_error").css("display", "block");
    $(".branch_city_error").text("Please select City");
   return false; 
   }
}

function check_Branch(branch){
	if($(branch_name).val()!=' ' && $(branch_name).val()!=null)
   {
    $(".branch_name_error").css("display", "none");
    return true;
   }else{
    $(".branch_name_error").css("display", "block");
    $(".branch_name_error").text("Please select Branch");
   return false; 
   }
}

function check_Email(email){
	Email = $(branch_email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   if(Email=='')
	{ 
	$(".branch_email_error").css("display", "none");
	return true;	
	}  
   else if(namePattern.test(Email)){
      $(".branch_email_error").css("display", "none");
   return true;
   }else{
 	$(".branch_email_error").css("display", "block");
   $(".branch_email_error").text("Please enter valid email");
   return false; 
   }
}

function check_ContactNo(contact_no){
    contact_no = $(branch_contact_no).val()     
   var phoneNumberPattern = /^[789]\d{9}$/; 
  
   if(phoneNumberPattern.test(contact_no)){
    $(".branch_contact_no_error").parent().children('.error').css("display", "none");
   return true;
   }else if($(contact_no).val()==' ' && $(contact_no).val()==null){
    $(".branch_contact_no_error").css("display", "block");
    $(".branch_contact_no_error").text("Please enter valid employee ID");
   return false; 
   }
   else{
    $(".branch_contact_no_error").css("display", "block");
    $(".branch_contact_no_error").text("Please enter valid Contact Number");
   return false; 
   }
}

function check_Password(password){
    password = $(branch_password).val()     
    re_password = $(branch_re_password).val()   
   if (password == ' ' && password==null) {		
		$(".branch_password_error").css("display", "block");
    	$(".branch_password_error").text("Password does not match");
    	return false;
   }
   else{
   	return true; 
   }
}

function check_RePassword(re_password){
    password = $(branch_password).val()  
    re_password = $(branch_re_password).val()     
   if (password == re_password) {		
		return true;
   }
   else{   	 
   	$(".branch_re_password_error").css("display", "block");
    	$(".branch_re_password_error").text("Password does not match");
    	return false;
   }
}
