$("#nsc_anchor").prepend('<span class="selected"></span>');
  $("#nsc_menu").addClass("active open");
  $("#nsc_span").addClass("open");

var doc_length = 0;

function make_same() {
   if (document.getElementById('checkbox1_44').checked) {
   		$("#bill_flat_no").val($("#flat_no").val());
			$("#bill_address_line1").val($("#address_line1").val());
			$("#bill_address_line2").val($("#address_line2").val());
			$("#bill_landmark").val($("#landmark").val());
			$("#bill_city").val($("#city").val()).change();			 
			$("#bill_pincode").val($("#pincode").val()).change();
			$("#bill_email").val($("#email").val());
			$("#bill_mobile").val($("#mobile").val());
			$("#bill_phone_no").val($("#phone_no").val());
			$("#bill_existing_consumer_no").val($("#existing_consumer_no").val());
			document.getElementById('bill_flat_no').readOnly = true;
			document.getElementById('bill_address_line1').readOnly = true;
			document.getElementById('bill_address_line2').readOnly = true;
			document.getElementById('bill_landmark').readOnly = true;
			document.getElementById('bill_city').disabled = true;
			document.getElementById('bill_pincode').disabled = true;
			document.getElementById('bill_email').readOnly = true;
			document.getElementById('bill_mobile').readOnly = true;
			document.getElementById('bill_phone_no').readOnly = true;
			document.getElementById('bill_existing_consumer_no').readOnly = true;
   } 
   else {

   		$("#bill_flat_no").val('');
			$("#bill_address_line1").val('');
			$("#bill_address_line2").val('');
			$("#bill_landmark").val('');
			$("#bill_city").val(' ').change();
			$("#bill_pincode").val(' ').change();
			$("#bill_email").val('');
			$("#bill_mobile").val('');
			$("#bill_phone_no").val('');
			$("#bill_existing_consumer_no").val('');   
			document.getElementById('bill_flat_no').readOnly = false;
			document.getElementById('bill_address_line1').readOnly = false;
			document.getElementById('bill_address_line2').readOnly = false;
			document.getElementById('bill_landmark').readOnly = false;
			document.getElementById('bill_city').disabled = false;
			document.getElementById('bill_pincode').disabled = false;
			document.getElementById('bill_email').readOnly = false;
			document.getElementById('bill_mobile').readOnly = false;
			document.getElementById('bill_phone_no').readOnly = false;
			document.getElementById('bill_existing_consumer_no').readOnly = false;			   	
   }
}
 
function clear_filter(){
    $( "#filter_div" ).load(" #filter_div" );
    setTimeout(function () {
        $('.select2').select2();
        //initTable1();
        src = "{% static 'assets/pages/scripts/components-date-time-pickers.min.js' %}";
        $('script[src="' + src + '"]').remove();
        $('<script>').attr('src', src).appendTo('head');
    }, 1000);
}



function hide_occupation() {
    if ($("#applicant_occupation").val() == 'OTHERS') {
        document.getElementById('applicant_other_details').readOnly = false;
    }
    else {
        $('#applicant_other_details').val("")
        document.getElementById('applicant_other_details').readOnly = true;
    }
}

function hide_premises() {
    if ($("#premises_type").val() == '4-LIS/OTHERS') {
        document.getElementById('bill_other_data').readOnly = false;
    }
    else {
        $('#bill_other_data').val("")
        document.getElementById('bill_other_data').readOnly = true;
    }
}

function validateData(){
	if(CheckConsumerCategory("#consumer_category")&CheckConsumerService("#consumer_service")&CheckSupplyType("#consumer_supply_type")
	   &CheckConsumerSubCategory("#consumer_subcategory")&checkName("#applicant_name")
	   &CheckAadharNo("#applicant_aadhar_no")&CheckOccupation("#applicant_occupation")
	   &CheckBusinessName("#flat_no")&CheckAddress1("#address_line1")&CheckAddress2("#address_line2")
	   &CheckLandmark("#landmark")&CheckCity("#city")&CheckPincode("#pincode")&checkEmail("#email")
	   &checkContactNo("#mobile")&checkHomePhone("#phone_no")&CheckConsumerNo("#existing_consumer_no")
 	   &CheckBillBusinessName("#bill_flat_no")&CheckBillAddress1("#bill_address_line1")&CheckBillAddress2("#bill_address_line2")
	   &CheckBillLandmark("#bill_landmark")&CheckBillCity("#bill_city")&CheckBillPincode("#bill_pincode")&checkBillEmail("#bill_email")
	   &checkBillContactNo("#bill_mobile")&checkBillHomePhone("#bill_phone_no")&CheckBillConsumerNo("#bill_existing_consumer_no")
	   &CheckPremises("#premises_type")&CheckRequestedLoad("#requested_load")&CheckLoadType("#load_type")
	   &CheckContractDemand("#contract_demand")&CheckDemandType("#contract_demand_type")&CheckAddressProof()&CheckIdProof()&CheckDropeZone()){
		return true;	
	}
	return false;
}


