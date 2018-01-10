
"""Script to create DB dump"""


from datetime import datetime, timedelta
import smtplib
import os
import string

PATH = '/Users/abhishek/Desktop/backup'
def postgredump():
	"""Dump the postgreSQL
	"""
	msg = 'postgresql DB dump successfull'
	user_name = 'root'
	password  = 'root'
	db_name   = 'rubanbridge'

	try:
		#import pdb;pdb.set_trace()
		cmd = 'pg_dump %s | gzip > %s/postgresql/%s_%s.gz' % \
				(db_name, PATH, db_name, datetime.now().strftime('%d%m%Y_%H'))
		#print cmd
		os.system(cmd)

	except:
		msg = "postgreSQL DB Dump Failed"

	return msg


def mysql_dump():
	"""Dump the MySQL DB
	"""
	msg = 'MySQL DB dump successfull'
	user_name = 'root'
	password  = 'root'
	db_name   = 'nextpulse'
	try:
		cmd = 'mysqldump -u %s --password=%s %s > %s/mysql/%s_%s.sql' % \
				(user_name, password, db_name, PATH, db_name, datetime.now().strftime('%d%m%Y_%H'))
		#print cmd
		os.system(cmd)

	except:
		msg = "MySQL DB Dump Failed"

	return msg

def send_mail(message):
	"""send mail regarding result of DUMP
	"""

	server = smtplib.SMTP('smtp3.netcore.co.in', 587)

	#Next, log in to the server
	server.login("abhishek.m@1bridge.one", "Abhishek123#")

	#Send the mail
	BODY = string.join((
            "From: abhishek.m@1bridge.one",
            "To: abhishek.m@1bridge.one",
            "Subject: Mail Backup Status Testing",
            "",
            message
            ), "\r\n")
	#server.sendmail("abhishek.m@1bridge.one", ["abhishek.m@1bridge.one", "prabhakar.s@1bridge.one"], BODY)
	server.sendmail("abhishek.m@1bridge.one", ["abhishek.m@1bridge.one"], BODY)

def main():
	"""Main function to dump the DBs
	"""
	msg = 'Hi Abhishek, Prabhakar \n \n'
	msg += '\n' + postgredump()
	msg += '\n' + mysql_dump()

	send_mail(msg)


if __name__ == '__main__':
	main()