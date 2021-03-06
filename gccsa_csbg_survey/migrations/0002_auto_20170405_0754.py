# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('gccsa_csbg_survey', '0001_initial'),
	]

	operations = [
		migrations.RemoveField(
			model_name='householdmemberdemographics',
			name='birthdate',
		),
		migrations.RemoveField(
			model_name='householdmemberdemographics',
			name='gender',
		),
		migrations.AddField(
			model_name='householdmember',
			name='birthdate',
			field=models.DateField(null=True, verbose_name='Birth Date'),
		),
		migrations.AddField(
			model_name='householdmember',
			name='gender',
			field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True, verbose_name='Gender'),
		),
		migrations.AlterField(
			model_name='document',
			name='doc_url',
			field=models.FileField(upload_to='/'),
		),
	]
