$(document).ready(function() {
	// CSRF Token
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	$.ajaxSetup({
	    crossDomain: false, // obviates need for sameOrigin test
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type)) {
	            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	        }
	    }
	});

	// Ajax
	$(document).ajaxSend(function(elm, xhr, s){
	    if (s.type == "POST") {
	        s.data += s.data?"&":"";
	        s.data += "_token=" + $('#csrf-token').val();
	    }
	});

	// Datepicker
	$(function() {
	    $( ".datepicker" ).datepicker({
	      changeMonth: true,
	      changeYear: true,
	      yearRange: "-100:+0",
	    });
	  });

	// Requremetns Page
	$('.requirements-cb').change(function() {
		if($('.requirements-cb').is(':checked')){
			// alert('checked');
			$( ".requirement-continue" ).prop( "disabled", false );
		}else{
			// alert('unchecked');
			$( ".requirement-continue" ).prop( "disabled", true );
		}
	});

	$('.requirement-continue').on('click', function() {
		$.ajax({
			type: "POST",
			url: "/create_survey/"
		}).success(function(res){
			alert('servey created!');
		});
	});

	// About Page
	$('.about-continue').on('click', function() {
		$('.content-form').each(function(){
			$(this).submit();
		});
	});

	// Head of Household, Household Page	
	$("#id_head_of_household_member_info__0-ssn").mask("999-99-9999");
	$("#id_alternate_contact_info__0-alt_contact_home_phone").mask("(999) 999-9999");
	$("#id_alternate_contact_info__0-alt_contact_mobile_phone").mask("(999) 999-9999");
	$("#id_head_of_household_member_info__0-mobile_phone").mask("(999) 999-9999");
	$("#id_household_member__3-home_phone").mask("(999) 999-9999");
	$("#id_household_member__3-zip_code").mask("99999");

	$(".am-ssn").mask("999-99-9999");
	$(".am-mobilephone").mask("(999) 999-9999");

	$('#id_head_of_household_member_info__0-household_relationship').on('change', function() {
		if($(this).val() == "other") {
			$('#id_head_of_household_member_info__0-household_relationship_other').attr('required', '');
		} else {
			$('#id_head_of_household_member_info__0-household_relationship_other').attr('required', null);
		}
	});

	$('#id_household_member__1-housing').on('change', function() {
		if($(this).val() == "other") {
			$('#id_household_member__1-housing_other').attr('required', '');
		} else {
			$('#id_household_member__1-housing_other').attr('required', null);
		}
	});

	$('#id_household_member__1-type_of_household').on('change', function() {
		if($(this).val() == "other") {
			$('#id_household_member__1-type_of_household_other').attr('required', '');
		} else {
			$('#id_household_member__1-type_of_household_other').attr('required', null);
		}
	});

	$('#id_alternate_contact_info__0-preferred_phone').on('change', function() {
		if($(this).val() == "home") {
			$('#id_alternate_contact_info__0-alt_contact_home_phone').attr('required', '');
			$('#id_alternate_contact_info__0-alt_contact_mobile_phone').attr('required', null);
		} if($(this).val() == "mobile") {
			$('#id_alternate_contact_info__0-alt_contact_home_phone').attr('required', null);
			$('#id_alternate_contact_info__0-alt_contact_mobile_phone').attr('required', '');
		}
	});

	// Add Member Page
	$('.am-submit').on('click', function(e) {
	    var firstName = $('.am-fn');
	    var lastName = $('.am-ln');
	    var ssn = $('.am-ssn');
	    var bday = $('.am-bday');
	    var gender = $("input:radio[name=am-gender]:checked").val()
	    var mobilephone = $('.am-mobilephone');
	    var relationship = $('.am-rel');

	    if(!firstName.val() || !lastName.val() || !ssn.val() || !mobilephone.val() || !bday.val() || !gender || !relationship.val()) {
	    	// alert('Please input all the required informations!');
	    } else {
	    	$('.modal').modal('toggle');
	    	$.ajax({
				type: "POST",
				data: {'firstname': firstName.val(),
						'lastname': lastName.val(),
						'ssn': ssn.val(),
						'mobile': mobilephone.val(),
						'bday': bday.val(),
						'gender': gender,
						'relationship': relationship.val()},
				url: "/csbg_survey/add_member/"
			}).success(function(res){
				// alert('Member added!');
				$('.tb-div').append("<div></div>");
				$('.tb-div > div:last-child').append("<div class='col-md-4 membernames-div'><span>" + firstName.val() + " " + lastName.val() + "</span></div>");
				$('.tb-div > div:last-child').append("<div class='col-md-3 memberbdays-div'><span>" + bday.val() + "</span></div>");
				$('.tb-div > div:last-child').append("<div class='col-md-3 memberrels-div'><span>" + relationship.val() + "</span></div>");
				$('.tb-div > div:last-child').append("<div class='col-md-2 memberdels-div'><button class='am-delete btn' type='button'>Delete</button></div>");
			});
	    }
	});

	$(document).on('click','.am-delete',function(){
		var name_temp = $(this).parent().parent().children().first().first();
		var name = name_temp.text().replace(/\s+/g, " ").replace(/^\s|\s$/g, "");
		var bday_temp = $(this).parent().parent().children().eq(1).first();
		var bday = bday_temp.text().replace(/\s+/g, " ").replace(/^\s|\s$/g, "");
		var del_temp = $(this).parent().parent();
		$.ajax({
			type: "POST",
			data: {'name': name, 'bday': bday},
			url: "/csbg_survey/delete_member/"
		}).success(function(res){			
			del_temp.remove();
		});
	});

	// Head of Household can't be deleted
	$('.tb-div').children().first().children().last().css('display', 'none');
	$('#id_1-first_name').val('aaa');
	$('#id_1-last_name').val('bbb');
	$('#id_1-ssn').val('111111111');
	$('#id_1-birthdate').val('09/09/1990');
	$('#id_1-gender').val('male');
	$('.hm-fields').hide();

	// Add member info page
	$( ".member-select" ).change(function() {
		var current_member_index = $('.cd-member-index').attr('value');
		var to_show_member_index = $(".member-select option:selected").index();
		// alert('current member index - ' + current_member_index + '   to show member index - ' + to_show_member_index);

		var education = $('#id_household_member_demographics__2-education option:selected').val();
		var race = $('#id_household_member_demographics__2-race option:selected').val();
		var ethnicity = $('#id_household_member_demographics__2-ethnicity option:selected').val();
		var employment = $('#id_household_member_income__2-employment option:selected').val();
		var payperiod = $('#id_household_member_income__2-pay_period option:selected').val();
		var income_other = $('#id_household_member_income__2-other_income_other').val();

		var no_health_insurance = $('#id_household_member_demographics__2-no_health_insurance').is(':checked');
		var disabled = $('#id_household_member_demographics__2-disabled').is(':checked');
		var veteran = $('#id_household_member_demographics__2-veteran').is(':checked');
		
		var other_income_cash = $('#id_household_member_income__2-other_income_cash').is(':checked');
		var other_income_snap = $('#id_household_member_income__2-other_income_snap').is(':checked');
		var other_income_tanf = $('#id_household_member_income__2-other_income_tanf').is(':checked');
		var other_income_ss = $('#id_household_member_income__2-other_income_ss').is(':checked');
		var other_income_ssdi = $('#id_household_member_income__2-other_income_ssdi').is(':checked');
		var other_income_medicare = $('#id_household_member_income__2-other_income_medicare').is(':checked');
		var other_income_other_agencies = $('#id_household_member_income__2-other_income_other_agencies').is(':checked');
		var other_income_gifts = $('#id_household_member_income__2-other_income_gifts').is(':checked');
		var other_income_unemployment = $('#id_household_member_income__2-other_income_unemployment').is(':checked');
		var other_income_workers_comp = $('#id_household_member_income__2-other_income_workers_comp').is(':checked');
		var other_income_pensions = $('#id_household_member_income__2-other_income_pensions').is(':checked');
		var other_income_job_training = $('#id_household_member_income__2-other_income_job_training').is(':checked');
		var other_income_military_allotments = $('#id_household_member_income__2-other_income_military_allotments').is(':checked');
		var other_income_va = $('#id_household_member_income__2-other_income_va').is(':checked');
		var other_income_insurance = $('#id_household_member_income__2-other_income_insurance').is(':checked');
		var other_income_alimony = $('#id_household_member_income__2-other_income_alimony').is(':checked');
		var other_income_foster_payments = $('#id_household_member_income__2-other_income_foster_payments').is(':checked');
		var other_income_child_support = $('#id_household_member_income__2-other_income_child_support').is(':checked');
		var other_income_college_scholarship = $('#id_household_member_income__2-other_income_college_scholarship').is(':checked');
		var other_income_student_loans = $('#id_household_member_income__2-other_income_student_loans').is(':checked');

		if(education == '' 
		|| race == ''
		|| ethnicity == ''
		|| employment == ''
		|| payperiod == ''
		|| !income_other){
			alert('Please input all the required informations');
			// Reverse the dropdown change action
			$(this).val($('.member-select option').eq(current_member_index).val());
		}else{
			$.ajax({
				type: "POST",
				data: {'education': education,
				'race': race,
				'ethnicity': ethnicity,
				'employment': employment,
				'payperiod': payperiod,
				'income_other': income_other,

				'no_health_insurance': no_health_insurance,
				'disabled': disabled,
				'veteran': veteran,

				'other_income_cash': other_income_cash,
				'other_income_snap': other_income_snap,
				'other_income_tanf': other_income_tanf,
				'other_income_ss': other_income_ss,
				'other_income_ssdi': other_income_ssdi,
				'other_income_medicare': other_income_medicare,
				'other_income_other_agencies': other_income_other_agencies,
				'other_income_gifts': other_income_gifts,
				'other_income_unemployment': other_income_unemployment,
				'other_income_workers_comp': other_income_workers_comp,
				'other_income_pensions': other_income_pensions,
				'other_income_job_training': other_income_job_training,
				'other_income_military_allotments': other_income_military_allotments,
				'other_income_va': other_income_va,
				'other_income_insurance': other_income_insurance,
				'other_income_alimony': other_income_alimony,
				'other_income_foster_payments': other_income_foster_payments,
				'other_income_child_support': other_income_child_support,
				'other_income_college_scholarship': other_income_college_scholarship,
				'other_income_student_loans': other_income_student_loans,
				'current_member_index': current_member_index,
				'to_show_member_index': to_show_member_index},
				url: "/csbg_survey/add_change_member/"
			}).success(function(res){
				if(res['education'] === undefined){ // If no data, clear all the tags
					clear_all_tags();
				} else { // If no data, clear all the tags
					set_all_tags(res);
				}
			});

			$.ajax({
				type: "POST",
				url: "/csbg_survey/get_member_status/"
			}).success(function(res){
				if(res['completed'] == 'true'){ // If all member data are completed
					$('.household-btns-div > button:last').prop('disabled', false);
					$('.household-btns-div > input').prop('disabled', false);
				} else { // If all member data are not completed yet
					$('.household-btns-div > button:last').prop('disabled', true);
					$('.household-btns-div > input').prop('disabled', true);
				}
			});

		  	$('.cd-member-index').attr('value', $(".member-select option:selected").index());
		}
	});

	var clear_all_tags = function(){
		$('#id_household_member_demographics__2-education :first').prop('selected', true);
		$('#id_household_member_demographics__2-race :first').prop('selected', true);
		$('#id_household_member_demographics__2-ethnicity :first').prop('selected', true);
		$('#id_household_member_income__2-employment :first').prop('selected', true);
		$('#id_household_member_income__2-pay_period :first').prop('selected', true);
		$('#id_household_member_income__2-other_income_other').val('');

		$('#id_household_member_demographics__2-no_health_insurance').prop('checked', false);
		$('#id_household_member_demographics__2-disabled').prop('checked', false);
		$('#id_household_member_demographics__2-veteran').prop('checked', false);
		
		$('#id_household_member_income__2-other_income_cash').prop('checked', false);
		$('#id_household_member_income__2-other_income_snap').prop('checked', false);
		$('#id_household_member_income__2-other_income_tanf').prop('checked', false);
		$('#id_household_member_income__2-other_income_ss').prop('checked', false);
		$('#id_household_member_income__2-other_income_ssdi').prop('checked', false);
		$('#id_household_member_income__2-other_income_medicare').prop('checked', false);
		$('#id_household_member_income__2-other_income_other_agencies').prop('checked', false);
		$('#id_household_member_income__2-other_income_gifts').prop('checked', false);
		$('#id_household_member_income__2-other_income_unemployment').prop('checked', false);
		$('#id_household_member_income__2-other_income_workers_comp').prop('checked', false);
		$('#id_household_member_income__2-other_income_pensions').prop('checked', false);
		$('#id_household_member_income__2-other_income_job_training').prop('checked', false);
		$('#id_household_member_income__2-other_income_military_allotments').prop('checked', false);
		$('#id_household_member_income__2-other_income_va').prop('checked', false);
		$('#id_household_member_income__2-other_income_insurance').prop('checked', false);
		$('#id_household_member_income__2-other_income_alimony').prop('checked', false);
		$('#id_household_member_income__2-other_income_foster_payments').prop('checked', false);
		$('#id_household_member_income__2-other_income_child_support').prop('checked', false);
		$('#id_household_member_income__2-other_income_college_scholarship').prop('checked', false);
		$('#id_household_member_income__2-other_income_student_loans').prop('checked', false);
	}

	var set_all_tags = function(res){
		$('#id_household_member_demographics__2-education').val(res['education']);
		$('#id_household_member_demographics__2-race').val(res['race']);
		$('#id_household_member_demographics__2-ethnicity').val(res['ethnicity']);
		$('#id_household_member_income__2-employment').val(res['employment']);
		$('#id_household_member_income__2-pay_period').val(res['payperiod']);
		$('#id_household_member_income__2-other_income_other').val(res['income_other']);

		$('#id_household_member_demographics__2-no_health_insurance').prop('checked', (res['no_health_insurance'] === 'true'));
		$('#id_household_member_demographics__2-disabled').prop('checked', (res['disabled'] === 'true'));
		$('#id_household_member_demographics__2-veteran').prop('checked', (res['veteran'] === 'true'));
		
		$('#id_household_member_income__2-other_income_cash').prop('checked', (res['other_income_cash'] === 'true'));
		$('#id_household_member_income__2-other_income_snap').prop('checked', (res['other_income_snap'] === 'true'));
		$('#id_household_member_income__2-other_income_tanf').prop('checked', (res['other_income_tanf'] === 'true'));
		$('#id_household_member_income__2-other_income_ss').prop('checked', (res['other_income_ss'] === 'true'));
		$('#id_household_member_income__2-other_income_ssdi').prop('checked', (res['other_income_ssdi'] === 'true'));
		$('#id_household_member_income__2-other_income_medicare').prop('checked', (res['other_income_medicare'] === 'true'));
		$('#id_household_member_income__2-other_income_other_agencies').prop('checked', (res['other_income_other_agencies'] === 'true'));
		$('#id_household_member_income__2-other_income_gifts').prop('checked', (res['other_income_gifts'] === 'true'));
		$('#id_household_member_income__2-other_income_unemployment').prop('checked', (res['other_income_unemployment'] === 'true'));
		$('#id_household_member_income__2-other_income_workers_comp').prop('checked', (res['other_income_workers_comp'] === 'true'));
		$('#id_household_member_income__2-other_income_pensions').prop('checked', (res['other_income_pensions'] === 'true'));
		$('#id_household_member_income__2-other_income_job_training').prop('checked', (res['other_income_job_training'] === 'true'));
		$('#id_household_member_income__2-other_income_military_allotments').prop('checked', (res['other_income_military_allotments'] === 'true'));
		$('#id_household_member_income__2-other_income_va').prop('checked', (res['other_income_va'] === 'true'));
		$('#id_household_member_income__2-other_income_insurance').prop('checked', (res['other_income_insurance'] === 'true'));
		$('#id_household_member_income__2-other_income_alimony').prop('checked', (res['other_income_alimony'] === 'true'));
		$('#id_household_member_income__2-other_income_foster_payments').prop('checked', (res['other_income_foster_payments'] === 'true'));
		$('#id_household_member_income__2-other_income_child_support').prop('checked', (res['other_income_child_support'] === 'true'));
		$('#id_household_member_income__2-other_income_college_scholarship').prop('checked', (res['other_income_college_scholarship'] === 'true'));
		$('#id_household_member_income__2-other_income_student_loans').prop('checked', (res['other_income_student_loans'] === 'true'));
	}

});










