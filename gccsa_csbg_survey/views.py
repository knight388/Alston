import os
import json
import logging
import datetime
import shutil
import zipfile
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.core.files import File
from formtools.wizard.views import SessionWizardView
from .forms import HeadOfHouseholdMemberInfo, AlternateContactInfo, HouseholdInfo, HouseholdReferralInfo, HeadOfHousehold, Household, HouseholdMemberDemographicsInfo, HouseholdMemberAdd
from .models import Survey, Org, Document
from .models import EDUCATION, ETHNICITY, RACE, EMPLOYMENT, PAY_PERIOD, HOUSING_TYPES, HOUSEHOLD_TYPES, GCCSA_HISTORY
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from reportlab.pdfgen import canvas
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.db import models
from os.path import basename
logger = logging.getLogger(__name__)
# member_names_be = []
# member_ssns_be = []
# member_mobiles_be = []
# member_genders_be = []
# member_bdays_be = []
# member_rels_be = []
# members_be = []


def about(request):

	config = get_config()
	title = config['org']['survey']['csbg']['title']
	about_file_name = config['org']['survey']['csbg']['about_file']

	if about_file_name != "":
		file = open(get_tpl_url() + about_file_name)
		return render(request, "about.html", {"about_content": file.read(), "title": title})
	else:
		return redirect(requirement)


def requirement(request):
	config = get_config()
	title = 'Requirements'
	requirements_file_name = config['org']['survey']['csbg']['requirements_file']
	if len(requirements_file_name) > 0:
		file = open(get_tpl_url() + requirements_file_name)
		return render(request, "requirement.html", {"requirements_content": file.read(), "title": title})
	else:
		return redirect(handler404)


def create_survey(request):
	config = get_config()
	org_symbol = config['org']['org_symbol']
	org_record = Org.objects.get(org_symbol=org_symbol)
	now_time = datetime.datetime.now()
	now_year_last2 = last_2_digits(now_time.year)
	if Survey.objects.count() > 0:
		logger.error("***  OUTPUT - has_record *** : Yes")
		survey_last_id = Survey.objects.latest('id').id
		survey_id = int(str(now_year_last2) + str(survey_last_id + 1))
	else:
		logger.error("***  OUTPUT - has_recored *** : No")
		survey_id = int(str(now_year_last2) + '1')
	request.session['member_names_be'] = []
	request.session['member_ssns_be'] = []
	request.session['member_mobiles_be'] = []
	request.session['member_bdays_be'] = []
	request.session['member_genders_be'] = []
	request.session['member_rels_be'] = []
	request.session['members_be'] = []
	survey_record = Survey.objects.create(org_id=org_record.id, created=now_time, submitted=now_time, survey_id=survey_id)
	request.session['survey_id'] = survey_record.id
	
	#response = HttpResponse(survey_record, content_type='text/plain')
	#response.status_code = 201
	#return response
	
	return survey_record


def add_member(request):
	req_dict = request.POST.dict()
	member_names_be = request.session['member_names_be']
	member_ssns_be = request.session['member_ssns_be']
	member_mobiles_be = request.session['member_mobiles_be']
	member_bdays_be = request.session['member_bdays_be']
	member_genders_be = request.session['member_genders_be']
	member_rels_be = request.session['member_rels_be']
	members_be = request.session['members_be']

	logger.error("***  OUTPUT - before save - member_names *** : " + str(request.session['member_names_be']))
	logger.error("***  OUTPUT - before save - member_ssns_be *** : " + str(request.session['member_ssns_be']))
	logger.error("***  OUTPUT - before save - member_mobiles_be *** : " + str(request.session['member_mobiles_be']))
	logger.error("***  OUTPUT - before save - member_bdays_be *** : " + str(request.session['member_bdays_be']))
	logger.error("***  OUTPUT - before save - member_genders_be *** : " + str(request.session['member_genders_be']))
	logger.error("***  OUTPUT - before save - member_rels_be *** : " + str(request.session['member_rels_be']))
	logger.error("***  OUTPUT - before save - members_be *** : " + str(request.session['members_be']))
	member_names_be.append(req_dict['firstname'] + ' ' + req_dict['lastname'])
	member_ssns_be.append(req_dict['ssn'])
	member_mobiles_be.append(req_dict['mobile'])
	member_bdays_be.append(req_dict['bday'])
	member_genders_be.append(req_dict['gender'])
	member_rels_be.append(req_dict['relationship'])
	members_be.append(req_dict['firstname'] + ' ' + req_dict['lastname'])
	request.session['member_names_be'] = member_names_be
	request.session['member_ssns_be'] = member_ssns_be
	request.session['member_mobiles_be'] = member_mobiles_be
	request.session['member_bdays_be'] = member_bdays_be
	request.session['member_genders_be'] = member_genders_be
	request.session['member_rels_be'] = member_rels_be
	request.session['members_be'] = members_be
	logger.error("***  OUTPUT - after save - member_names *** : " + str(request.session['member_names_be']))
	logger.error("***  OUTPUT - after save - member_ssns_be *** : " + str(request.session['member_ssns_be']))
	logger.error("***  OUTPUT - after save - member_mobiles_be *** : " + str(request.session['member_mobiles_be']))
	logger.error("***  OUTPUT - after save - member_bdays_be *** : " + str(request.session['member_bdays_be']))
	logger.error("***  OUTPUT - after save - member_genders_be *** : " + str(request.session['member_genders_be']))
	logger.error("***  OUTPUT - after save - member_rels_be *** : " + str(request.session['member_rels_be']))
	logger.error("***  OUTPUT - after save - members_be *** : " + str(request.session['members_be']))
	log_current_status()
	response = HttpResponse('', content_type='text/plain')
	response.status_code = 201
	return response


