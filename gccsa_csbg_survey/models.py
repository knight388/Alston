'''
Created on Feb 21, 2017

@author: apptworks
'''

from django.utils.translation import gettext as _
from django.db import models
from localflavor.us.models import USStateField, PhoneNumberField, USZipCodeField, USSocialSecurityNumberField

ALT_CONTACT_RELATIONSHIPS = (
	('relative', _('Relative')),
	('spouse', _('Spouse')),
	('friend', _('Friend')),
	('coworker', _('Coworker')),
)

EDUCATION = (
	('pre_hs', _('0-8 grade')),
	('in_hs', _('9-12 no high school graduation')),
	('hs_grad', _('High school graduate/GED')),
	('post_hs', _('12+ post sec')),
	('college_degree', _('2 or 4 year degree')),
)

EMPLOYMENT = (
  ('employed', _('Employed')),
  ('not_employed', _('Not employed')),
  ('self_employed', _('Self employed')),
)

ETHNICITY = (
  ('hispanic', _('Hispanic')),
  ('not_hispanic', _('Not Hispanic')),
)

GCCSA_HISTORY = (
  ('first_time_applicant', _('No, I am a first time applicant')),
  ('0-2_years', _('Yes, 0-2 years ago')),
  ('3-5_years', _('Yes, 3-5 years ago')),
  ('over_5_years', _('Yes, over 5 years ago')),
)
GENDER = (
  ('male', _('Male')),
  ('female', _('Female')),
)

HOUSEHOLD_TYPES = (
	('single_female', _('Single parent female')),
	('single_male', _('Single parent male')),
	('single_person', _('Single person')),
	('two_parent', _('Two parent household')),
	('two_adults', _('Two adults')),
	('no_children', _('No children')),
	('other', _('Other')),
)

HOUSING_TYPES = (
	('housing_assistance', _('Housing assistance')),
	('apartment', _('Rent an apartment')),
	('home_rent', _('Rent a home')),
	('homeowner', _('Homeowner')),
	('homeless', _('Homeless')),
	('live_wtih_relatives', _('Live with relatives')),
	('other', _('Other')),
)

PAY_PERIOD = (
	('weekly', _('Weekly')),
	('biweekly', _('Every two weeks')),
	('semi_monthly', _('Twice a month')),
	('monthly', _('Monthly')),
	('other', _('Other')),
)

PREFERRED_CONTACT_TOD = (
    ('morning', _('Morning')),
    ('afternoon', _('Afternoon')),
)

PREFERRED_PHONE = (
    ('home', _('Home')),
    ('mobile', _('Mobile')),
)

RACE = (
	('black', _('Black/African American')),
	('white', _('White')),
	('native', _('American Indian or Alaska Native')),
	('asian', _('Asian')),
	('multi', _('Multi-race')),
	('other', _('Other')),
)


class Org(models.Model):
	org_symbol = models.CharField(max_length=8, db_index=True)
	org_product = models.CharField(max_length=8, db_index=True)

	class Meta:
		unique_together = ('org_symbol', 'org_product',)



class Survey(models.Model):
	org = models.ForeignKey(Org)
	created = models.DateTimeField(auto_now_add=True)
	submitted = models.DateTimeField()
	survey_id = models.SmallIntegerField()  # last 2 digits of year plus id, calculated on submitted time


class Household(models.Model):
	survey = models.ForeignKey(Survey)
	address_1 = models.CharField(max_length=128, verbose_name=_('Address'), help_text=_(''))
	city = models.CharField(max_length=64, verbose_name=_('City'), help_text=_(''))
	county = models.CharField(max_length=100, verbose_name=_('County'), help_text=_(''))
	state = USStateField(max_length=100, verbose_name=_('State'), help_text=_(''))
	zip_code = USZipCodeField(max_length=5, verbose_name=_('Zip Code'), help_text=_(''))
	home_phone = PhoneNumberField(max_length=100, blank=True, verbose_name=_('Home Phone'), help_text=_(''))  # blank ok only if head of household mobile_phone is not blank
	type_of_household = models.CharField(max_length=20, choices=HOUSEHOLD_TYPES, verbose_name=_('Type of Household'), help_text=_(''))
	# type_of_household_other = models.CharField(max_length=40, verbose_name=_('Other'), help_text=_('')) #required if type_of_household = 'other'
	housing_type = models.CharField(max_length=20, choices=HOUSING_TYPES, verbose_name=_('Housing Type'), help_text=_(''))
	# housing_other = models.CharField(max_length=40, blank=True, verbose_name=_('Housing Other'), help_text=_('Other')) #required if housing = 'other'
	assistance_snap = models.BooleanField(verbose_name=_('Household receives SNAP'), help_text=_(''))
	assistance_caa = models.BooleanField(verbose_name=_('Household receives assistance from other community agencies'), help_text=_(''))
	assistance_child_support = models.BooleanField(verbose_name=_('Household receives assistance for child support'), help_text=_(''))


