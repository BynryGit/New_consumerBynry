 $("#system_user_anchor").prepend('<span class="selected"></span>');
 $("#system_user_menu").addClass("active open");
 $("#system_user_span").addClass("open");

 var initTable1 = function () {
     var table = $('#head_admin_table');

     var oTable = table.dataTable({
			"bDestroy" : true,
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
                {"data": "id","sClass": "text-center"},
                {"data": "name","sClass": "text-center"}, 
                {"data": "contact","sClass": "text-center"}, 
                {"data" : "email","sClass": "text-center"},      
                {"data" : "role","sClass": "text-center"},      
                {"data" : "status","sClass": "text-center"},      
                {"data" : "actions","sClass": "text-center"}                             
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
		//$("#city").append('<option value="">Select City</option>');
			$(".first_name_error").css("display", "none");			
			$(".last_name_error").css("display", "none");			
			$(".address_error").css("display", "none");			
			$(".email_error").css("display", "none");			
			$(".role_error").css("display", "none");			
			$(".branch_name_error").css("display", "none");			
			$(".employee_id_error").css("display", "none");			
			$(".contact_no_error").css("display", "none");			
			$(".city_error").css("display", "none");			
			$(".password_error").css("display", "none");			
			$(".re_password_error").css("display", "none");			
		
		$('#password').html('');  	
		$('#re_password').html('');
		$('#contact_no').html('');  
		$('#fname').val('');  	
		$('#lname').val('');  	
		$('#address').val('');  	
		$('#employee_ID').val('');  	
		$('#city').val('');  	
		$('#branch_name').val('');  	
		$('#role').val('');  	
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
			var emp_id = $('#employee_ID').val();
			var role = $('#role').val();
			var branch = $('#branch_name').val();
			var contact_no = $('#contact_no').val();
			var email = $('#email').val();
			var password = $('#password').val();
			
					
			user_status = document.getElementById('user_status').checked;
			
			if (validateData()) {
					$.ajax({
			       type	: "GET",
			       url : '/save_system_user_details/',
			       data : {'user_status':user_status,'first_name':first_name,'last_name':last_name,'branch':branch,'city':city,'address':address,'emp_id':emp_id,'role':role,'contact_no':contact_no,'email':email,'password':password},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		   initTable1();
			     		  	$('#add_admin_model').modal('hide');
			     		  	$('#success_modal').modal('show');
			     		  }
			     		  if (response.success == "false") {
								$("#error-modal").modal('show');
			    		  }	
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });		
			}
	}

function edit_admin_modal(user_id) {			
			$(".user_first_name_error").css("display", "none");			
			$(".user_last_name_error").css("display", "none");			
			$(".user_address_error").css("display", "none");			
			$(".user_email_error").css("display", "none");			
			$(".user_role_error").css("display", "none");			
			$(".user_branch_name_error").css("display", "none");			
			$(".user_emp_id_error").css("display", "none");			
			$(".user_contact_no_error").css("display", "none");			
			$(".user_city_error").css("display", "none");			
			$(".user_password_error").css("display", "none");			
			$(".user_re_password_error").css("display", "none");		
			$("#user_branch_name").prop("disabled", false);	
			
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
						$("#user_role").val(response.user_data.role); 
						$("#user_branch_name").val(response.user_data.branch); 
						$("#user_emp_id").val(response.user_data.employee_id); 
						$("#user_contact_no").val(response.user_data.contact_no); 
						$("#user_city").val(response.user_data.city); 

						if (response.user_data.user_status=='Active') {						
							$("#update_user_status").attr("checked",true).change(); 									
						}	
						else {							
							$("#update_user_status").attr("checked",false).change();
						}										
						if (response.user_data.role.match(/H.O./g)) {
							$("#user_branch_name").prop("disabled", true);
						}							
							
						$("#edit_admin_modal").modal('show');   
		     		  }
		     		  if (response.success == "false") {
								$("#error-modal").modal('show');
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
			var branch = $('#user_branch_name').val();
			var contact_no = $('#user_contact_no').val();
			var email = $('#user_email').val();
			var password = $('#user_pass').val();
			var re_password = $('#user_re_pass').val();
			
			user_status = document.getElementById('update_user_status').checked;

			if (validateEditData()) {
					$.ajax({
			       type	: "GET",
			       url : '/update_system_user_details/',
			       data : {'user_id':user_id,'user_status':user_status,'first_name':first_name,'last_name':last_name,'branch':branch,'city':city,'address':address,'emp_id':emp_id,'role':role,'contact_no':contact_no,'email':email,'password':password},       
			       success: function (response) {			  
			     		  if(response.success=='True'){
			     		  	initTable1();
			     		  	$('#edit_admin_modal').modal('hide');
			     		  	$('#success_update_modal').modal('show');
			     		  }
			     		  if (response.success == "false") {
								$("#error-modal").modal('show');
			    		  }	
			       },       
			       error : function(response){
			       alert("_Error");
			       }
			   });					
		}
	}

function validateEditData(){
	$(".user_branch_name_error").css("display", "none");
	if(check_firstname("#user_first_name")&check_lastname("#user_last_name")&check_address("#user_address")
	   &check_city("#user_city")&check_email("#user_email")&check_role("#user_role")
	   &check_employee_id("#user_emp_id")&check_contactno("#user_contact_no")&check_repassword("#user_re_pass")
	  ){    
		return true;	
	}
	return false;
}

function check_firstname(user_first_name){
 	var namePattern = /[A-Za-z]+/;  
	first_name = $(user_first_name).val()  
   if(namePattern.test(first_name)){
 	$(".user_first_name_error").css("display", "none");
   return true;
   }else{
    $(".user_first_name_error").css("display", "block");
    $(".user_first_name_error").text("Please enter valid first Name");
   return false; 
   }
}

function check_lastname(user_last_name){
 	var namePattern = /[A-Za-z]+/;  
	last_name = $(user_last_name).val()  
   if(namePattern.test(last_name)){
 	$(".user_last_name_error").css("display", "none");
   return true;
   }else{
    $(".user_last_name_error").css("display", "block");
    $(".user_last_name_error").text("Please enter valid last Name");
   return false; 
   }
}

function check_employee_id(user_emp_id){
	employee_id = $(user_emp_id).val()  
   if($(user_emp_id).val()!=' ' && $(user_emp_id).val()!=null)
   {
    $(".user_emp_id_error").css("display", "none");
    return true;
   }else{
    $(".user_emp_id_error").css("display", "block");
    $(".user_emp_id_error").text("Please enter valid employee ID");
   return false; 
   }
}

function check_address(user_address){
 	var namePattern = /[A-Za-z]+/;  
	address = $(user_address).val()  
   if(namePattern.test(address)){
 	$(".user_address_error").css("display", "none");
   return true;
   }else{
    $(".user_address_error").css("display", "block");
    $(".user_address_error").text("Please enter valid Address");
   return false; 
   }
}

function check_city(user_city){
	if($(user_city).val()!=' ' && $(user_city).val()!=null)
   {
    $(".user_city_error").css("display", "none");
    return true;
   }else{
    $(".user_city_error").css("display", "block");
    $(".user_city_error").text("Please select City");
   return false; 
   }
}

function check_role(user_role){
	if($(user_role).val()!=' ' && $(user_role).val()!=null)
   {
    $(".user_role_error").css("display", "none");
    return true;
   }else{
    $(".user_role_error").css("display", "block");
    $(".user_role_error").text("Please select Role");
   return false; 
   }
}

function check_email(user_email){
	Email = $(user_email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   if(Email=='')
	{ 
	$(".user_email_error").css("display", "block");
   $(".user_email_error").text("Please enter valid email");
	return true;	
	}  
   else if(namePattern.test(Email)){
      $(".user_email_error").css("display", "none");
   return true;
   }else{
 	$(".user_email_error").css("display", "block");
   $(".user_email_error").text("Please enter valid email");
   return false; 
   }
}

function check_contactno(user_contact_no){
    contact_no = $(user_contact_no).val()    
   var phoneNumberPattern = /^[789]\d{9}$/; 
  
   if(phoneNumberPattern.test(contact_no)){
    $(".user_contact_no_error").parent().children('.error').css("display", "none");
   return true;
   }else if($(contact_no).val()==' ' && $(contact_no).val()==null){
    $(".user_contact_no_error").css("display", "block");
    $(".user_contact_no_error").text("Please enter valid employee ID");
   return false; 
   }
   else{
    $(".user_contact_no_error").css("display", "block");
    $(".user_contact_no_error").text("Please enter valid Contact Number");
   return false; 
   }
}
/*
function check_password(user_pass){
	alert('inn password');
    password = $(user_pass).val()     
    re_password = $(user_re_pass).val()   
   if (password == ' ' && password==null) {		
		$(".user_password_error").css("display", "block");
    	$(".user_password_error").text("Password does not match");
    	return false;
   }
   else{
   	return true; 
   }
}*/

function check_repassword(user_re_pass){
    password = $(user_pass).val();  
    re_password = $(user_re_pass).val();
   if (password == re_password) {		
		return true;
   }
   else{   	 
   	$(".user_re_password_error").css("display", "block");
    	$(".user_re_password_error").text("Password does not match");
    	return false;
   }
}
	
	
function validateData(){
	$(".branch_name_error").css("display", "none");
	if(checkFirstName("#fname")&checkLastName("#lname")&CheckAddress("#address")
	   &CheckCity("#city")&checkEmail("#email")&checkRole("#role")//&checkBranch("#branch_name")
	   &CheckEmployee_ID("#employee_ID")&checkContactNo("#contact_no")&checkPassword("#password")
	   &checkRePassword("#re_password")
	  ){    
		return true;	
	}
	return false;
}

function checkFirstName(first_name){
 	var namePattern = /[A-Za-z]+/;  
	first_name = $(fname).val()  
   if(namePattern.test(first_name)){
 	$(".first_name_error").css("display", "none");
   return true;
   }else{
    $(".first_name_error").css("display", "block");
    $(".first_name_error").text("Please enter valid first Name");
   return false; 
   }
}

function checkLastName(last_name){
 	var namePattern = /[A-Za-z]+/;  
	last_name = $(lname).val()  
   if(namePattern.test(last_name)){
 	$(".last_name_error").css("display", "none");
   return true;
   }else{
    $(".last_name_error").css("display", "block");
    $(".last_name_error").text("Please enter valid last Name");
   return false; 
   }
}

function CheckEmployee_ID(employee_ID){
	employee_id = $(employee_ID).val()  
   if($(employee_ID).val()!=' ' && $(employee_ID).val()!=null)
   {
    $(".employee_id_error").css("display", "none");
    return true;
   }else{
    $(".employee_id_error").css("display", "block");
    $(".employee_id_error").text("Please enter valid employee ID");
   return false; 
   }
}

function CheckAddress(address){
 	var namePattern = /[A-Za-z]+/;  
	address = $(address).val()  
   if(namePattern.test(address)){
 	$(".address_error").css("display", "none");
   return true;
   }else{
    $(".address_error").css("display", "block");
    $(".address_error").text("Please enter valid Address");
   return false; 
   }
}

function CheckCity(city){
	if($(city).val()!=' ' && $(city).val()!=null)
   {
    $(".city_error").css("display", "none");
    return true;
   }else{
    $(".city_error").css("display", "block");
    $(".city_error").text("Please select City");
   return false; 
   }
}

/*function checkBranch(branch_name){
	if($(branch_name).val()!=' ' && $(branch_name).val()!=null)
   {
    $(".branch_name_error").css("display", "none");
    return true;
   }else{
    $(".branch_name_error").css("display", "block");
    $(".branch_name_error").text("Please select Branch");
   return false; 
   }
}*/

function checkRole(role){
	if($(role).val()!=' ' && $(role).val()!=null)
   {
    $(".role_error").css("display", "none");
    return true;
   }else{
    $(".role_error").css("display", "block");
    $(".role_error").text("Please select Role");
   return false; 
   }
}

function checkEmail(email){
	Email = $(email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   if(Email=='')
	{ 
	$(".email_error").css("display", "block");
   $(".email_error").text("Please enter valid email");
	return false;	
	}  
   else if(namePattern.test(Email)){
      $(".email_error").css("display", "none");
   return true;
   }else{
 	$(".email_error").css("display", "block");
   $(".email_error").text("Please enter valid email");
   return false; 
   }
}

function checkContactNo(contact_no){
    contact_no = $(contact_no).val()    
   var phoneNumberPattern = /^[789]\d{9}$/; 
   if(phoneNumberPattern.test(contact_no)){
    $(".contact_no_error").css("display", "none");
   return true;
   }else if($(contact_no).val()==' ' && $(contact_no).val()==null){
    	$(".contact_no_error").css("display", "block");
    	$(".contact_no_error").text("Please enter valid Contact Number");
   	return false; 
   }
   else{
    	$(".contact_no_error").css("display", "block");
    	$(".contact_no_error").text("Please enter valid Contact Number");
   	return false; 
   }
}

function checkPassword(password){
	if($(password).val()!='' && $(password).val()!=null)
   {
    	$(".password_error").css("display", "none");
    	return true;
   }else{
    	$(".password_error").css("display", "block");
    	$(".password_error").text("Please enter password ");
   	return false; 
   }     
}

function checkRePassword(re_password){
    password1 = $(password).val();  
    re_password1 = $(re_password).val();
   if (password1 == re_password1) {		
		return true;
   } 
   else if (password1 == 'undefined') {		
   	$(".re_password_error").css("display", "none");
		return false;
   }
   else{   	    
   	$(".re_password_error").css("display", "block");
    	$(".re_password_error").text("Password does not match");
    	return false;
   }
}


function get_branch_list(){
    city = $("#user_city").val();
    $("#user_branch_name").html('');
    $("#user_branch_name").append('<option value="">Select Branch</option>');
    if(city != ""){
        $.ajax({
            type : "GET",
            url : '/get-branch/',
            data : {'city':city},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.branch_list, function (index, item) {
                        $("#user_branch_name").append('<option value="'+item.branch_id+'">'+item.branch+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }
}  

function get_branch(){
    city = $("#city").val();
    $("#branch_name").html('');
    $("#branch_name").append('<option value="">Select Branch</option>');
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

function check_branch_data(){
	var role = $('#role').val();
	$("#branch_name").prop("disabled", false);  
	if (role.match(/H.O./g)) {
			$("#branch_name").prop("disabled", true);
			$(".branch_name_error").css("display", "none");
	    	return true;
		}	
		else {
			$(".branch_name_error").css("display", "block");
	    	$(".branch_name_error").text("Please select Branch");
	    	return false;
		}    
}  

function check_edit_branch_data(){
	var role = $('#user_role').val();
	$("#user_branch_name").prop("disabled", false);  
	if (role.match(/H.O./g)) {
			$("#user_branch_name").prop("disabled", true);
			$(".user_branch_name_error").css("display", "none");
	    	return true;
		}	
		else {
			$(".user_branch_name_error").css("display", "block");
	    	$(".user_branch_name_error").text("Please select Branch");
	    	return false;
		}    
}  