def delete_member(request):
	req_dict = request.POST.dict()
	member_names_be = request.session['member_names_be']
	member_ssns_be = request.session['member_ssns_be']
	member_mobiles_be = request.session['member_mobiles_be']
	member_bdays_be = request.session['member_bdays_be']
	member_genders_be = request.session['member_genders_be']
	member_rels_be = request.session['member_rels_be']
	members_be = request.session['members_be']
	logger.error("***  OUTPUT - before delete - member_names *** : " + str(request.session['member_names_be']))
	logger.error("***  OUTPUT - before delete - member_ssns_be *** : " + str(request.session['member_ssns_be']))
	logger.error("***  OUTPUT - before delete - member_mobiles_be *** : " + str(request.session['member_mobiles_be']))
	logger.error("***  OUTPUT - before delete - member_bdays_be *** : " + str(request.session['member_bdays_be']))
	logger.error("***  OUTPUT - before delete - member_genders_be *** : " + str(request.session['member_genders_be']))
	logger.error("***  OUTPUT - before delete - member_rels_be *** : " + str(request.session['member_rels_be']))
	logger.error("***  OUTPUT - before delete - members_be *** : " + str(request.session['members_be']))

	index_list = list_duplicates_of(member_names_be, str(req_dict['name']))
	logger.error("***  OUTPUT - before delete - members_be *** : " + str(index_list))

	# Delete the member with 'name' and 'bday' info
	for index in index_list:
		logger.error("***  OUTPUT - current index *** : " + str(index))
		logger.error("***  OUTPUT - current member_bdays_be *** : " + str(member_bdays_be[index]))
		if member_bdays_be[index] == req_dict['bday']:
			member_names_be.pop(index)
			member_ssns_be.pop(index)
			member_mobiles_be.pop(index)
			member_bdays_be.pop(index)
			member_genders_be.pop(index)
			member_rels_be.pop(index)
			members_be.pop(index)
			break
	request.session['member_names_be'] = member_names_be
	request.session['member_ssns_be'] = member_ssns_be
	request.session['member_mobiles_be'] = member_mobiles_be
	request.session['member_bdays_be'] = member_bdays_be
	request.session['member_genders_be'] = member_genders_be
	request.session['member_rels_be'] = member_rels_be
	request.session['members_be'] = members_be
	logger.error("***  OUTPUT - after delete - member_names *** : " + str(request.session['member_names_be']))
	logger.error("***  OUTPUT - after delete - member_ssns_be *** : " + str(request.session['member_ssns_be']))
	logger.error("***  OUTPUT - after delete - member_mobiles_be *** : " + str(request.session['member_mobiles_be']))
	logger.error("***  OUTPUT - after delete - member_bdays_be *** : " + str(request.session['member_bdays_be']))
	logger.error("***  OUTPUT - after delete - member_genders_be *** : " + str(request.session['member_genders_be']))
	logger.error("***  OUTPUT - after delete - member_rels_be *** : " + str(request.session['member_rels_be']))
	logger.error("***  OUTPUT - after delete - members_be *** : " + str(request.session['members_be']))
	log_current_status()
	response = HttpResponse('', content_type='text/plain')
	response.status_code = 201
	return response


def add_change_member(request):
	req_dict = request.POST.dict()

	# Get the index info from data
	current_member_index = int(req_dict['current_member_index'])
	to_show_member_index = int(req_dict['to_show_member_index'])
	# Delete the index info from the req data
	req_dict.pop('current_member_index')
	req_dict.pop('to_show_member_index')
	members_be = request.session['members_be']
	logger.error("***  OUTPUT - before save - members_be *** : " + str(request.session['members_be']))

	members_be.pop(current_member_index)
	members_be.insert(current_member_index, req_dict)
	request.session['members_be'] = members_be
	logger.error("***  OUTPUT - before save - members_be *** : " + str(request.session['members_be']))
	log_current_status()
	logger.error("***  OUTPUT - data current *** : " + str(members_be[current_member_index]))
	logger.error("***  OUTPUT - data to_show *** : " + str(members_be[to_show_member_index]))
	# logger.error("***  OUTPUT - data_type current *** : " + str(isinstance(members_be[current_member_index], dict)))
	# logger.error("***  OUTPUT - data_type to_show *** : " + str(isinstance(members_be[to_show_member_index], dict)))
	res_data = members_be[to_show_member_index]
	if(isinstance(res_data, dict)):
		response = JsonResponse(res_data)
	else:
		response = JsonResponse({})
	response.status_code = 201
	return response


def get_default_member(request):
	members_be = request.session['members_be']
	logger.error("***  OUTPUT - members_be *** : " + str(request.session['members_be']))
	res_data = members_be[0]
	log_current_status()
	if(isinstance(res_data, dict)):
		response = JsonResponse(res_data)
	else:
		response = JsonResponse({})
	response.status_code = 201
	return response


def get_member_status(request):
	members_be = request.session['members_be']
	logger.error("***  OUTPUT - members_be *** : " + str(request.session['members_be']))
	if(all(isinstance(x, dict) for x in members_be)):
		response = JsonResponse({'completed': 'true'})
	else:
		response = JsonResponse({'completed': 'false'})
	response.status_code = 201
	return response


def get_pdf(request):
	pdf_file = open((get_cur_survey_url() + '/{}').format('survey.pdf'), 'rb')
	response = HttpResponse(pdf_file.read(), content_type='application/pdf')
	response['Content-Disposition'] = 'inline;filename=some_file.pdf'
	return response


def handler404(request):
	response = render_to_response('404.html')
	response.status_code = 404
	return response


TEMPLATES = ["head_of_household_page.html",
			 "household_member_page.html",
			 "household_member_add_page.html",
			 "household_page.html",
			 "upload_doc_page.html",
			 "verify_info_page.html"]


