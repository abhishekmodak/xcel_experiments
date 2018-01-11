
from django.core.management.base import BaseCommand, CommandError

import xlsxwriter
import os
import django
from datetime import datetime
from survey.models import *
from profiles.models import *
from survey_web_service.models import *
import csv
from django.utils.encoding import smart_str, smart_unicode
from django.core.mail import send_mail,EmailMessage

class Command(BaseCommand):
    def handle(*args, **options):
        st_time = datetime.now()
	insertion_list = []
        s = Survey.objects.get(id=104,active=2)
	usm = UserSurveyMap.objects.filter(survey=s,active=2,user__active=2).order_by('user__user__email')
    	insertion_list = []
    	answer_list = Answer.objects.filter(question__block__survey=s).order_by('question__code').exclude(user__id__in=[264,777])

        file_name = 'Outreach_Form.csv'
        with open(file_name, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                smart_str(u"App answer data"),
                smart_str(u"Consent status"),
                smart_str(u"User id"),
                smart_str(u"Email"),
                smart_str(u"Distict"),
                smart_str(u"Village"),
                smart_str(u"Select Date"),
                smart_str(u"Attendance in Village meeting"),
                smart_str(u"Type of Outreach"),
                smart_str(u"Outreach Topic"),
            ])

    	    if answer_list.count() >= 1:
		app_answer_ids = list(set(answer_list.values_list('app_answer_data',flat=True)))
		for appid in app_answer_ids:
	    	    anslist = answer_list.select_related('question','choice','user',\
				    'question__block__survey').filter(app_answer_data=appid)

	    	    anslist_obj = anslist[0].__dict__
	    	    surveyid = anslist_obj['_question_cache'].block.survey.id
	    	    anslist_obj_user = anslist_obj['_user_cache'].__dict__
	    	    userid, user_email = anslist_obj_user['id'], anslist_obj_user['email']
	    	    onebaname = anslist_obj_user['first_name'] + ' '+ anslist_obj_user['last_name']
	    	    creation_key = anslist_obj['creation_key']
	    	    app_answer_data = appid
	    	    app_answer_on = anslist_obj['app_answer_on'].strftime('%d-%m-%Y')
	    	    answer_created_on = anslist_obj['created'].date()
	    	    answer_submission_date = anslist_obj['submission_date'].date()
	    	    content_type, object_id = anslist[0].content_type.name, anslist_obj['object_id']

	    	    try:
		        gp = Village.objects.get(id=object_id).gramapanchayath.name
	    	    except:
		        gp = 'N/A'
	    	    try:
		        taluk = Village.objects.get(id=object_id).gramapanchayath.mandal.taluk.name
	    	    except:
		        taluk = 'N/A'
	    	    try:
		        district = Village.objects.get(id=object_id).gramapanchayath.mandal.taluk.district.name
	    	    except:
		        district = 'N/A'
	    	    try:
		        select_villagename = anslist.get(question__id=1947).text
	            except:
		        select_villagename = 'N/A'
	            try:
		        consent_status = anslist.get(question__id=1948).choice.text
	            except:
		        consent_status = 'N/A'
	            try:
		        date = anslist.get(question__id=1949).date
	            except:
		        date = ''
	            try:
		        attendance = anslist.get(question__id=1950).text
	            except:
		        attendance = ''
	            try:
		        reachtopic = anslist.filter(question__id=1951)[0].get_multi_ans()
	            except:
		        reachtopic = ''
	            try:
		        reachtype = anslist.get(question__id=1953).choice.text
	            except:
		        reachtype = ''

		    writer.writerow([
                            smart_str(app_answer_data),
                            smart_str(consent_status),
                            smart_str(userid),
                            smart_str(user_email),
                            smart_str(district),
                            smart_str(select_villagename),
                            smart_str(date),
                            smart_str(attendance),
                            smart_str(reachtype),
                            smart_str(reachtopic)
                        ])

	sub = 'Outreach Report for the day - '+ datetime.now().strftime('%d-%B-%Y')
        body = 'Dear Team, \n\n Please find the Outreach Report, attached along with this mail.'
        email = EmailMessage(sub, body, 'admin@1bridge.mahiti.org', \
                     ['abhishek.m@1bridge.one', 'manu.dawar@1bridge.one'],\
                     headers = {'Reply-To': 'admin@1bridge.org'})
        attachment = open(file_name, 'rb')
        email.attach(file_name,attachment.read(),'application/csv')
        email.send()
        end_time = datetime.now()
        print (end_time - st_time)
	return "Success"

	

