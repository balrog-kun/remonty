#! /usr/bin/python2

import sys, os, time, datetime

# runner.ts needs to be in the same directory as this executable / module
ts_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '/runner.ts'

# Time of day at which to do our email sending and/or note creation every
# day: 9am.  Anything submitted as opened-today or closed-today after that
# time in the day (i.e. when the information wasn't in the database ahead
# of that date) will not have a note created automatically here.
cutoff_time = datetime.time(9, 0)

def get_timestamp():
	return os.path.getmtime(ts_path)

def set_timestamp(ts):
	#if not os.path.exists(ts_path):
	#	open(ts_path, 'a').close()
	ts = time.mktime(ts.timetuple())
	os.utime(ts_path, ( ts, ts ))

def process_date(yr, mo, dy):
	# TODO: if too far in the past perhaps don't bother doing anything?
	print('Processing ' + str((yr, mo, dy)))

while True:
	last_day = datetime.date.fromtimestamp(get_timestamp())
	today = datetime.datetime.today()

	# It's not today until the cutoff time
	if today.time() < cutoff_time:
		today = today - datetime.timedelta(1)
	today = today.date()

	# Run the backlog until last_ts is today
	while last_day < today:
		last_day = last_day + datetime.timedelta(1)
		process_date(last_day.year, last_day.month, last_day.day)
		set_timestamp(last_day)

	# Wait for the next cutoff time
	tomorrow = datetime.datetime.combine(
			last_day + datetime.timedelta(1),
			cutoff_time)
	print('Sleeping until ' + str(tomorrow))
	time.sleep(time.mktime(tomorrow.timetuple()) - time.time())