class InformationWizard(SessionWizardView):
	file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'wizard_doc'))
	# template_name = "template.html"

	def get_template_names(self):
		logger.error("***  OUTPUT - current_page *** : " + self.steps.current)
		return [TEMPLATES[int(self.steps.current)]]

	def done(self, form_list, **kwargs):
		PROJECT_ROOT = get_project_root()
		wizard_doc_url = PROJECT_ROOT + '/wizard_doc'
		for root, dirs, files in os.walk(wizard_doc_url):
			for file in files:
				path_file = os.path.join(root, file)
				shutil.copy2(path_file, get_cur_survey_url())
		config = get_config()
		PROJECT_ROOT = get_project_root()
		survey_id = Survey.objects.latest('id').survey_id
		zf = zipfile.ZipFile(get_cur_survey_zip_url() + '/survey_' + str(survey_id) + ".zip", "w")
		for dirname, subdirs, files in os.walk(get_cur_survey_url()):
			for filename in files:
				zf.write(os.path.join(dirname, filename), basename(os.path.join(dirname, filename)))
		zf.close()
		zip_url = get_cur_survey_zip_url() + '/survey_' + str(survey_id) + ".zip"
		form_data = process_form_data(form_list)
		return render_to_response('done.html', {'form_data': form_data, 'zip_url': zip_url})
	# def get_form_initial(self, step):
	# initial = {}
	# logger.error("***  OUTPUT - current 002 *** : " + step)
	#   if step == '1':
	#	 prev_data = self.storage.get_step_data('0')
	#	 first_name = prev_data.get('head_of_household_member_info__0-first_name','')
	#	 last_name = prev_data.get('head_of_household_member_info__0-last_name','')
	#   return self.initial_dict.get(step, initial)

	def get_context_data(self, form, **kwargs):
		if 'survey_id' not in self.request.session:
			create_survey(self.request)
		
		context = super(InformationWizard, self).get_context_data(form=form, **kwargs)
		if self.steps.current == '1':
			prev_data = self.storage.get_step_data('0')
			first_name = prev_data.get('head_of_household_member_info__0-first_name', '')
			last_name = prev_data.get('head_of_household_member_info__0-last_name', '')
			ssn = prev_data.get('head_of_household_member_info__0-ssn', '')
			mobile = prev_data.get('head_of_household_member_info__0-mobile_phone', '')
			bday = prev_data.get('head_of_household_member_info__0-birthdate', '')
			gender = prev_data.get('head_of_household_member_info__0-gender', '')
			logger.error("***  OUTPUT - gender *** : " + str(gender))
			# logger.error("***  OUTPUT - member_names_be *** : " + str(member_names_be))
			# logger.error("***  OUTPUT - member_bdays_be *** : " + str(member_bdays_be))
			# logger.error("***  OUTPUT - member_rels_be *** : " + str(member_rels_be))
			# logger.error("***  OUTPUT - members_be *** : " + str(members_be))
			log_current_status()
			member_names_be = self.request.session['member_names_be']
			member_ssns_be = self.request.session['member_ssns_be']
			member_mobiles_be = self.request.session['member_mobiles_be']
			member_bdays_be = self.request.session['member_bdays_be']
			member_genders_be = self.request.session['member_genders_be']
			member_rels_be = self.request.session['member_rels_be']
			members_be = self.request.session['members_be']
			logger.error("***  OUTPUT - before show - member_names [self.req.ses] *** : " + str(self.request.session['member_names_be']))
			logger.error("***  OUTPUT - before show - member_ssns_be [self.req.ses] *** : " + str(self.request.session['member_ssns_be']))
			logger.error("***  OUTPUT - before show - member_mobiles_be [self.req.ses] *** : " + str(self.request.session['member_mobiles_be']))
			logger.error("***  OUTPUT - before show - member_bdays_be [self.req.ses] *** : " + str(self.request.session['member_bdays_be']))
			logger.error("***  OUTPUT - before show - member_genders_be [self.req.ses] *** : " + str(self.request.session['member_genders_be']))
			logger.error("***  OUTPUT - before show - member_rels_be [self.req.ses] *** : " + str(self.request.session['member_rels_be']))
			logger.error("***  OUTPUT - before show - members_be [self.req.ses] *** : " + str(self.request.session['members_be']))
			names = []
			bdays = []
			rels = []
			members = [names, bdays, rels]
			if not member_rels_be:
				member_names_be.insert(0, first_name + " " + last_name)
				member_ssns_be.insert(0, ssn)
				member_mobiles_be.insert(0, mobile)
				member_bdays_be.insert(0, bday)
				member_genders_be.insert(0, gender)
				member_rels_be.insert(0, 'HeadOfHousehold')
				members_be.insert(0, member_names_be[0])
				logger.error("*** output HeadOfHousehold member info added ***")
			for name in member_names_be:
				members[0].append(name)
			for bday in member_bdays_be:
				members[1].append(bday)
			for rel in member_rels_be:
				members[2].append(rel)
			self.request.session['member_names_be'] = member_names_be
			self.request.session['member_ssns_be'] = member_ssns_be
			self.request.session['member_mobiles_be'] = member_mobiles_be
			self.request.session['member_bdays_be'] = member_bdays_be
			self.request.session['member_genders_be'] = member_genders_be
			self.request.session['member_rels_be'] = member_rels_be
			self.request.session['members_be'] = members_be
			logger.error("***  OUTPUT - after show - member_names [self.req.ses] *** : " + str(self.request.session['member_names_be']))
			logger.error("***  OUTPUT - after show - member_ssns_be [self.req.ses] *** : " + str(self.request.session['member_ssns_be']))
			logger.error("***  OUTPUT - after show - member_mobiles_be [self.req.ses] *** : " + str(self.request.session['member_mobiles_be']))
			logger.error("***  OUTPUT - after show - member_bdays_be [self.req.ses] *** : " + str(self.request.session['member_bdays_be']))
			logger.error("***  OUTPUT - after show - member_genders_be [self.req.ses] *** : " + str(self.request.session['member_genders_be']))
			logger.error("***  OUTPUT - after show - member_rels_be [self.req.ses] *** : " + str(self.request.session['member_rels_be']))
			logger.error("***  OUTPUT - after show - members_be [self.req.ses] *** : " + str(self.request.session['members_be']))
			log_current_status()

			# for bday in members[1]:
			#   str1 = ''.join(bday)
			#   logger.error("*** output ***" + str())
			context.update({'members': members, 'mem_count': range(0, len(members[1]))})
		if self.steps.current == '2':
			member_names_be = self.request.session['member_names_be']
			member_bdays_be = self.request.session['member_bdays_be']
			member_rels_be = self.request.session['member_rels_be']
			context.update({'member_names_be': member_names_be, 'member_bdays_be': member_bdays_be, 'member_rels_be': member_rels_be})
		if self.steps.current == '5':
			prev_data = self.storage.get_step_data('0')
			first_name = prev_data.get('head_of_household_member_info__0-first_name', '')
			last_name = prev_data.get('head_of_household_member_info__0-last_name', '')
			ssn = prev_data.get('head_of_household_member_info__0-ssn', '')
			secured_ssn = ssn.replace(str(ssn[:6]), '***-**')
			mobile_phone = prev_data.get('head_of_household_member_info__0-mobile_phone', '')
			birthday = prev_data.get('head_of_household_member_info__0-birthdate', '')
			gender = prev_data.get('head_of_household_member_info__0-gender', '')
			hoh_info = {'first_name': first_name,
						'last_name': last_name,
						'ssn': secured_ssn,
						'mobile_phone': mobile_phone,
						'birthday': birthday,
						'gender': gender, }
			email = prev_data.get('alternate_contact_info__0-email')
			preferred_phone = prev_data.get('alternate_contact_info__0-preferred_phone')
			preferred_email = prev_data.get('alternate_contact_info__0-preferred_email')
			preferred_contact_tod = prev_data.get('alternate_contact_info__0-preferred_contact_tod')
			ac_info = {'email': email,
					   'preferred_phone': preferred_phone,
					   'preferred_email': preferred_email,
					   'preferred_contact_tod': preferred_contact_tod, }
			prev_data = self.storage.get_step_data('3')
			logger.error("***  OUTPUT - prev data - 3 *** : " + str(prev_data))
			prev_data = self.storage.get_step_data('4')
			logger.error("***  OUTPUT - prev data - 4 *** : " + str(prev_data))
			prev_data = self.storage.get_step_data('3')
			addr = prev_data.get('household_member__3-address_1', '')
			city = prev_data.get('household_member__3-city', '')
			country = prev_data.get('household_member__3-county', '')
			state = prev_data.get('household_member__3-state', '')
			zip_code = prev_data.get('household_member__3-zip_code', '')
			home_phone = prev_data.get('household_member__3-home_phone', '')
			type_of_household = prev_data.get('household_member__3-type_of_household', '')
			housing_type = prev_data.get('household_member__3-housing_type', '')
			assistance_snap = 'off' if not prev_data.get('household_member__3-assistance_snap', '') else 'on'
			assistance_caa = 'off' if not prev_data.get('household_member__3-assistance_caa', '') else 'on'
			assistance_child_support = 'off' if not prev_data.get('household_member__3-assistance_child_support', '') else 'on'
			hh_info = {'addr': addr,
					   'city': city,
					   'state': state,
					   'country': country,
					   'zip_code': zip_code,
					   'home_phone': home_phone,
					   'type_of_household': type_of_household,
					   'housing_type': housing_type,
					   'assistance_snap': assistance_snap,
					   'assistance_caa': assistance_caa,
					   'assistance_child_support': assistance_child_support, }
			hear_united_way = 'off' if not prev_data.get('household_referral_info__3-hear_united_way', '') else 'on'
			hear_govt_agency = 'off' if not prev_data.get('household_referral_info__3-hear_govt_agency', '') else 'on'
			hear_ss_agency = 'off' if not prev_data.get('household_referral_info__3-hear_ss_agency', '') else 'on'
			hear_gccsa_client = 'off' if not prev_data.get('household_referral_info__3-hear_gccsa_client', '') else 'on'
			hear_apt_mgr = 'off' if not prev_data.get('household_referral_info__3-hear_apt_mgr', '') else 'on'
			hear_flyer = 'off' if not prev_data.get('household_referral_info__3-hear_flyer', '') else 'on'
			hear_internet = 'off' if not prev_data.get('household_referral_info__3-hear_internet', '') else 'on'
			hear_radio_tv = 'off' if not prev_data.get('household_referral_info__3-hear_radio_tv', '') else 'on'
			hear_other = prev_data.get('household_referral_info__3-hear_other', '')
			headstart_client = 'off' if not prev_data.get('household_referral_info__3-headstart_client', '') else 'on'
			previous_client = prev_data.get('household_referral_info__3-previous_client', '')
			reason_recent_divorce = 'off' if not prev_data.get('household_referral_info__3-reason_recent_divorce', '') else 'on'
			reason_relocated = 'off' if not prev_data.get('household_referral_info__3-reason_relocated', '') else 'on'
			reason_unexpected_expenses = 'off' if not prev_data.get('household_referral_info__3-reason_unexpected_expenses', '') else 'on'
			reason_housing_award = 'off' if not prev_data.get('household_referral_info__3-reason_housing_award', '') else 'on'
			reason_job_loss = 'off' if not prev_data.get('household_referral_info__3-reason_job_loss', '') else 'on'
			reason_last_employment_date = prev_data.get('household_referral_info__3-reason_last_employment_date', '')
			reason_medical = 'off' if not prev_data.get('household_referral_info__3-reason_medical', '') else 'on'
			reason_other = 'off' if not prev_data.get('household_referral_info__3-reason_other', '') else 'on'
			reason_details = prev_data.get('household_referral_info__3-reason_details', '')
			other_services_rental_assistance = 'off' if not prev_data.get('household_referral_info__3-other_services_rental_assistance', '') else 'on'
			other_services_electricity_assistance = 'off' if not prev_data.get('household_referral_info__3-other_services_electricity_assistance', '') else 'on'
			other_services_job_readiness = 'off' if not prev_data.get('household_referral_info__3-other_services_job_readiness', '') else 'on'
			other_services_financial_literacy = 'off' if not prev_data.get('household_referral_info__3-other_services_financial_literacy', '') else 'on'
			other_services_housing_counseling = 'off' if not prev_data.get('household_referral_info__3-other_services_housing_counseling', '') else 'on'
			other_services_school_supplies = 'off' if not prev_data.get('household_referral_info__3-other_services_school_supplies', '') else 'on'
			other_services_head_start = 'off' if not prev_data.get('household_referral_info__3-other_services_head_start', '') else 'on'
			other_services_vocational_training = 'off' if not prev_data.get('household_referral_info__3-other_services_vocational_training', '') else 'on'
			other_services_adult_basic_education = 'off' if not prev_data.get('household_referral_info__3-other_services_adult_basic_education', '') else 'on'
			other_services_bus_passes = 'off' if not prev_data.get('household_referral_info__3-other_services_bus_passes', '') else 'on'
			other_services_food = 'off' if not prev_data.get('household_referral_info__3-other_services_food', '') else 'on'
			other_services_nutrition = 'off' if not prev_data.get('household_referral_info__3-other_services_nutrition', '') else 'on'
			other_services_seasonal = 'off' if not prev_data.get('household_referral_info__3-other_services_seasonal', '') else 'on'
			case_management = 'off' if not prev_data.get('household_referral_info__3-case_management', '') else 'on'
			hr_info = {'hear_united_way': hear_united_way,
					   'hear_govt_agency': hear_govt_agency,
					   'hear_ss_agency': hear_ss_agency,
					   'hear_gccsa_client': hear_gccsa_client,
					   'hear_apt_mgr': hear_apt_mgr,
					   'hear_flyer': hear_flyer,
					   'hear_internet': hear_internet,
					   'hear_radio_tv': hear_radio_tv,
					   'hear_other': hear_other,
					   'headstart_client': headstart_client,
					   'previous_client': previous_client,
					   'reason_recent_divorce': reason_recent_divorce,
					   'reason_relocated': reason_relocated,
					   'reason_unexpected_expenses': reason_unexpected_expenses,
					   'reason_housing_award': reason_housing_award,
					   'reason_job_loss': reason_job_loss,
					   'reason_last_employment_date': reason_last_employment_date,
					   'reason_medical': reason_medical,
					   'reason_other': reason_other,
					   'reason_details': reason_details,
					   'other_services_rental_assistance': other_services_rental_assistance,
					   'other_services_electricity_assistance': other_services_electricity_assistance,
					   'other_services_job_readiness': other_services_job_readiness,
					   'other_services_financial_literacy': other_services_financial_literacy,
					   'other_services_housing_counseling': other_services_housing_counseling,
					   'other_services_school_supplies': other_services_school_supplies,
					   'other_services_head_start': other_services_head_start,
					   'other_services_vocational_training': other_services_vocational_training,
					   'other_services_adult_basic_education': other_services_adult_basic_education,
					   'other_services_bus_passes': other_services_bus_passes,
					   'other_services_food': other_services_food,
					   'other_services_nutrition': other_services_nutrition,
					   'other_services_seasonal': other_services_seasonal,
					   'case_management': case_management, }

			pdf_generation({'hoh_info': hoh_info, 'ac_info': ac_info, 'hh_info': hh_info, 'hr_info': hr_info, 'request': self.request})
			context.update({'hoh_info': hoh_info, 'ac_info': ac_info})
		return context


