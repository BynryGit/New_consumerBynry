$.mask.definitions['h'] = "[A-Z]";    
    
function changevalidation() {
	 if ($('#applicant_aadhar_no:selected').text() == "Adhaar Card") { // Adhaar Card
		$("#applicant_aadhar_no").attr("placeholder","ex: 999999999999");
		$("#applicant_aadhar_no").mask("999999999999");

	 } 
	 if ($('#kyc').val() == "4") { // Election Card
		$("#kycnumber").attr("placeholder","ex: AAA9999999");
		$("#kycnumber").mask("hhh9999999");
	 }  
}       


function checkName(applicant_name){
 	var namePattern = /[A-Za-z]+/;  
	applicant_name = $(applicant_name).val()  
   if(namePattern.test(applicant_name)){

 	$(applicant_name).parent().children('.error').css("display", "none");
   return true;
   }else{

    $(applicant_name).parent().children('.error').css("display", "block");
    $(applicant_name).parent().children('.error').text("Please enter valid applicant name");
   return false; 
   }
}

function checkContactNo(contact_no){
   var namePattern = /[0-9]{11}/;  
	contactno = $(contact_no).val()  
   if(namePattern.test(contactno)){

 	$(contact_no).parent().children('.error').css("display", "none");
   return true;
   }else{

    $(contact_no).parent().children('.error').css("display", "block");
    $(contact_no).parent().children('.error').text("Please enter valid contact number");
   return false; 
   }
}

function checkHomePhone(home){
   var namePattern = /[0-9]{11}/;  
	contactno = $(home).val() 
	 	if(contactno=='')
	{
	return true;	
	} 
   else if(namePattern.test(contactno)){
 	$(home).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(home).parent().children('.error').css("display", "block");
    $(home).parent().children('.error').text("Please enter valid contact number");
   return false; 
   }
}

function checkgender(gender){
	if($(gender).val()!='')
   {
    $(gender).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(gender).parent().children('.error').css("display", "block");
    $(gender).parent().children('.error').text("Please select gender from list");
   return false; 
   }
}

function checkaddress(address_line1){
	if($(address_line1).val()!='')
   {
    $(address_line1).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(address_line1).parent().children('.error').css("display", "block");
    $(address_line1).parent().children('.error').text("Please enter valid address");
   return false; 
   }
}

function checkoccupation(applicant_occupation){

	if($(applicant_occupation).val()!='')
   {
    $(applicant_occupation).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(applicant_occupation).parent().children('.error').css("display", "block");
    $(applicant_occupation).parent().children('.error').text("Please select an occupation from list");
   return false; 
   }
}

function check_consumer_category(consumer_category){

	if($(consumer_category).val()!='')
   {
    $(consumer_category).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(consumer_category).parent().children('.error').css("display", "block");
    $(consumer_category).parent().children('.error').text("Please select a consumer category from list");
   return false; 
   }
}

function check_consumer_service(consumer_service){

	if($(consumer_service).val()!='')
   {
    $(consumer_service).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(consumer_service).parent().children('.error').css("display", "block");
    $(consumer_service).parent().children('.error').text("Please select a consumer service from list");
   return false; 
   }
}

function check_consumer_supply_type(consumer_supply_type){

	if($(consumer_supply_type).val()!='')
   {
    $(consumer_supply_type).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(consumer_supply_type).parent().children('.error').css("display", "block");
    $(consumer_supply_type).parent().children('.error').text("Please select a consumer supply type from list");
   return false; 
   }
}

function check_consumer_subcategory(consumer_subcategory){

	if($(consumer_subcategory).val()!='')
   {
    $(consumer_subcategory).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(consumer_subcategory).parent().children('.error').css("display", "block");
    $(consumer_subcategory).parent().children('.error').text("Please select a consumer subcategory from list");
   return false; 
   }
}

function check_premises_type(premises_type){

	if($(premises_type).val()!='')
   {
    $(premises_type).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(premises_type).parent().children('.error').css("display", "block");
    $(premises_type).parent().children('.error').text("Please select a premises type from list");
   return false; 
   }
}

function check_city(city){
	if($(city).val()!='')
   {
    $(city).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(city).parent().children('.error').css("display", "block");
    $(city).parent().children('.error').text("Please select a city from list");
   return false; 
   }
}

function check_pincode(pincode){
	if($(pincode).val()!='')
   {
    $(pincode).parent().children('.error').css("display", "none");
   return true;
   }else{
    $(pincode).parent().children('.error').css("display", "block");
    $(pincode).parent().children('.error').text("Please select a pincode from list");
   return false; 
   }
}


function checkEmail(email){
	Email = $(email).val()
   var namePattern = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;  
   	if(Email=='')
	{
	return true;	
	}  
   else if(namePattern.test(Email)){
      $(email).parent().children('.error').css("display", "none");
   return true;
   }else{
 	$(email).parent().children('.error').css("display", "block");
   $(email).parent().children('.error').text("Please enter valid email");
   return false; 
   }
}
	

function validateData(){

	if(checkName("#applicant_name")&&checkEmail("#email")){
		return true;	
	}
	return false;
}