class HouseholdMember(models.Model):
	household = models.ForeignKey(Household)
	first_name = models.CharField(error_messages={'required': 'Please let us know what to call you!'}, max_length=100, verbose_name=_('First Name'), help_text=_(''))
	last_name = models.CharField(max_length=100, verbose_name=_('Last Name'), help_text=_(''))
	ssn = USSocialSecurityNumberField(verbose_name=_('Social Security Number'), help_text=_(''))
	mobile_phone = PhoneNumberField(max_length=100, blank=True, verbose_name=_('Mobile Phone'), help_text=_(''))  # blank ok only if household home_phone is not blank
	birthdate = models.DateField(null=True, verbose_name=_('Birth Date'), help_text=_(''))  # no later than 100 years ago
	gender = models.CharField(null=True, max_length=20, choices=GENDER, verbose_name=_('Gender'), help_text=_(''))


class HeadOfHouseholdMember(models.Model):
	household_member = models.ForeignKey(HouseholdMember)
	email = models.EmailField(verbose_name=_('Email'), help_text=_(''))
	preferred_phone = models.CharField(max_length=20, choices=PREFERRED_PHONE, verbose_name=_('Preferred Phone'), help_text=_(''))  # home_phone or mobile_phone must not be blank if chosen
	preferred_email = models.EmailField(verbose_name=_('Preferrred contact email address'), help_text=_(''))
	preferred_contact_tod = models.CharField(max_length=20, choices=PREFERRED_CONTACT_TOD, verbose_name=_('Preferrred Time of Contact'), help_text=_(''))


class HouseholdMemberDemographics(models.Model):
	household_member = models.ForeignKey(HouseholdMember)
	education = models.CharField(max_length=20, choices=EDUCATION, verbose_name=_('Education'), help_text=_(''))
	race = models.CharField(max_length=20, choices=RACE, verbose_name=_('Race'), help_text=_(''))
	ethnicity = models.CharField(max_length=20, choices=ETHNICITY, verbose_name=_('Ethnicity'), help_text=_(''))
	no_health_insurance = models.BooleanField(verbose_name=_('No Health Insurance'), help_text=_(''))
	disabled = models.BooleanField(verbose_name=_('Disabled'), help_text=_('Disabled'))
	veteran = models.BooleanField(verbose_name=_('Veteran'), help_text=_('Veteran'))


class HouseholdMemberIncome(models.Model):
	household_member = models.ForeignKey(HouseholdMember)
	employment = models.CharField(max_length=20, choices=EMPLOYMENT, verbose_name=_('Employment'), help_text=_(''))
	pay_period = models.CharField(max_length=50, choices=PAY_PERIOD, verbose_name=_('Pay Period'), help_text=_(''))  # disabled if employment = 'not_employed'
	other_income_cash = models.BooleanField(verbose_name=_('Cash'), help_text=_(''))
	other_income_snap = models.BooleanField(verbose_name=_('SNAP Food Stamps'), help_text=_(''))
	other_income_tanf = models.BooleanField(verbose_name=_('TANF'), help_text=_(''))
	other_income_ss = models.BooleanField(verbose_name=_('Social Security'), help_text=_(''))
	other_income_ssdi = models.BooleanField(verbose_name=_('SSDI/SSI/RSDI'), help_text=_(''))
	other_income_medicare = models.BooleanField(verbose_name=_('Medicare'), help_text=_(''))
	other_income_other_agencies = models.BooleanField(verbose_name=_('Assistance from Other Agencies'), help_text=_(''))
	other_income_gifts = models.BooleanField(verbose_name=_('Gifts'), help_text=_(''))
	other_income_unemployment = models.BooleanField(verbose_name=_('Unemployment'), help_text=_(''))
	other_income_workers_comp = models.BooleanField(verbose_name=_("Worker's Comp"), help_text=_(''))
	other_income_pensions = models.BooleanField(verbose_name=_('Pensions'), help_text=_(''))
	other_income_job_training = models.BooleanField(verbose_name=_('Job Training Stipends'), help_text=_(''))
	other_income_military_allotments = models.BooleanField(verbose_name=_('Military Allotments'), help_text=_(''))
	other_income_va = models.BooleanField(verbose_name=_('VA Benefits'), help_text=_(''))
	other_income_insurance = models.BooleanField(verbose_name=_('Insurance Payment'), help_text=_(''))
	other_income_alimony = models.BooleanField(verbose_name=_('Alimony'), help_text=_(''))
	other_income_foster_payments = models.BooleanField(verbose_name=_('Foster/Adopted Children Payments'), help_text=_(''))
	other_income_child_support = models.BooleanField(verbose_name=_('Court-ordered Child Support'), help_text=_(''))
	other_income_college_scholarship = models.BooleanField(verbose_name=_('College Scholarships'), help_text=_(''))
	other_income_student_loans = models.BooleanField(verbose_name=_('Student Loans'), help_text=_(''))
	other_income_other = models.CharField(max_length=50, verbose_name=_('Other'), help_text=_(''))
	# no_proof_of_income = models.BooleanField(verbose_name=_('I have no proof of income of over the last 30 days'), help_text=_(''))