def process_form_data(form_list):
	form_data = [form.cleaned_data for form in form_list]
	return form_data


def pdf_generation(info_dict):
	pages = []
	html_header = "<html><head></head><body>"
	html_last = "</body></html>"
	request = info_dict['request']
	member_names_be = request.session['member_names_be']
	member_ssns_be = request.session['member_ssns_be']
	member_mobiles_be = request.session['member_mobiles_be']
	member_bdays_be = request.session['member_bdays_be']
	member_genders_be = request.session['member_genders_be']
	member_rels_be = request.session['member_rels_be']
	members_be = request.session['members_be']
	# Page 1
	html_headofhousehold = "<h3 style='padding-left: 10px;'>Head Of Household</h3><hr><div style='width:20%; display: inline-block;'><span>First Name:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hoh_info']['first_name'] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Last Name: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + info_dict['hoh_info']['last_name'] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>SSN: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + info_dict['hoh_info']['ssn'] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Mobile Phone: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + info_dict['hoh_info']['mobile_phone'] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Birthday: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + info_dict['hoh_info']['birthday'] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Gender: " + "</span></div><div style='width:30%; display: inline-block;'><span>" + info_dict['hoh_info']['gender'] + "</span></div><br>"
	html_headofhousehold_alternatecontactinfo = "<h3 style='padding-left: 10px;'>Alternate Contact Info</h3><hr><div style='width:30%; display: inline-block;'><span>Email:" + "</span></div><div style='width:30%; display: inline-block;'><span>" + info_dict['ac_info']['email'] + "</span></div><br>" + "<div style='width:30%; display: inline-block;'><span>Preferred Phone: " + "</span></div><div style='width:30%; display: inline-block;'><span>" + info_dict['ac_info']['preferred_phone'] + "</span></div><br>" + "<div style='width:30%; display: inline-block;'><span>Preferred Email:" + "</span></div><div style='width:30%; display: inline-block;'><span>" + info_dict['ac_info']['preferred_email'] + "</span></div><br>" + "<div style='width:30%; display: inline-block;'><span>Preferred Time of Contact: " + "</span></div><div style='width:30%; display: inline-block;'><span>" + info_dict['ac_info']['preferred_contact_tod'] + "</span></div><br>"
	html_householdmembers = "<h3 style='padding-left: 10px;'>Household Member List</h3><hr>" + '<div style="font-weight: 600; margin-bottom: 5px"><div class="col-md-4" style="display: inline-block; width: 30%; background-color: #e2e2e2;"><span class="th-span">Name</span></div><div class="col-md-3" style="display: inline-block; width: 30%; background-color: #e2e2e2; border-left:3px solid #fff; border-right:3px solid #fff;"><span class="th-span">Birth Date</span></div><div class="col-md-2" style="display: inline-block; width: 39%; background-color: #e2e2e2;"><span class="th-span">Relationship</span></div></div>'
	for index in range(0, len(member_names_be)):
		each_member_row = '<div class="row tb-div"><div class="col-md-4" style="display: inline-block; width: 30%;"><span>' + member_names_be[index] + '</span></div><div class="col-md-3" style="display: inline-block; width: 30%;"><span>' + member_bdays_be[index] + '</span></div><div class="col-md-2" style="display: inline-block; width: 30%;"><span>' + member_rels_be[index] + '</span></div></div>'
		html_householdmembers = html_householdmembers + each_member_row
	html = html_header + html_headofhousehold + html_headofhousehold_alternatecontactinfo + html_householdmembers + html_last
	page1 = HTML(string=html).render()
	pages.append(page1)
	# Page 2 ~ n (Pages for each household member information)
	for index in range(0, len(member_names_be)):
		# Household member info
		each_hm_name = member_names_be[index].split()
		each_hm_secured_ssn = member_ssns_be[index].replace(str(member_ssns_be[index][:6]), '***-**')
		each_hm_title = "<h3>No " + str(index + 1) + " - " + member_names_be[index] + "</h3><hr>"
		each_hm_info = "<h3 style='padding-left: 10px;'>Household Member Info</h3><div style='width:20%; display: inline-block;'><span>First Name:</span></div><div style='width: 40%; display:inline-block'><span>" + each_hm_name[0] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Last Name: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + each_hm_name[1] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>SSN: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + each_hm_secured_ssn + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Mobile Phone: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + member_mobiles_be[index] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Birthday: " + "</span></div><div style='width:20%; display: inline-block;'><span>" + member_bdays_be[index] + "</span></div><br>" + "<div style='width:20%; display: inline-block;'><span>Gender: " + "</span></div><div style='width:30%; display: inline-block;'><span>" + member_genders_be[index] + "</span></div><br>"
		# Household member demographic
		each_hm_education = dict(EDUCATION).get(members_be[index]['education'])
		each_hm_race = dict(RACE).get(members_be[index]['race'])
		each_hm_ethnicity = dict(ETHNICITY).get(members_be[index]['ethnicity'])
		each_hm_demo_title = "<h3 style='padding-left: 10px;'>Household Member Demographic</h3>"
		each_hm_demo_education = "<div style='width:30%; display: inline-block'<span>Education:</span></div><div style='width: 40%; display: inline-block'<span>" + each_hm_education + "</span></div><br>"
		each_hm_demo_race = "<div style='width:30%; display: inline-block'<span>Race:</span></div><div style='width: 40%; display: inline-block'<span>" + each_hm_race + "</span></div><br>"
		each_hm_demo_ethnicity = "<div style='width:30%; display: inline-block'<span>Ethnicity:</span></div><div style='width: 40%; display: inline-block'<span>" + each_hm_ethnicity + "</span></div><br>"
		each_hm_demo_no_health_insurance = "<div style='width:30%; display: inline-block'<span>No Health Insurance:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['no_health_insurance']) + "</span></div><br>"
		each_hm_demo_disabled = "<div style='width:30%; display: inline-block'<span>Disabled:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['disabled']) + "</span></div><br>"
		each_hm_demo_veteran = "<div style='width:30%; display: inline-block'<span>Veteran:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['veteran']) + "</span></div><br>"
		# Household member income
		each_hm_employment = dict(EMPLOYMENT).get(members_be[index]['employment'])
		each_hm_pay_period = dict(PAY_PERIOD).get(members_be[index]['payperiod'])
		each_hm_income_title = "<h3 style='padding-left: 10px;'>Household Member Income</h3>"
		each_hm_income_employment = "<div style='width:40%; display: inline-block'<span>Employment:</span></div><div style='width: 40%; display: inline-block'<span>" + each_hm_employment + "</span></div><br>"
		each_hm_income_pay_period = "<div style='width:40%; display: inline-block'<span>Pay Period:</span></div><div style='width: 40%; display: inline-block'<span>" + each_hm_pay_period + "</span></div><br>"

		each_hm_income_cash = "<div style='width:40%; display: inline-block'<span>Cash:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_cash']) + "</span></div><br>"
		each_hm_income_snap = "<div style='width:40%; display: inline-block'<span>SNAP Food Stamps:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_snap']) + "</span></div><br>"
		each_hm_income_tanf = "<div style='width:40%; display: inline-block'<span>TANF:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_tanf']) + "</span></div><br>"
		each_hm_income_ss = "<div style='width:40%; display: inline-block'<span>Social Security:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_ss']) + "</span></div><br>"
		each_hm_income_ssdi = "<div style='width:40%; display: inline-block'<span>SSDI/SSI/RSDI:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_ssdi']) + "</span></div><br>"
		each_hm_income_medicare = "<div style='width:40%; display: inline-block'<span>Medicare:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_medicare']) + "</span></div><br>"
		each_hm_income_other_agencies = "<div style='width:40%; display: inline-block'<span>Assistance from Other Agencies:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_other_agencies']) + "</span></div><br>"
		each_hm_income_gifts = "<div style='width:40%; display: inline-block'<span>Gifts:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_gifts']) + "</span></div><br>"
		each_hm_income_unemployment = "<div style='width:40%; display: inline-block'<span>Unemployment:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_unemployment']) + "</span></div><br>"
		each_hm_income_workers_comp = "<div style='width:40%; display: inline-block'<span>Worker's Comp:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_workers_comp']) + "</span></div><br>"
		each_hm_income_pensions = "<div style='width:40%; display: inline-block'<span>Pensions:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_pensions']) + "</span></div><br>"
		each_hm_income_job_training = "<div style='width:40%; display: inline-block'<span>Job Training Stipends:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_job_training']) + "</span></div><br>"
		each_hm_income_military_allotments = "<div style='width:40%; display: inline-block'<span>Military Allotments:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_military_allotments']) + "</span></div><br>"
		each_hm_income_va = "<div style='width:40%; display: inline-block'<span>VA Benefits:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_va']) + "</span></div><br>"
		each_hm_income_insurance = "<div style='width:40%; display: inline-block'<span>Insurance Payment:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_insurance']) + "</span></div><br>"
		each_hm_income_alimony = "<div style='width:40%; display: inline-block'<span>Alimony:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_alimony']) + "</span></div><br>"
		each_hm_income_foster_payments = "<div style='width:40%; display: inline-block'<span>Foster/Adopted Children Payments:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_foster_payments']) + "</span></div><br>"
		each_hm_income_child_support = "<div style='width:40%; display: inline-block'<span>Court-ordered Child Support:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_child_support']) + "</span></div><br>"
		each_hm_income_college_scholarship = "<div style='width:40%; display: inline-block'<span>College Scholarships:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_college_scholarship']) + "</span></div><br>"
		each_hm_income_student_loans = "<div style='width:40%; display: inline-block'<span>Student Loans:</span></div><div style='width: 40%; display: inline-block'<span>" + boolean2booleanicon(members_be[index]['other_income_student_loans']) + "</span></div><br>"
		each_hm_income_other = "<div style='width:40%; display: inline-block'<span>Other:</span></div><div style='width: 40%; display: inline-block'<span>" + members_be[index]['income_other'] + "</span></div><br>"
		each_hm_demo = each_hm_demo_title + each_hm_demo_education + each_hm_demo_race + each_hm_demo_ethnicity + each_hm_demo_no_health_insurance + each_hm_demo_disabled + each_hm_demo_veteran
		each_hm_income = each_hm_income_title + each_hm_income_employment + each_hm_income_pay_period + each_hm_income_cash + each_hm_income_snap + each_hm_income_tanf + each_hm_income_ss + each_hm_income_ssdi + each_hm_income_medicare + each_hm_income_other_agencies + each_hm_income_other_agencies + each_hm_income_gifts + each_hm_income_unemployment + each_hm_income_workers_comp + each_hm_income_pensions + each_hm_income_job_training + each_hm_income_military_allotments + each_hm_income_va + each_hm_income_insurance + each_hm_income_alimony + each_hm_income_foster_payments + each_hm_income_child_support + each_hm_income_college_scholarship + each_hm_income_student_loans + each_hm_income_other
		html = html_header + each_hm_title + each_hm_info + each_hm_demo + each_hm_income + html_last
		page2 = HTML(string=html).render()
		pages.append(page2)

	# Household information
	each_hm_household_type = dict(HOUSEHOLD_TYPES).get(info_dict['hh_info']['type_of_household'])
	each_hm_housing_type = dict(HOUSING_TYPES).get(info_dict['hh_info']['housing_type'])
	hh_title = "<h3>Household Information</h3><hr>"
	hh_addr = "<div style='width:40%; display: inline-block;'><span>Address:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hh_info']['addr'] + "</span></div><br>"
	hh_city = "<div style='width:40%; display: inline-block;'><span>City:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hh_info']['city'] + "</span></div><br>"
	hh_country = "<div style='width:40%; display: inline-block;'><span>Country:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hh_info']['country'] + "</span></div><br>"
	hh_state = "<div style='width:40%; display: inline-block;'><span>State:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hh_info']['state'] + "</span></div><br>"
	hh_zip_code = "<div style='width:40%; display: inline-block;'><span>Zip Code:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hh_info']['zip_code'] + "</span></div><br>"
	hh_type_of_household = "<div style='width:40%; display: inline-block;'><span>Type of Household:</span></div><div style='width: 40%; display:inline-block'><span>" + each_hm_household_type + "</span></div><br>"
	hh_housing_type = "<div style='width:40%; display: inline-block;'><span>Housing Type:</span></div><div style='width: 40%; display:inline-block'><span>" + each_hm_housing_type + "</span></div><br>"
	hh_assistance_snap = "<div style='width:40%; display: inline-block;'><span>Household receives SNAP:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hh_info']['assistance_snap']) + "</span></div><br>"
	hh_assistance_caa = "<div style='width:40%; display: inline-block;'><span>Household receives assistance from other community agencies:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hh_info']['assistance_caa']) + "</span></div><br>"
	hh_assistance_child_support = "<div style='width:40%; display: inline-block;'><span>Household receives assistance for child support:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hh_info']['assistance_child_support']) + "</span></div><br>"
	each_hr_previous_client = dict(GCCSA_HISTORY).get(info_dict['hr_info']['previous_client'])
	hr_title = "<h3>Household Referral</h3><hr>"
	hr_hear_united_way = "<h4>How did you learn about GCCSA services?</h4><div style='width:40%; display: inline-block;'><span>2-1-1 United Way Hotline:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_united_way']) + "</span></div><br>"
	hr_hear_govt_agency = "<div style='width:40%; display: inline-block;'><span>Government Agency:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_govt_agency']) + "</span></div><br>"
	hr_hear_ss_agency = "<div style='width:40%; display: inline-block;'><span>Other Community Agency:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_ss_agency']) + "</span></div><br>"
	hr_hear_gccsa_client = "<div style='width:40%; display: inline-block;'><span>A Former GCCSA Client:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_gccsa_client']) + "</span></div><br>"
	hr_hear_apt_mgr = "<div style='width:40%; display: inline-block;'><span>Apartment Manager Referred:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_apt_mgr']) + "</span></div><br>"
	hr_hear_flyer = "<div style='width:40%; display: inline-block;'><span>Flyer:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_flyer']) + "</span></div><br>"
	hr_hear_internet = "<div style='width:40%; display: inline-block;'><span>GCCSA Website/Internet:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_internet']) + "</span></div><br>"
	hr_hear_radio_tv = "<div style='width:40%; display: inline-block;'><span>Radio, Newspaaper, TV:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['hear_radio_tv']) + "</span></div><br>"
	hr_hear_other = "<div style='width:40%; display: inline-block;'><span>Other:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hr_info']['hear_other'] + "</span></div><br>"
	hr_headstart_client = "<div style='width:40%; display: inline-block;'><h4>Are you a head start client:</h4></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['headstart_client']) + "</span></div><br>"
	hr_previous_client = "<div style='width:40%; display: inline-block;'><h4>Are you, or a Household Member a previous client of GCCSA:</h4></div><div style='width: 40%; display:inline-block'><span>" + each_hr_previous_client + "</span></div><br>"
	hr_reason_recent_divorce = "<h4>Indicate the situation and/or circumstances that led to you requesting GCCSA Services.</h4><div style='width:40%; display: inline-block;'><span>Recent Divorce / Separation:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['reason_recent_divorce']) + "</span></div><br>"
	hr_reason_relocated = "<div style='width:40%; display: inline-block;'><span>Relocated to the Area:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['reason_relocated']) + "</span></div><br>"
	hr_reason_unexpected_expenses = "<div style='width:40%; display: inline-block;'><span>Unexpected Expenses:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['reason_unexpected_expenses']) + "</span></div><br>"
	hr_reason_housing_award = "<div style='width:40%; display: inline-block;'><span>Change in Housing Award Amount:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['reason_housing_award']) + "</span></div><br>"
	hr_reason_job_loss = "<div style='width:40%; display: inline-block;'><span>Job Loss:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['reason_job_loss']) + "</span></div><br>"
	hr_reason_last_employment_date = "<div style='width:40%; display: inline-block;'><span>Last date of employment:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hr_info']['reason_last_employment_date'] + "</span></div><br>"
	hr_reason_medical = "<div style='width:40%; display: inline-block;'><span>Medical Emergency:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['reason_medical']) + "</span></div><br>"
	hr_reason_other = "<div style='width:40%; display: inline-block;'><span>Other:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['reason_other']) + "</span></div><br>"
	hr_reason_details = "<div style='width:40%; display: inline-block;'><span>Provide details of your household situation:</span></div><div style='width: 40%; display:inline-block'><span>" + info_dict['hr_info']['reason_details'] + "</span></div><br>"
	hh_content = hh_title + hh_addr + hh_city + hh_country + hh_state + hh_zip_code + hh_type_of_household + hh_housing_type + hh_assistance_snap + hh_assistance_caa + hh_assistance_child_support
	hr_content = hr_title + hr_hear_united_way + hr_hear_govt_agency + hr_hear_ss_agency + hr_hear_gccsa_client + hr_hear_apt_mgr + hr_hear_flyer + hr_hear_internet + hr_hear_radio_tv + hr_hear_other + hr_headstart_client + hr_previous_client + hr_reason_recent_divorce + hr_reason_relocated + hr_reason_unexpected_expenses + hr_reason_housing_award + hr_reason_job_loss + hr_reason_last_employment_date + hr_reason_medical + hr_reason_other + hr_reason_details
	html = html_header + hh_content + hr_content + html_last
	page3 = HTML(string=html).render()
	pages.append(page3)
	# Household referral information(continue)
	hr_other_services_rental_assistance = "<h4>GCCSA offers various services to address household needs through Case Management and referrals to Community Partners.</h4><div style='width:40%; display: inline-block;'><span>Rental Assistance:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_rental_assistance']) + "</span></div><br>"
	hr_other_services_electricity_assistance = "<div style='width:40%; display: inline-block;'><span>Electricity Assistance:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_electricity_assistance']) + "</span></div><br>"
	hr_other_services_job_readiness = "<div style='width:40%; display: inline-block;'><span>Job Readiness Training:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_job_readiness']) + "</span></div><br>"
	hr_other_services_financial_literacy = "<div style='width:40%; display: inline-block;'><span>Financial Literacy:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_financial_literacy']) + "</span></div><br>"
	hr_other_services_housing_counseling = "<div style='width:40%; display: inline-block;'><span>Housing Counseling:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_housing_counseling']) + "</span></div><br>"
	hr_other_services_school_supplies = "<div style='width:40%; display: inline-block;'><span>School Supplies/Holiday Initiative:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_school_supplies']) + "</span></div><br>"
	hr_other_services_head_start = "<div style='width:40%; display: inline-block;'><span>Head Start/Early Head Start Program:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_head_start']) + "</span></div><br>"
	hr_other_services_vocational_training = "<div style='width:40%; display: inline-block;'><span>Scholarship/Vocational Training:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_vocational_training']) + "</span></div><br>"
	hr_other_services_adult_basic_education = "<div style='width:40%; display: inline-block;'><span>GED/Adult Basic Education:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_adult_basic_education']) + "</span></div><br>"
	hr_other_services_bus_passes = "<div style='width:40%; display: inline-block;'><span>Bus Passes:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_bus_passes']) + "</span></div><br>"
	hr_other_services_food = "<div style='width:40%; display: inline-block;'><span>Emergency Food:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_food']) + "</span></div><br>"
	hr_other_services_nutrition = "<div style='width:40%; display: inline-block;'><span>Nutrition Services:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_nutrition']) + "</span></div><br>"
	hr_other_services_seasonal = "<div style='width:40%; display: inline-block;'><span>Seasonal Holiday Initiatives:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['other_services_seasonal']) + "</span></div><br>"
	hr_case_management = "<div style='width:40%; display: inline-block;'><span>Case Management Program:</span></div><div style='width: 40%; display:inline-block'><span>" + switch2booleanicon(info_dict['hr_info']['case_management']) + "</span></div><br>"
	hr_content_continue = hr_other_services_rental_assistance + hr_other_services_electricity_assistance + hr_other_services_job_readiness + hr_other_services_financial_literacy + hr_other_services_housing_counseling + hr_other_services_school_supplies + hr_other_services_head_start + hr_other_services_vocational_training + hr_other_services_adult_basic_education + hr_other_services_bus_passes + hr_other_services_food + hr_other_services_nutrition + hr_other_services_seasonal + hr_case_management
	html = html_header + hr_content_continue + html_last
	page4 = HTML(string=html).render()
	pages.append(page4)

	pdf_file = pages[0].copy([page for p in pages for page in p.pages]).write_pdf(get_cur_survey_url() + '/survey.pdf')