function CheckConsumerCategory(consumer_category){
    if($(consumer_category).val()!=' ' && $(consumer_category).val()!=null){
        $(consumer_category).parent().children('.error').css("display", "none");
        return true;
    }else{
        $(consumer_category).parent().children('.error').css("display", "block");
        $(consumer_category).parent().children('.error').text("Please select a Consumer Category");
        return false;
    }
}

function CheckConsumerService(consumer_service){
	if($(consumer_service).val()!=' ' && $(consumer_service).val()!=null){
        $(consumer_service).parent().children('.error').css("display", "none");
        return true;
    }else{
        $(consumer_service).parent().children('.error').css("display", "block");
        $(consumer_service).parent().children('.error').text("Please select a Service Requested");
        return false;
    }
}

function CheckSupplyType(consumer_supply_type){
	if($(consumer_supply_type).val()!=' ' && $(consumer_supply_type).val()!=null){
        $(consumer_supply_type).parent().children('.error').css("display", "none");
        return true;
    }else{
        $(consumer_supply_type).parent().children('.error').css("display", "block");
        $(consumer_supply_type).parent().children('.error').text("Please select a Supply Type");
        return false;
    }
}

function CheckConsumerSubCategory(consumer_subcategory){
    if($(consumer_subcategory).val()!=' ' && $(consumer_subcategory).val()!=null){
        $(consumer_subcategory).parent().children('.error').css("display", "none");
        return true;
    }else{
        $(consumer_subcategory).parent().children('.error').css("display", "block");
        $(consumer_subcategory).parent().children('.error').text("Please select a Consumer Subcategory");
        return false;
    }
}

function checkName(applicant_name){
 	var namePattern = /[A-Za-z]+/;  
	applicant_name = $(applicant_name).val()  
    if(namePattern.test(applicant_name)){
 	    $(applicant_name_error).css("display", "none");
        return true;
    }else{
        $(applicant_name_error).css("display", "block");
        $(applicant_name_error).text("Please enter valid Applicant Name");
        return false;
    }
}

function CheckAadharNo(applicant_aadhar_no){
    applicant_aadhar_no = $(applicant_aadhar_no).val()
    var Pattern = /^\d{12}$/;
    if(Pattern.test(applicant_aadhar_no)){
        $(applicant_aadhar_no_error).css("display", "none");
        return true;
    }
    else{
        $(applicant_aadhar_no_error).css("display", "block");
        $(applicant_aadhar_no_error).text("Please enter valid Aadhar Number");
        return false;
    }
}

function CheckOccupation(applicant_occupation){
	if($(applicant_occupation).val()!=' ' && $(applicant_occupation).val()!=null){
        if ($(applicant_occupation).val() == 'OTHERS') {
            if ($("#applicant_other_details").val() !=''){
                $("#applicant_other_error").css("display", "none");
                return true;
            }
            else {
                $(applicant_occupation).parent().children('.error').css("display", "none");
                $("#applicant_other_error").css("display", "block");
                $("#applicant_other_error").text("Please Enter Other Occupation");
             return false;
            }
        }
        else {
            $("#applicant_other_error").css("display", "none");
            $(applicant_occupation).parent().children('.error').css("display", "none");
            return true;
        }
    }else{
        $(applicant_occupation).parent().children('.error').css("display", "block");
        $(applicant_occupation).parent().children('.error').text("Please select Occupation");
        return false;
    }
}
function CheckBusinessName(flat_no){
 	var namePattern = /[A-Za-z]+/;  
	flat_no = $(flat_no).val()  
   if(namePattern.test(flat_no)){
 	$(flat_no_error).css("display", "none");
   return true;
   }else{
    $(flat_no_error).css("display", "block");
    $(flat_no_error).text("Please enter valid Name");
   return false; 
   }
}
function CheckAddress1(address_line1){
 	var namePattern = /[A-Za-z]+/;  
	address_line1 = $(address_line1).val()  
   if(namePattern.test(address_line1)){
 	$(address_line1_error).css("display", "none");
   return true;
   }else{
    $(address_line1_error).css("display", "block");
    $(address_line1_error).text("Please enter valid Address");
   return false; 
   }
}
function CheckAddress2(address_line2){

 	var namePattern = /[A-Za-z]+/;  
 	address_line2 = $(flat_no).val()
	if(address_line2=='')
    {
    $(address_line2_error).css("display", "none");
    return true;    
    }  		  
   else if(namePattern.test(address_line2)){
 	$(address_line2_error).css("display", "none");
   return true;
   }else{
    $(address_line2_error).css("display", "block");
    $(address_line2_error).text("Please enter valid Address");
   return false; 
   }
}
function CheckLandmark(landmark){
 	var namePattern = /[A-Za-z]+/;  
	landmark = $(landmark).val()  
	if(landmark=='')
    {
    $(landmark_error).css("display", "none");
    return true;    
    }  		
   else if(namePattern.test(landmark)){
 	$(landmark_error).css("display", "none");
   return true;
   }else{
    $(landmark_error).css("display", "block");
    $(landmark_error).text("Please enter valid Landmark");
   return false; 
   }
}

