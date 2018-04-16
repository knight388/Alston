from django import forms
from betterforms.multiform import MultiModelForm
from collections import OrderedDict
from .models import HouseholdMember, Household, HeadOfHouseholdMember, HouseholdReferral, HouseholdMemberDemographics, HouseholdMemberIncome, Document

# Page 1-1


class HeadOfHouseholdMemberInfo(forms.ModelForm):
	class Meta:
		model = HouseholdMember
		fields = ('__all__')
		widgets = {
			'birthdate': forms.DateInput(attrs={'class': 'datepicker'}),
		}

	def __init__(self, *args, **kwargs):
		super(HeadOfHouseholdMemberInfo, self).__init__(*args, **kwargs)
		self.fields.pop('household')

	# def clean(self):
	# 	super(HeadOfHouseholdMemberInfo, self).clean()
	# 	self.add_error('first_name', 'msg')
	# 	data = self.cleaned_data
	# 	raise forms.ValidationError(
	#					"Did not send for 'help' in the subject despite "
	#					"CC'ing yourself."
	#				)
	# 	self.validate_required_field(self.cleaned_data, 'first_name')
	# 	self.first_name = "AAA"
	# 	if data.get('household_relationship', none) == "other" :
	# 		self._errors['household_relationship'] = self.error_class(['message'])
	# 	else :
	# 		self._errors['household_relationship'] = self.error_class(['message'])
	# Page 1-2


class AlternateContactInfo(forms.ModelForm):
	class Meta:
		model = HeadOfHouseholdMember
		fields = ('__all__')

	def __init__(self, *args, **kwargs):
		super(AlternateContactInfo, self).__init__(*args, **kwargs)
		self.fields.pop('household_member')

# Page 1


class HeadOfHousehold(MultiModelForm):
	base_fields = {}
	form_classes = OrderedDict((
		('head_of_household_member_info', HeadOfHouseholdMemberInfo),
		('alternate_contact_info', AlternateContactInfo),
	))

# Page 2


class HouseholdMemberInfo(forms.ModelForm):
	class Meta:
		model = HouseholdMember
		fields = ('__all__')

	def __init__(self, *args, **kwargs):
		super(HouseholdMemberInfo, self).__init__(*args, **kwargs)
		self.fields.pop('household')

# Page 3-1


class HouseholdMemberDemographicsInfo(forms.ModelForm):
	class Meta:
		model = HouseholdMemberDemographics
		fields = ('__all__')

	def __init__(self, *args, **kwargs):
		super(HouseholdMemberDemographicsInfo, self).__init__(*args, **kwargs)
		self.fields.pop('household_member')

# Page 3-2


class HouseholdMemberIncomeInfo(forms.ModelForm):
	class Meta:
		model = HouseholdMemberIncome
		fields = ('__all__')

	def __init__(self, *args, **kwargs):
		super(HouseholdMemberIncomeInfo, self).__init__(*args, **kwargs)
		self.fields.pop('household_member')

# Page 3


class HouseholdMemberAdd(MultiModelForm):
	base_fields = {}
	form_classes = OrderedDict((
		('household_member_demographics', HouseholdMemberDemographicsInfo),
		('household_member_income', HouseholdMemberIncomeInfo),
	))

# Page 4-1


class HouseholdInfo(forms.ModelForm):
	class Meta:
		model = Household
		fields = ('__all__')

	def __init__(self, *args, **kwargs):
		super(HouseholdInfo, self).__init__(*args, **kwargs)
		self.fields.pop('survey')

# Page 4-2


class HouseholdReferralInfo(forms.ModelForm):
	class Meta:
		model = HouseholdReferral
		fields = ('__all__')
		widgets = {
			'reason_last_employment_date': forms.DateInput(attrs={'class': 'datepicker'}),
		}

	def __init__(self, *args, **kwargs):
		super(HouseholdReferralInfo, self).__init__(*args, **kwargs)
		self.fields.pop('household')

# Page 4


class Household(MultiModelForm):
	base_fields = {}
	form_classes = OrderedDict((
    ('household_member', HouseholdInfo),
    ('household_referral_info', HouseholdReferralInfo),
  ))

# Page 5


class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('__all__')

	def __init__(self, *args, **kwargs):
		super(DocumentForm, self).__init__(*args, **kwargs)

# Page 6


class VerifyInfo(forms.Form):
	query_1 = forms.BooleanField(label="I attest the information provided in this application is true and correct to the best of my knowledge and belief.")
	query_2 = forms.BooleanField(label="I understand that no more than three (3) attempts (via phone) will be made by a GCCSA representative to schedule an appointment for GCCSA services plan.")
	query_3 = forms.BooleanField(label="I understand my household income will be annualized, at the time of the submitted application, based on pre-established agency procedures and the Texas Administrative Code (TAC).")
	query_4 = forms.BooleanField(label="I understand I may appeal a denial of eligibility, amount of assistance received or a delay of service(s).")
	query_5 = forms.BooleanField(label="I authorize the Texas Department of Housing and Community Affairs and its contracted agencies to solicit/verify information provided on this application.")
	query_6 = forms.BooleanField(label="I understand that completion and submission of this application does not guarantee services.")
	query_7 = forms.BooleanField(label="I understand that I am responsible for providing copies of support documentation. GCCSA does not make copies of documentation.")
	query_8 = forms.BooleanField(label="I understand that after one year, a request for my application documents will be subject to the policy and procedures as outlined in the Open Records Request, and may require a fee for service.")
	query_9 = forms.BooleanField(label="I AM AWARE THAT I AM SUBJECT TO PROSECUTION AND/OR FINES UP TO $10,000 FOR PROVIDING FALSE OR FRAUDULENT INFORMATION. Title 18, Section 1001 of the U.S. Code makes it a criminal offense to make willful false statements or misrepresentation to any department or agency in the United States as to any matter within its jurisdiction.")