# Extra functions


def switch2booleanicon(switch_str):
	if switch_str == 'on':
		return '[✓]'
		# '☑'
	else:
		return '[ ]'


def boolean2booleanicon(var_bool):
	if var_bool == 'true':
		return '[✓]'
	else:
		return '[ ]'


def log_current_status():
	# logger.error("***  OUTPUT - member names *** : " + str(member_names_be))
	# logger.error("***  OUTPUT - member ssns *** : " + str(member_ssns_be))
	# logger.error("***  OUTPUT - member mobiles *** : " + str(member_mobiles_be))
	# logger.error("***  OUTPUT - member bdays *** : " + str(member_bdays_be))
	# logger.error("***  OUTPUT - member genders *** : " + str(member_genders_be))
	# logger.error("***  OUTPUT - member rels *** : " + str(member_rels_be))
	# logger.error("***  OUTPUT - members *** : " + str(members_be))
	a = 0


def list_duplicates_of(seq, item):
	start_at = -1
	locs = []
	while True:
		try:
			loc = seq.index(item, start_at + 1)
		except ValueError:
			break
		else:
			locs.append(loc)
			start_at = loc
	return locs


def last_2_digits(n):
	return float(str(n)[-3:]) if '.' in str(n)[-2:] else int(str(n)[-2:])