function CheckCity(city){
	if($(city).val()!=' ' && $(city).val()!=null)
   {
    $(city).parent().children('.error').css("display", "none");
    return true;
   }else{
    $(city).parent().children('.error').css("display", "block");
    $(city).parent().children('.error').text("Please select City");
   return false; 
   }
}

function CheckPincode(pincode){
	if($(pincode).val()!=' ' && $(pincode).val()!=null)
   {
    $(pincode).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(pincode).parent().children('.error').css("display", "block");
    $(pincode).parent().children('.error').text("Please select Pincode");
   return false; 
   }
}
function checkEmail(email){
	Email = $(email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   if(Email=='')
	{ 
	$(email_error).css("display", "none");
	return true;	
	}  
   else if(namePattern.test(Email)){
      $(email_error).css("display", "none");
   return true;
   }else{
 	$(email_error).css("display", "block");
   $(email_error).text("Please enter valid email");
   return false; 
   }
}

function checkContactNo(mobile){
    mobile = $(mobile).val()     
   var phoneNumberPattern = /^[789]\d{9}$/; 
   if(phoneNumberPattern.test(mobile)){
    $(mobile_error).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(mobile_error).parent().children('.error').css("display", "block");
    $(mobile_error).parent().children('.error').text("Please enter valid Mobile Number");
   return false; 
   }
}

function checkHomePhone(home){
    home = $(home).val()     
   var phoneNumberPattern = /^[0]\d{10,11}$/; 
  if(home=='')
    {
    $(phone_no_error).css("display", "none");
    return true;    
    } 
   else if(phoneNumberPattern.test(home)){
 	$(phone_no_error).css("display", "none");
   return true;
   }else{
    $(phone_no_error).css("display", "block");
    $(phone_no_error).text("Please enter valid Landline Number");
   return false; 
   }
}
function CheckConsumerNo(existing_consumer_no){
 	var namePattern = /[0-9]+/;  
	existing_consumer_no = $(existing_consumer_no).val()  
   if(existing_consumer_no=='')
    {
    $(consumer_no_error).css("display", "none");
    return true;    
    } 	
   else if(namePattern.test(existing_consumer_no)){
 	$(consumer_no_error).css("display", "none");
   return true;
   }else{
    $(consumer_no_error).css("display", "block");
    $(consumer_no_error).text("Please enter valid Consumer No");
   return false; 
   }
}
 
 function CheckBillBusinessName(flat_no){
 	var namePattern = /[A-Za-z]+/;  
	flat_no = $(flat_no).val()  
   if(namePattern.test(flat_no)){
 	$(bill_flat_no_error).css("display", "none");
   return true;
   }else{
    $(bill_flat_no_error).css("display", "block");
    $(bill_flat_no_error).text("Please enter valid Name");
   return false; 
   }
}
function CheckBillAddress1(address_line1){
 	var namePattern = /[A-Za-z]+/;  
	address_line1 = $(address_line1).val()  
   if(namePattern.test(address_line1)){
 	$(bill_address_line1_error).css("display", "none");
   return true;
   }else{
    $(bill_address_line1_error).css("display", "block");
    $(bill_address_line1_error).text("Please enter valid Address");
   return false; 
   }
}
function CheckBillAddress2(address_line2){

 	var namePattern = /[A-Za-z]+/;  
 	address_line2 = $(flat_no).val()
	if(address_line2=='')
    {
    return true;    
    }  		  
   else if(namePattern.test(address_line2)){
 	$(bill_address_line2_error).css("display", "none");
   return true;
   }else{
    $(bill_address_line2_error).css("display", "block");
    $(bill_address_line2_error).text("Please enter valid Address");
   return false; 
   }
}
function CheckBillLandmark(landmark){
 	var namePattern = /[A-Za-z]+/;  
	landmark = $(landmark).val()  
	if(landmark=='')
    {
    $(bill_landmark_error).css("display", "none");
    return true;    
    }  		
   else if(namePattern.test(landmark)){
 	$(bill_landmark_error).css("display", "none");
   return true;
   }else{
    $(bill_landmark_error).css("display", "block");
    $(bill_landmark_error).text("Please enter valid Landmark");
   return false; 
   }
}

function CheckBillCity(city){
	if($(city).val()!=' ' && $(city).val()!=null)
   {
    $(city).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(city).parent().children('.error').css("display", "block");
    $(city).parent().children('.error').text("Please select City");
   return false; 
   }
}

function CheckBillPincode(pincode){
	if($(pincode).val()!=' ' && $(pincode).val()!=null)
   {
    $(pincode).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(pincode).parent().children('.error').css("display", "block");
    $(pincode).parent().children('.error').text("Please select Pincode");
   return false; 
   }
}
function checkBillEmail(email){
	Email = $(email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   	if(Email=='')
	{
   $(bill_email_error).css("display", "none");
	return true;	
	}  
   else if(namePattern.test(Email)){
      $(bill_email_error).css("display", "none");
   return true;
   }else{
 	$(bill_email_error).css("display", "block");
   $(bill_email_error).text("Please enter valid email");
   return false; 
   }
}

function checkBillContactNo(mobile){
    mobile = $(mobile).val()     
   var phoneNumberPattern = /^[789]\d{9}$/; 
   if(phoneNumberPattern.test(mobile)){
    $(bill_mobile_error).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(bill_mobile_error).parent().children('.error').css("display", "block");
    $(bill_mobile_error).parent().children('.error').text("Please enter valid Mobile Number");
   return false; 
   }
}

function checkBillHomePhone(home){
    home = $(home).val()     
   var phoneNumberPattern = /^[0]\d{10,11}$/; 
  if(home=='')
    {
    $(phone_no_error).css("display", "none");
    return true;    
    } 
   else if(phoneNumberPattern.test(home)){
 	$(phone_no_error).css("display", "none");
   return true;
   }else{
    $(bill_phone_no_error).css("display", "block");
    $(bill_phone_no_error).text("Please enter valid Landline Number");
   return false; 
   }
}
function CheckBillConsumerNo(existing_consumer_no){
 	var namePattern = /[0-9]+/;  
	existing_consumer_no = $(existing_consumer_no).val() 
   if(existing_consumer_no=='')
    {
    $(bill_existing_consumer_no_error).css("display", "none");
    return true;    
    } 	
   else if(namePattern.test(existing_consumer_no)){
 	$(bill_existing_consumer_no_error).css("display", "none");
   return true;
   }else{
    $(bill_existing_consumer_no_error).css("display", "block");
    $(bill_existing_consumer_no_error).text("Please enter valid Consumer No");
   return false; 
   }
}
function CheckPremises(premises_type){
	if($(premises_type).val()!=' ' && $(premises_type).val()!=null)
   {
    if ($(premises_type).val() == '4-LIS/OTHERS') {
    	if ($("#bill_other_data").val() !=''){
    	   $("#bill_other_data_error").css("display", "none");	
         return true;
    	}
    	else {
    	   $(premises_type).parent().children('.error').css("display", "none");	
    		$("#bill_other_data_error").css("display", "block");	
    		$("#bill_other_data_error").text("Please Enter Other Premises");
         return false;
    	}
    }
    else {
       $("#bill_other_data_error").css("display", "none");	
       $(premises_type).parent().children('.error').css("display", "none");	
       return true;
    }
       
   }else{
    $(premises_type).parent().children('.error').css("display", "block");
    $(premises_type).parent().children('.error').text("Please select Premises");
    return false; 
   }
}

function CheckRequestedLoad(requested_load){
	if($(requested_load).val()!=' ' && $(requested_load).val()!=null)
   {
    $(requested_load).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(requested_load).parent().children('.error').css("display", "block");
    $(requested_load).parent().children('.error').text("Please select Requested Load");
   return false; 
   }
}
function CheckLoadType(load_type){
	if($(load_type).val()!=' ' && $(load_type).val()!=null)
   {
    $(load_type).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(load_type).parent().children('.error').css("display", "block");
    $(load_type).parent().children('.error').text("Please select Type");
   return false; 
   }
}
function CheckContractDemand(contract_demand){
	if($(contract_demand).val()!=' ' && $(contract_demand).val()!=null)
   {
    $(contract_demand).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(contract_demand).parent().children('.error').css("display", "block");
    $(contract_demand).parent().children('.error').text("Please select Contract Demand");
   return false; 
   }
}
function CheckDemandType(contract_demand_type){
	if($(contract_demand_type).val()!=' ' && $(contract_demand_type).val()!=null)
   {
    $(contract_demand_type).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(contract_demand_type).parent().children('.error').css("display", "block");
    $(contract_demand_type).parent().children('.error').text("Please select Type");
   return false; 
   }
}
function CheckAddressProof() {
	
	flag_1 = 0
	var addProofList = document.getElementsByClassName('addproofclass')
	for(var i=0; addProofList[i]; ++i){
      if(addProofList[i].checked){
           flag_1 = 1
           break;
      }
   }
   if (flag_1 == 1) {
   	$("#addProofset_error").css("display", "none");
  		return true;
	}	
	else {
    	$("#addProofset_error").css("display", "block");	
      $("#addProofset_error").text("Please select at least one Address Proof");
   	return false; 
	}
}
function CheckIdProof() {
	flag_1 = 0
	var IdProofList = document.getElementsByClassName('idproofclass')
	for(var i=0; IdProofList[i]; ++i){
      if(IdProofList[i].checked){
           flag_1 = 1
           break;
      }
   }
   if (flag_1 == 1) {
   	$("#idProofset_error").css("display", "none");
  		return true;
	}	
	else {
    	$("#idProofset_error").css("display", "block");	
      $("#idProofset_error").text("Please select at least one Identity Proof");
   	return false; 
	}
}

function CheckDropeZone(){
    id_doc = 0;
	add_doc = 0;
    var checkboxes = document.getElementsByName("id_proof");
    for(i = 0;i<checkboxes.length;i++)
    {
        if(checkboxes[i].checked==1){
            id_doc = id_doc + 1;
        }
    }
    var checkboxes = document.getElementsByName("address_proof");
    for(i = 0;i<checkboxes.length;i++)
    {
        if(checkboxes[i].checked==1){
            add_doc = add_doc + 1;
        }
    }
    total_doc = add_doc + id_doc;
    if(total_doc != doc_length){
        if(total_doc > doc_length){
            doc_diff = total_doc - doc_length;
            $("#error_dropzone").css("display","block");
            $("#error_dropzone").text('Please attach '+doc_diff+' document');
            return false;
        }
        else if(total_doc < doc_length){
            doc_diff = doc_length - total_doc ;
            $("#error_dropzone").css("display","block");
            $("#error_dropzone").text('Please remove '+doc_diff+' document');
            return false;
        }
    }
    else{
        $("#error_dropzone").css("display","none");
        return true;
    }
}



$("#save-consumer").click(function(event)  {
	//console.log($("#consumer_form").serialize())

	bill_city = $("#bill_city").val()
	bill_pincode = $("#bill_pincode").val()

	if (validateData()) {
	event.preventDefault();  												
	
  			$.ajax({  				  
				  type	: "POST",
				   url : '/nscapp/save-new-consumer/',
 					data : $("#consumer_form").serialize()+'&bill_city='+bill_city+'&bill_pincode='+bill_pincode,
                     
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
$("#save-consumer-print").click(function(event)  {
	//console.log($("#consumer_form").serialize())

	console.log($("#attachment").val());
	return false;

	bill_city = $("#bill_city").val()
	bill_pincode = $("#bill_pincode").val()

	if (validateData()) {
	event.preventDefault();  												
	
  			$.ajax({  				  
				  type	: "POST",
				   url : '/nscapp/save-new-consumer/',
 					data : $("#consumer_form").serialize()+'&bill_city='+bill_city+'&bill_pincode='+bill_pincode,
                     
              success: function (response) {   
	              if(response.success=='true'){
							window.open("/nscapp/nsc-form/?nsc_id="+response.nsc_id,'_blank');
							location.reload() 
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

////////////////////////////////// NEW DROPZONE ///////////////////////////
        var uploaded_file_mb = 0;
        var uploaded_file1_mb = 0;
        var uploaded_file2_mb = 0;
        Dropzone.options.myAwesomeDropzone3 = {
            autoProcessQueue: true,
            uploadMultiple: true,
            paramName: "file",
            //maxFiles: 10,
            //maxFilesize: 2,
            method: 'post',
            parallelUploads: 1,
            url: '/nscapp/upload-consumer-docs/',
            dictDefaultMessage: "Drop or Browse up to 10 images (1MB or higher in size)",
            addRemoveLinks: true,
            acceptedFiles: "",
            dictInvalidFileType: 'This file type is not supported.',
            dictMaxFilesExceeded: "You can not upload more than 10 images.",

            init: function () {
                var myDropzone = this;
                var reordered_array = new Array();
                var temp_image_files = new Array();
                this.on("sending", function () {
                    return false;
                });

                /*this.on("totaluploadprogress", function (file,progress,bytesSent) {
                    uploaded_file1_mb = parseInt(bytesSent)/(1024*1024);
                    uploaded_file_mb = parseFloat(uploaded_file1_mb) + parseFloat(uploaded_file2_mb)+ parseFloat(display_image_size);;
                    $("#progress_bar").val(parseFloat(uploaded_file_mb));
                    if(uploaded_file_mb > 100){
                        $("#error-modal1").modal('show');
                        $("#error-message1").text("Uploaded file size exceeds limit of 100 MB");
                    }
                    progrss_count = parseFloat(uploaded_file_mb).toFixed(2) + "/100 MB"
                    $(".progress_count").text(progrss_count);
                    var alreadyUploadedTotalSize = getTotalPreviousUploadedFilesSize(bytesSent);
                });*/


                this.on("addedfile", function(file, response){
                    $(".txt_dropzone3").text("");
                    if (this.files.length) {
                        var i, len, pre;
                        for (i = 0, len = this.files.length; i < len - 1; i++){
                            if (this.files[i].name == file.name && this.files[i].size == file.size && this.files[i].lastModifiedDate.toString() == file.lastModifiedDate.toString()) {
                                this.removeFile(file);
                                //return (pre = file.previewElement) != null ? pre.parentNode.removeChild(file.previewElement) : void 0;
                            }
                        }
                    }
                    temp_image_files.push(file);
                });

                this.on("success", function (files, response) {
                    doc_length = doc_length + 1;
                    $('#attachment').val($('#attachment').val()+","+response.attachid);
                    $('a .dz-remove').attr('href','/remove-advert-image/?image_id='+response.attachid);
                    reordered_array.push(response.attachid);
                    $('#attachment').val(reordered_array);
                    $('#attachments').val(reordered_array);
                });

                this.on("removedfile", function(file){
                    deleting_image_id = reordered_array[temp_image_files.indexOf(file)];
                    $.ajax({
                        url: "/nscapp/remove-consumer-docs/?image_id="+deleting_image_id,
                        success: function(result){
                            doc_length = doc_length - 1;
                            arr = $('#attachment').val();
                            arr = arr.split(',');
                            console.log('Before Id Remove : '+ arr);
                            arr = jQuery.grep(arr, function(value) {
                                return value != deleting_image_id;
                            });
                            console.log('After Id Remove : '+ arr);
                            $('#attachment').val(arr);
                        }
                    });
                    arr =$('#attachments').val();
                    arr = arr.split(',');
                    arr = jQuery.grep(arr, function(value) {
                        return value != deleting_image_id;
                    });

                    $('#attachments').val(arr);
                    var index=myDropzone.files.length;
                    var temp_image_id = reordered_array[temp_image_files.indexOf(file)];

                    reordered_array = jQuery.grep(reordered_array, function(value) {
                        return value != temp_image_id;
                    });

                    temp_image_files = jQuery.grep(temp_image_files, function(value) {
                        return value != file;
                    });
                    $('#attachments').val(reordered_array);
                    if (myDropzone.files.length == 0){
                        $(".txt_dropzone3").text("Click or drag and drop to upload documents");
                    }
                });

                this.on("maxfilesexceeded", function (file) {
                    this.removeFiles(file);
                    $('#lbl_upl').css ("color", "red");
                });

                function getTotalPreviousUploadedFilesSize(bytesSent){
                    var totalSize = 0;
                    var image_space =bytesSent;
                    $("#image_space").val(image_space);
                }
            }
        }
        
        
       

