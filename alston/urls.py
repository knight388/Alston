from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^csbg_survey/', include('gccsa_csbg_survey.urls')),
]
