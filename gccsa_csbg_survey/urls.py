from django.conf.urls import url, include

from gccsa_csbg_survey import views as gccsa_views
from gccsa_csbg_survey.forms import *

urlpatterns = [
	url(r'^$', gccsa_views.about, name='about'),
	url(r'^about/', gccsa_views.about, name='about'),
	url(r'^requirement/', gccsa_views.requirement, name='requirement'),
	url(r'^create_survey/', gccsa_views.create_survey, name='create_survey'),
	url(r'^add_member/', gccsa_views.add_member, name='add_member'),
	url(r'^delete_member/', gccsa_views.delete_member, name='delete_member'),
	url(r'^add_change_member/', gccsa_views.add_change_member, name='add_change_member'),
	url(r'^get_default_member/', gccsa_views.get_default_member, name='get_default_member'),
	url(r'^get_member_status/', gccsa_views.get_member_status, name='get_member_status'),

	url(r'^information/$', gccsa_views.InformationWizard.as_view( [HeadOfHousehold, HouseholdMemberInfo,
			HouseholdMemberAdd, Household, DocumentForm, VerifyInfo]), name='information'),
	url(r'^get_pdf/', gccsa_views.get_pdf, name='get_pdf'),
	url(r'^handle404/', gccsa_views.handler404, name='404'),
]