class HouseholdReferral(models.Model):
	household = models.ForeignKey(Household)
	hear_united_way = models.BooleanField(verbose_name=_('2-1-1 United Way Hotline'), help_text=_(''))
	hear_govt_agency = models.BooleanField(verbose_name=_('Government Agency'), help_text=_(''))
	hear_ss_agency = models.BooleanField(verbose_name=_('Other Community Agency'), help_text=_(''))
	hear_gccsa_client = models.BooleanField(verbose_name=_('A Former GCCSA Client'), help_text=_(''))
	hear_apt_mgr = models.BooleanField(verbose_name=_('Apartment Manager Referred'), help_text=_(''))
	hear_flyer = models.BooleanField(verbose_name=_('Flyer'), help_text=_(''))
	hear_internet = models.BooleanField(verbose_name=_('GCCSA Website/Internet'), help_text=_(''))
	hear_radio_tv = models.BooleanField(verbose_name=_('Radio, Newspaaper, TV'), help_text=_(''))
	hear_other = models.CharField(max_length=50, verbose_name=_('Other'), help_text=_(''))
	headstart_client = models.BooleanField(verbose_name=_('Are you a head start client'), help_text=_(''))
	previous_client = models.CharField(max_length=50, choices=GCCSA_HISTORY, verbose_name=_('Are you, or a Household Member a previous client of GCCSA'), help_text=_(''))
	reason_recent_divorce = models.BooleanField(verbose_name=_('Recent Divorce / Separation'), help_text=_(''))
	reason_relocated = models.BooleanField(verbose_name=_('Relocated to the Area'), help_text=_(''))
	reason_unexpected_expenses = models.BooleanField(verbose_name=_('Unexpected Expenses'), help_text=_(''))
	reason_housing_award = models.BooleanField(verbose_name=_('Change in Housing Award Amount'), help_text=_(''))
	reason_job_loss = models.BooleanField(verbose_name=_('Job Loss'), help_text=_(''))
	reason_last_employment_date = models.DateField(null=True, blank=True, verbose_name=_('Last date of employment'), help_text=_(''))  # cannot be null if reason_job_loss is set
	reason_medical = models.BooleanField(verbose_name=_('Medical Emergency'), help_text=_(''))
	reason_other = models.BooleanField(verbose_name=_('Other'), help_text=_(''))
	reason_details = models.CharField(max_length=4000, verbose_name=_('Provide details of your household situation'), help_text=_(''))
	other_services_rental_assistance = models.BooleanField(verbose_name=_('Rental Assistance'), help_text=_(''))
	other_services_electricity_assistance = models.BooleanField(verbose_name=_('Electricity Assistance'), help_text=_(''))
	other_services_job_readiness = models.BooleanField(verbose_name=_('Job Readiness Training'), help_text=_(''))
	other_services_financial_literacy = models.BooleanField(verbose_name=_('Financial Literacy'), help_text=_(''))
	other_services_housing_counseling = models.BooleanField(verbose_name=_('Housing Counseling'), help_text=_(''))
	other_services_school_supplies = models.BooleanField(verbose_name=_('School Supplies/Holiday Initiative'), help_text=_(''))
	other_services_head_start = models.BooleanField(verbose_name=_('Head Start/Early Head Start Program'), help_text=_(''))
	other_services_vocational_training = models.BooleanField(verbose_name=_('Scholarship/Vocational Training'), help_text=_(''))
	other_services_adult_basic_education = models.BooleanField(verbose_name=_('GED/Adult Basic Education'), help_text=_(''))
	other_services_bus_passes = models.BooleanField(verbose_name=_('Bus Passes'), help_text=_(''))
	other_services_food = models.BooleanField(verbose_name=_('Emergency Food'), help_text=_(''))
	other_services_nutrition = models.BooleanField(verbose_name=_('Nutrition Services'), help_text=_(''))
	other_services_seasonal = models.BooleanField(verbose_name=_('Seasonal Holiday Initiatives'), help_text=_(''))
	case_management = models.BooleanField(verbose_name=_('Case Management Program'), help_text=_(''))


class Document(models.Model):
	description = models.CharField(max_length=255, blank=True)
	doc_url = models.FileField(upload_to='/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