def get_config():
	PROJECT_ROOT = get_project_root()
	CONFIG_FOLDER = os.path.join(PROJECT_ROOT, 'org_info/gccsa/config/')
	with open(CONFIG_FOLDER + 'config.json') as config_data:
		config = json.load(config_data)
	return config


def get_tpl_url():
	PROJECT_ROOT = get_project_root()
	TPL_ROOT = os.path.join(PROJECT_ROOT, 'org_info/gccsa/tpl/')
	return TPL_ROOT


def get_cur_survey_url():
	config = get_config()
	PROJECT_ROOT = get_project_root()
	survey_id = Survey.objects.latest('id').survey_id
	logger.error("***  OUTPUT - survey_id *** :" + str(survey_id))
	CUR_SURVEY_URL = PROJECT_ROOT + '/org_info/' + config['org']['org_symbol'] + '/survey/' + 'survey_' + str(survey_id)
	if not os.path.isdir(CUR_SURVEY_URL):
		os.makedirs(CUR_SURVEY_URL)
	return CUR_SURVEY_URL


def get_cur_survey_zip_url():
	config = get_config()
	PROJECT_ROOT = get_project_root()
	survey_id = Survey.objects.latest('id').survey_id
	logger.error("***  OUTPUT - survey_id *** :" + str(survey_id))
	CUR_SURVEY_ZIP_URL = PROJECT_ROOT + '/org_info/' + config['org']['org_symbol'] + '/survey'
	if not os.path.isdir(CUR_SURVEY_ZIP_URL):
		os.makedirs(CUR_SURVEY_ZIP_URL)
	return CUR_SURVEY_ZIP_URL


def get_project_root():
	settings_dir = os.path.dirname(__file__)
	PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
	return PROJECT_ROOT
