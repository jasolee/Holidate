from django.apps import AppConfig
# from django_cron import CronJobBase, Schedule
# from datetime import datetime
# import psycopg2

#!/usr/bin/python

hostname = 'localhost'
username = 'postgres'
password = 'admin'
database = 'cal_data'

# Simple routine to run a query on a database and print the results:
# def doQuery( conn ) :
# 	today = datetime.datetime.today()
# 	cur = conn.cursor()
# 	cur.execute("SELECT PK, s_date, e_date, name, reason FROM timeline_employee")
# 	for i, s_date, e_date, name, reason in cur.fetchall():
# 		ur.execute("INSERT INTO timeline_past_hyuga VALUES(name, s_date, e_date, reason)")
# 		cur.execute("DELETE FROM timeline_hyuga WHERE PK = i")

# class MyCronJob(CronJobBase):
#     RUN_EVERY_MINS = 5 # every hour

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'timeline.cron_update'    # a unique code

#     def update_daily(self):
#     	myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
#     	doQuery( myConnection )
#     	myConnection.close()

# class TimelineConfig(AppConfig):
#     name = 'timeline'

# import hmac
# import hashlib

# hmac.new(
#   '_hvjqP-LgV31LhwarYEPxJekT8u04HRdayQDwBOM', # secret key (keep safe!)
#   request.user.id, # user's id
#   digestmod=hashlib.sha256 # hash function
# ).hexdigest()