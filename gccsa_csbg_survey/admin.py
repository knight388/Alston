from django.contrib import admin

# Register your models here.
from .models import Org, Survey, Household, HouseholdMember, HeadOfHouseholdMember, HouseholdMemberDemographics, HouseholdMemberIncome, HouseholdReferral, Document

admin.site.register(Org)
admin.site.register(Survey)
admin.site.register(Household)
admin.site.register(HouseholdMember)
admin.site.register(HeadOfHouseholdMember)
admin.site.register(HouseholdMemberDemographics)
admin.site.register(HouseholdMemberIncome)
admin.site.register(HouseholdReferral)
admin.site.register(Document)
