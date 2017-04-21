$("#nsc_anchor").prepend('<span class="selected"></span>');
$("#nsc_menu").addClass("active open");
$("#nsc_span").addClass("open");



var initTable1 = function () {
    var table = $('#nsc_table');
    consumer_category = $("#select_consumer_category").val();
    consumer_sub_category = $("#select_consumer_sub_category").val();
    supply_type = $("#select_supply_type").val();
    nsc_status = $("#select_nsc_status").val();
    start_date = $("#start_date").val();
    end_date = $("#end_date").val();

    var fixedHeaderOffset = 0;
    if (App.getViewPort().width < App.getResponsiveBreakpoint('md')) {
        if ($('.page-header').hasClass('page-header-fixed-mobile')) {
            fixedHeaderOffset = $('.page-header').outerHeight(true);
        }
    } else if ($('.page-header').hasClass('navbar-fixed-top')) {
        fixedHeaderOffset = $('.page-header').outerHeight(true);
    }

    var oTable = table.dataTable({
        "bDestroy":true,
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

        fixedHeader: {
            header: true,
            headerOffset: fixedHeaderOffset
        },

        "ajax": "/nscapp/get-nsc-data/?consumer_category="+consumer_category+"&consumer_sub_category="+consumer_sub_category+"&supply_type="+supply_type+"&nsc_status="+nsc_status+"&start_date="+start_date+"&end_date="+end_date,
        "columns": [
            {"data": "registration_id"},
            {"data": "applicant_name"},
            {"data": "category"},
            {"data": "sub_category"},
            {"data": "supply_type"},
            {"data": "registration_date"},
            {"data": "status"},
            {"data": "actions"},
        ],

        "order": [
            [0, 'asc']
        ],

        buttons: [        	
            { extend: 'print', className: 'btn dark btn-outline', 
                 filename: 'New Service Request  Bynry', "title": "New Service Request | Bynry",
                 exportOptions: {
                     columns: [ 0, 1, 2, 3, 4, 5, 6 ]
                 },
             },
            { extend: 'pdf', className: 'btn green btn-outline',
                 filename: 'New Service Request  Bynry', "title": "New Service Request | Bynry",
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
                 filename: 'New Service Request  Bynry', "title": "New Service Request | Bynry",
                 customize: function(doc) {
                     doc.defaultStyle.alignment= 'center';
                 },
                 exportOptions: {
                     columns: [ 0, 1, 2, 3, 4, 5, 6 ]
                 },
             },
             { extend: 'csv', className: 'btn purple btn-outline',
                 filename: 'New Service Request  Bynry', "title": "New Service Request | Bynry",
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
            [5, 10, 15, 20, "All"]
        ],
        "pageLength": 20,

    });
    $('#nsc_table_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });
}

initTable1();

function filter_nsc(){
    initTable1();
}

function clear_filter(){
    $('.select2').val('All').change();
    $("#start_date").val('');
    $("#end_date").val('');
    initTable1();
}

    // SHUBHAM KYC
    function open_remark_KYC() {
		if ($("#verify_KYC").val()== 'Rejected' ) {
	  		 $("#remark_div").css("display","block");
		}
		else {
   		$("#remark_div").css("display","none");
		}
	}
    function open_remark_technical() {
		if ($("#verify_technical").val()== 'Failed' ) {
	  		 $("#remark_div_tech").css("display","block");
		}
		else {
   		$("#remark_div_tech").css("display","none");
		}
    }
	function change_pay_mode() {
		$("#paymode_error").css("display", "none");
		$(amount_error).css("display", "none");
		$(checkno_error).css("display", "none");
		$(checknm_error).css("display", "none");
		$(checkDDno_error).css("display", "none");
		$(checkDDnm_error).css("display", "none");		
		if ($("#payment_mode").val()== 'DD' ) {
			 $("#cheque_div").css("display","none");
	  		 $("#DD_div").css("display","block");
		}
		else if ($("#payment_mode").val()== 'Cheque' ) {
   		$("#cheque_div").css("display","block");
   		$("#DD_div").css("display","none");
		}
	}
	   // KYC Verification
	function KYC_verify(var1) {
		  $("#remark_error").css("display", "none");
        var  registration_id = var1;
        $.ajax({
            type: 'GET',
            url: '/nscapp/get-verification-data/',
            data: {'registration_id': registration_id},
            success: function (response) {

            console.log(response);
                if (response.success == 'true') {
                	$('#KYC_aadhar_no').val(response.data.aadhar_no)
						$('#KYC_consumerid').val(response.data.consumer_id)
						$('#KYC_applicant_name').val(response.data.applicant_name)
						$('#KYC_mobile_no').val(response.data.meter_mobile_no)
						$('#KYC_email_id').val(response.data.meter_email_id)
						$('#KYC_address').val(response.data.address)
						$('#KYC_city').val(response.data.city_name)
						$('#KYC_pincode').val(response.data.pincode)
						$('#verify_KYC').val('').change()
						$('#KYC_remark').val('')		

                  $("#KYC_model").modal('show');
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
	function validate_KYC() {
		if ($("#verify_KYC").val() == '') {
			$("#kyc_status_error").css("display", "block");
		   $("#kyc_status_error").text("Please Select Status");
		   return false;
	   }
		else if ($('#verify_KYC').val() == 'Rejected' & $('#KYC_remark').val() == '') {
			$("#remark_error").css("display", "block");
		   $("#remark_error").text("Please write Remark");
		   return false;
		}
		else {
		   $("#remark_error").css("display", "none");
			return true
		}
	}
 	// Save KYC verification
	$("#save-KYC").click(function(event) {
		if (validate_KYC()) {

		event.preventDefault();

	   var formData= new FormData();

		formData.append("consumer_id",$('#KYC_consumerid').val());
		formData.append("verify_KYC_status",$('#verify_KYC').val());
		formData.append("KYC_remark",$('#KYC_remark').val());

  			$.ajax({
				  type	: "POST",
				   url : '/nscapp/save-consumer-kyc/',
 					data : formData,
					cache: false,
		         processData: false,
		    		contentType: false,
              success: function (response) {
	              if(response.success=='true'){
							$("#KYC_model").modal('hide');	           	  		
	           	  		$("#success_modal").modal('show');
	              	}
	      			if (response.success == "false") {
	      				$("#KYC_model").modal('hide');
							$("#error-model").modal('show');
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
// Technical
	function Technical_verify(var1) {
		  $("#checklist_error").css("display", "none");
		  $(techname_error).css("display", "none");
		  $(mobile_error).css("display", "none");
		  $("#techremark_error").css("display", "none");
        var  registration_id = var1;
        $.ajax({
            type: 'GET',
            url: '/nscapp/get-verification-data/',
            data: {'registration_id': registration_id},
            success: function (response) {

            console.log(response);
                if (response.success == 'true') {
                	$('#tech_consumerid').val(response.data.consumer_id)
						$('#tech_reg_no').val(response.data.registration_no)
						$('#tech_cons_names').val(response.data.applicant_name)
						$('#tech_cont_no').val(response.data.meter_mobile_no)
						$('#tech_address').val(response.data.address)
						$('#tech_category').val(response.data.consumer_category)
						$('#tech_subcat').val(response.data.consumer_subcategory)
						$('#tech_supply_type').val(response.data.supply_type)
						$('#tech_premise_type').val(response.data.type_of_premises)
						$('#technician_name').val('')
						$('#tech_contact_no').val('')
						$('#verify_technical').val('').change()
						$('#tech_remark').val('')
						document.getElementById("checkbox1_1").checked = false;
						document.getElementById("checkbox1_2").checked = false;
						document.getElementById("checkbox1_3").checked = false;
						document.getElementById("checkbox1_4").checked = false;
										
                  $("#technical_model").modal('show');
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

   function validate_Technical() {
		if (CheckChecklist()&checkName("#technician_name")&CheckContact("#tech_contact_no")&CheckStatus()&ChecktechStatus()) {
			return true;
		}
		return false;
	 }
	function CheckChecklist() {
			flag_1 = 0
			var CheckedList = document.getElementsByClassName('CheckListclass')
			for(var i=0; CheckedList[i]; ++i){
		      if(CheckedList[i].checked){
		           flag_1 = 1
		           break;
		      }
		   }
		   if (flag_1 == 1) {
		   	$("#checklist_error").css("display", "none");
		  		return true;
			}
			else {
		    	$("#checklist_error").css("display", "block");
		      $("#checklist_error").text("Please select at least one Check");
		   	return false;
			}
	}
	function checkName(techname) {
		 	var namePattern = /[A-Za-z]+/;
			techname = $(techname).val()
		   if(namePattern.test(techname)){
		 	$(techname_error).css("display", "none");
		   return true;
		   }else{
		    $(techname_error).css("display", "block");
		    $(techname_error).text("Please enter valid Name");
		   return false;
		   }
	}
	function CheckContact(mobile) {
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
	function CheckStatus() {
		if ($('#verify_technical').val() == 'Failed' & $('#tech_remark').val() == '') {
			$("#techremark_error").css("display", "block");
		   $("#techremark_error").text("Please write Remark");
		   return false;
		}
		else {
		   $("#techremark_error").css("display", "none");
			return true
		}
	}
	function ChecktechStatus() {
		if ($('#verify_technical').val() == '') {
			$("#techstatus_error").css("display", "block");
		   $("#techstatus_error").text("Please Select Status");
		   return false;
		}
		else {
		   $("#techstatus_error").css("display", "none");
			return true
		}
	}	
 	// Save technical verification
	$("#save-technical").click(function(event)  {
		if (validate_Technical()) {

			event.preventDefault();
  			$.ajax({
				  type	: "POST",
				   url : '/nscapp/save-consumer-technical/',
 					data : $("#technical_form").serialize(),

              success: function (response) {
	              if(response.success=='true'){
	              		$("#technical_model").modal('hide');
	           	  		$("#success_modal").modal('show');
	              	}
	      			if (response.success == "false") {
	      				$("#technical_model").modal('hide');
							$("#error-model").modal('show');

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

// Payment
	function Payment_verify(var1) {
		  $(amount_error).css("display", "none");
		  $(checkno_error).css("display", "none");
		  $(checknm_error).css("display", "none");
		  $(checkDDno_error).css("display", "none");
		  $(checkDDnm_error).css("display", "none");
        var  registration_id = var1;
        $.ajax({
            type: 'GET',
            url: '/nscapp/get-verification-data/',
            data: {'registration_id': registration_id},
            success: function (response) {

            console.log(response);
                if (response.success == 'true') {
                	$('#pay_consumerid').val(response.data.consumer_id)
						$('#pay_reg_no').val(response.data.registration_no)
						$('#pay_cons_name').val(response.data.applicant_name)
						$('#pay_cont_no').val(response.data.meter_mobile_no)
						$('#pay_category').val(response.data.consumer_category)
						$('#pay_subcategory').val(response.data.consumer_subcategory)
						$('#pay_supply_type').val(response.data.supply_type)
						$('#pay_address').val(response.data.address)
						$('#pay_pincode').val(response.data.pincode)						
						$('#pay_amount_paid').val('')
						$('#pay_cheque_no').val('')
						$('#payment_mode').val('').change()
						$('#pay_cheque_name').val('')						
                  $("#payment_model").modal('show');
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

	function validate_Payment() {
		$("#paymode_error").css("display", "none");
	 	if ($("#payment_mode").val()== 'DD' ) {
			if (CheckAmount()&CheckDDNo()&CheckDDName()) {
			  return true;
			}
			return false;
		}
		else if ($("#payment_mode").val()== 'Cheque' ){
			if (CheckAmount()&CheckCNo()&CheckCName()) {
			  return true;
			}
			return false;
		}
		else {
			if (PayModeStatus()) {
			  return true;
			}
			return false;
		}
	}
	function CheckAmount() {
		 	var namePattern = /[0-9]+/;
			Amount = $(pay_amount_paid).val()
			if(namePattern.test(Amount)){
		 	$(amount_error).css("display", "none");
		   return true;
		   }else{
		    $(amount_error).css("display", "block");
		    $(amount_error).text("Please enter valid Amount");
		   return false;
		   }
	}
	function CheckCNo() {
		 	var namePattern = /[0-9]+/;
			number = $(pay_cheque_no).val()
			if(namePattern.test(number)){
		 	$(checkno_error).css("display", "none");
		   return true;
		   }else{
		    $(checkno_error).css("display", "block");
		    $(checkno_error).text("Please enter valid Cheque No");
		   return false;
		   }
	}
	function CheckCName() {
		 	var namePattern = /[A-Za-z]+/;
			ckname = $(pay_cheque_name).val()
		   if(namePattern.test(ckname)){
		 	$(checknm_error).css("display", "none");
		   return true;
		   }else{
		    $(checknm_error).css("display", "block");
		    $(checknm_error).text("Please enter valid Name");
		   return false;
		   }
	}
	function CheckDDNo() {
		 	var namePattern = /[0-9]+/;
			number = $(pay_DD_no).val()
			if(namePattern.test(number)){
		 	$(checkDDno_error).css("display", "none");
		   return true;
		   }else{
		    $(checkDDno_error).css("display", "block");
		    $(checkDDno_error).text("Please enter valid DD No");
		   return false;
		   }
	}
	function CheckDDName() {
		 	var namePattern = /[A-Za-z]+/;
			ckname = $(pay_DD).val()
		   if(namePattern.test(ckname)){
		 	$(checkDDnm_error).css("display", "none");
		   return true;
		   }else{
		    $(checkDDnm_error).css("display", "block");
		    $(checkDDnm_error).text("Please enter valid Name");
		   return false;
		   }
	}
	function PayModeStatus() {
		if ($('#payment_mode').val() == '') {
			$("#paymode_error").css("display", "block");
		   $("#paymode_error").text("Please Select Payment Mode");
		   return false;
		}
		else {
		   $("#paymode_error").css("display", "none");
			return true
		}
	}		   
	   
	   
 	// Save payment verification
	$("#save-payment").click(function(event)  {
	if (validate_Payment()) {

		event.preventDefault();

  			$.ajax({
				  type	: "POST",
				   url : '/nscapp/save-consumer-payment/',
 					data : $("#payment_form").serialize(),

              success: function (response) {
	              if(response.success=='true'){
	              	   $("#payment_model").modal('hide');
	           	  		$("#success_modal").modal('show');
	              	}
	      			if (response.success == "false") {
	      				$("#payment_model").modal('hide');
							$("#error-model").modal('show');

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


    function consumer_details(registration_id) {
    	$("#error_meter_route").css("display", "none");
    	$("#error_meter_no").css("display", "none");
    	$("#error_meter_date").css("display", "none");
    	$("#error_meter_digit").css("display", "none");
    	$("#error_meter_make").css("display", "none");
    	$("#error_meter_type").css("display", "none");
    	$("#error_meter_status").css("display", "none");
        $.ajax({
            type: 'GET',
            url: '/nscapp/get-consumer-data/',
            data: {'registration_id': registration_id},
            success: function (response) {
            console.log(response);
                if (response.success == 'true') {
                    $('#meter_consumer_id').val(response.consumer_id);
                    $('#registration_no').val(response.registration_number);
                    $('#applicant_name').val(response.applicant_name);
                    $('#consumer_number').val(response.consumer_no);
                    $('#connection_category').val(response.consumer_category);
                    $('#connection_sub_category').val(response.consumer_sub_category);
                    $('#connection_supply_type').val(response.supply_type);
                    $('#connection_address').val(response.address);
                    $('#meter_route').val('').change();
                    $('#meter_no').val('');
                    $('#meter_date').val('');
                    $('#meter_digit').val('');
                    $('#meter_make').val('');
                    $('#meter_type').val('');
                    $('#meter_status').val('').change();
                    
                    $("#Meter_Detail_model").modal('show');  
                }
                if (response.success == 'false') {
                    alert(response.message);
                }
            },
            error: function (response) {
                alert('error');
            },
        });
	}

	function save_meter_details(){
	    if(validate_meter_details()){
            meter_status = $('#meter_status').val();
            meter_no = $('#meter_no').val();
            meter_date = $('#meter_date').val();
            meter_route = $('#meter_route').val();
            tech_name = $('#tech_name').val();
            tech_contact = $('#tech_contact').val();
            consumer_id = $('#meter_consumer_id').val();
            $.ajax({
				type	: "POST",
				url : '/nscapp/save-meter-details/',
 				data : {
 			        'meter_status' : $('#meter_status').val(),
                    'meter_no' : $('#meter_no').val(),
                    'meter_date' : $('#meter_date').val(),
                    'meter_route' : $('#meter_route').val(),
                    'consumer_id' : $('#meter_consumer_id').val(),
                    'meter_digit' : $('#meter_digit').val(),
                    'meter_make' : $('#meter_make').val(),
                    'meter_type' : $('#meter_type').val(),
 				},
                success: function (response) {
	                if(response.success=='true'){
	                    $("#Meter_Detail_model").modal('hide');
	           	  		$("#success_modal").modal('show');
	              	}
	      			if (response.success == "false") {
	      			 $("#Meter_Detail_model").modal('hide');
					    $("#error-model").modal('show');
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
	}


    function validate_meter_details() {
        if(validate_meter_data("meter_route","error_meter_route") & validate_meter_data("meter_no","error_meter_no") & validate_meter_data("meter_date","error_meter_date") & validate_meter_data("meter_digit","error_meter_digit") & validate_meter_data("meter_make","error_meter_make") & validate_meter_data("meter_type","error_meter_type") ){
            return true;
        }
    }

    function validate_meter_data(id,error) {
	 	if ($("#"+id).val()) {
            $("#"+error).css("display","none");
			return true;
		}
		else {
			$("#"+error).css("display","block");
            $("#"+error).css("color","red");
			return false;
		}
	}

	function CheckTechName() {
        var namePattern = /[A-Za-z]+/;
        ckname = $("#tech_name").val();
        $("#error_tech_name").css("color","red");
        if(!ckname){
            $("#error_tech_name").css("display", "block");
		    $("#error_tech_name").text("Please enter Technician Name");
            return false;
        }
		else if(namePattern.test(ckname)){
		 	$("#error_tech_name").css("display", "none");
		    return true;
		}else{
		    $("#error_tech_name").css("display", "block");
		    $("#error_tech_name").text("Please enter valid Name");
            return false;
        }
	}

	function checkTechNo(){
	    validate_meter_data("tech_contact","error_tech_contact")
        mobile = $("#tech_contact").val();
        $("#error_tech_contact").css("color","red");
        var phoneNumberPattern = /^[789]\d{9}$/;
        if(!mobile){
            $("#error_tech_contact").css("display", "block");
		    $("#error_tech_contact").text("Please enter Contact No.");
            return false;
        }
        if(phoneNumberPattern.test(mobile)){
            $("#error_tech_contact").css("display", "none");
            return true;
        }else{
            $("#error_tech_contact").css("display", "block");
            $("#error_tech_contact").text("Please enter valid Contact No.");
            return false;
        }
    }