import urllib2, urllib
import json, csv
import pprint as pp
import random
import time
import gzip
from datetime import datetime, timedelta
import os, re, sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto

now = datetime.utcnow()
time_shift = now + timedelta(minutes=-15)
min_time = time_shift.strftime('%Y-%m-%d %H:%M:%S')

#convert day and hour to match filepath syntax
def get_month(month_count):
	if month_count < 10:
		month = '0' + str(month_count)
	else:
		month = str(month_count)
	return month

def get_day(day_count):
	if day_count < 10:
		day = '0' + str(day_count)
	else:
		day = str(day_count)
	return day
	
def get_hour(hour_count):
	if hour_count < 10:
		hour = '0' + str(hour_count)
	else:
		hour = str(hour_count)
	return hour

year = str(now.year)
month = get_month(now.month)
day = get_day(now.day)
hour = get_hour(now.hour)
minute = str(now.minute)

def get_json(url):
    try:
        src = urllib2.urlopen(url).read()
        rsp = json.loads(src)
    except:
        rsp = {}
    return rsp


base_uri = 'http://api.chartbeat.com/live/recent/v3/?apikey='
APIKEY = '317a25eccba186e0f6b558f45214c0e7'
HOST = 'avc.com'
query_url = base_uri + APIKEY + '&host=' + HOST + '&limit=2'

rsp = get_json(query_url)

local_filename = '/Users/samjulius/Desktop/chartbeat_data/y=' + year + '/m=' + month + '/d=' + day + '/h=' + hour + '/' + 'chartbeat_data_' + year + month + day + minute + '.gz'

with gzip.open(local_filename, 'w') as log_file:
	# utc_timestamp = datetime.fromtimestamp(int(token['utc'])).strftime('%Y-%m-%d %H:%M:%S')
	# if utc_timestamp >= min_time:
	for token in rsp:
		log_file.write(json.dumps(token) + '\n')

log_file.close()

#set filepath where you want to save file on s3
# s3_filename = '/chartbeat_data/y=' + year + '/m=' + month + '/d=' + day + '/h=' + hour + '/' + 'chartbeat_data_' + year + month + day + minute + '.gz'

# #write ledger to s3 folder for pickup
# s3 = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
# bucket = s3.get_bucket('metamx-shecht')
# key = bucket.new_key(s3_filename)
# key.set_contents_from_filename(ec2_filename)

# cred_file.close()

