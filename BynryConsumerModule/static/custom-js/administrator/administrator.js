 $("#admin_anchor").prepend('<span class="selected"></span>');
	 $("#admin_menu").addClass("active open");
	 $("#admin_span").addClass("open");
	
    
    	 var initTable1 = function () {	 	
		
        var table = $('#dispatch_bill_cycle_table');

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

            "ajax": "/get-role-list/",
            "columns": [
                {"data": "role","sClass": "text-center"},
                {"data": "description","sClass": "text-center"},
                {"data": "created_on","sClass": "text-center"},
                {"data": "associated_user","sClass": "text-center"},
                {"data": "status","sClass": "text-center"},
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

function validateRole(user_role){
	
	user_name = $(user_role).val()

   if($(user_role).val()!=''){
  
 	$(user_role).parent().children('.error').css("display", "none");
   return true;
   }else{
   
    $(user_role).parent().children('.error').css("display", "block");
    $(user_role).parent().children('.error').text("Please enter Role Name");
   return false; 
   }
}

function check_privilage(){
			var checkboxValues1 = []
			checkboxValues1 = $('.privillages:checked').map(function() {
			    return $(this).val();
			}).get(); 

			if (checkboxValues1.length == 0){
				$("#priv_err").css("display", "block");
				$("#priv_err").text("Please select at least 1 Privilege");
			   return false; 
			}else{
				$("#priv_err").css("display", "none");
				return true;
			}
		} 

$("#save-role").click(function(event)  {
 
 if(validateRole("#roll_name")){	
	var prv = check_privilage()
	if (prv == false){
     return false;	
	}		 
	event.preventDefault();  	
	var checkboxValues = []
	checkboxValues = $('.privillages:checked').map(function() {
			    return $(this).val();
			}).get(); 

	var formData= new FormData();

	formData.append("roll_name",$('#roll_name').val());
	formData.append("description",$('#description').val());				
	formData.append("privilege_list",checkboxValues);												
	console.log(checkboxValues)
	 $.ajax({  				  
			  type	: "POST",
			   url : '/save-new-role/',
	 			data : formData,
				cache: false,
		      processData: false,
		 		contentType: false, 
		 			               
	        success: function (response) {   
	           if(response.success=='true'){
						$("#success_modal").modal('show');						
	           	}
	   			if (response.success == "false") {
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
    
function edit_role_modal(role_id) {
		$("#edit_role_modal").modal('show');  
		   $.ajax({
		       type	: "GET",
		       url : '/get-role-details/',
		       data : {'role_id':role_id},       
		       success: function (response) {			  
		     		  if(response.success=='true'){
		     		  	$("#role_name").text(response.user_data.role);
		     		  	$("#roleid").val(response.user_data.role_id);
		     		  	$("#role_desc").text(response.user_data.role_description);
		     		  	$("#role_append").html(response.user_data.final_list);	
		     		  	document.getElementById('status_switch').checked = true;			
		     		  	
		     		  	$('label[for="' + $("#status_switch") + '"]').html								
						
						$("#edit_role_modal").modal('show');   
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
		
		
function update_role_details() {

		var checkboxValues = []
		checkboxValues = $('.privillagesModel:checked').map(function() {
			    return $(this).val();
			}).get(); 
		var formData= new FormData();

		formData.append("roleid",$('#roleid').val());
		formData.append("description",$('#role_desc').val());				
		formData.append("privilege_list",checkboxValues);
		formData.append("status",document.getElementById('status_switch').checked);
				
			$.ajax({				
			   type	: "POST",
			   url : '/update-role-details/',
	 			data : formData,
				cache: false,
		      processData: false,
		 		contentType: false, 
		 		
		      success: function (response) {			  
	     		  if(response.success=='True'){

	     		  	$('#edit_role_modal').modal('hide');
	     		  	$('#edit_success_modal').modal('show');
	     		  }
	       },       
	       error : function(response){
	       alert("_Error");
	       }
	   });				
	}		    
		