#! /usr/bin/python2

import sys, os, time, datetime, urllib
import xml.etree.cElementTree as ElementTree

tracker_home = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(tracker_home + '/..')

import roundup.instance

# runner.ts needs to be in the same directory as this executable / module
ts_path = tracker_home + '/runner.ts'

# Time of day at which to do our email sending and/or note creation every
# day: 9am.  Anything submitted as opened-today or closed-today after that
# time in the day (i.e. when the information wasn't in the database ahead
# of that date) will not have a note created automatically here.
cutoff_time = datetime.time(9, 0)

noteapi = 'http://api.openstreetmap.org/api/0.6/notes'

statusmap = {
	"1": "4", # nie-rozpoczety -> w-trakcie-do-poprawienia
	"2": "4", # w-trakcie -> w-trakcie-do-poprawienia
	"5": "6", # zamkniety -> zamkniety-do-poprawienia
}

stillpending = statusmap.values()

def post_note(desc, issueid, lat, lon, yr, mo, dy):
	req_params = {
		'lat': str(lat),
		'lon': str(lon),
		'text': ('Remonty %02i-%02i: ' % ( mo, dy )) + desc +
			' - zobacz http://remonty.openstreetmap.pl/' +
			'remonty/issue' + str(issueid)
	}

	conn = urllib.urlopen(noteapi, urllib.urlencode(req_params))
	try:
		newnote = conn.read()
	finally:
		conn.close()

	root = ElementTree.fromstring(newnote)
	if root.tag != 'osm':
		raise Exception('Root not osm in ' + newnote)

	for note in root:
		if note.tag != 'note':
			continue
		for prop in note:
			if prop.tag == 'id':
				return int(prop.text)

	raise Exception('Note id not found in ' + newnote)

def post_comment(noteid, desc, issueid, lat, lon, yr, mo, dy):
	req_params = {
		'text': ('Remonty %02i-%02i: ' % ( mo, dy )) + desc
	}

	conn = urllib.urlopen(noteapi + '/' + str(noteid) + '/comment',
			urllib.urlencode(req_params))
	try:
		newcomment = conn.read()
	finally:
		conn.close()

	root = ElementTree.fromstring(newcomment)
	if root.tag != 'osm':
		raise Exception('Root not osm in ' + newcomment)

	for note in root:
		if note.tag != 'note':
			continue
		for prop in note:
			if prop.tag == 'id':
				return int(prop.text)

	raise Exception('Note id not found in ' + newcomment)

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

	tracker = roundup.instance.open(tracker_home)
	db = tracker.open('admin')
	db.tx_Source = 'cli'
	dates = db.nameddate
	issues = db.issue

	current = dates.filter(None, {
		'date': '%02i-%02i-%02i' % (yr, mo, dy) })
	for dateid in current:
		desc = dates.get(dateid, 'desc')
		note = int(dates.get(dateid, 'note'))

		# 0 - create a note for this date
		# <int> - a note with id #<int> exists for this date
		# -1 - do not create any note for this date
		if note != 0:
			continue

		issueid = dates.get(dateid, 'issue')
		lat = issues.get(issueid, 'lat')
		lon = issues.get(issueid, 'lon')
		status = issues.get(issueid, 'status')

		if status in stillpending:
			# Check if we have a note for the previous date
			# in this issue
			# TODO: check if still open, perhaps reopen
			lastnote = None
			issuedates = issues.get(issueid, 'dates')
			for issuedateid in issuedates:
				prevnote = int(dates.get(issuedateid, 'note'))
				if prevnote <= 0:
					continue
				if lastnote is not None and lastnote > prevnote:
					continue
				lastnote = prevnote

		if status in statusmap:
			issues.set(issueid, status=statusmap[status])
			# TODO: if last date in this issue, set status to
			# zamkniety-do-poprawienia instead of w-trakcie-do-p.

		try:
			if status not in stillpending or lastnote is None:
				noteid = post_note(desc, issueid,
						lat, lon, yr, mo, dy)
				print('note #' + str(noteid) + ' created')
			else:
				noteid = lastnote
				post_comment(noteid, desc, issueid,
						lat, lon, yr, mo, dy)
				print('commented on note #' + str(noteid))
		except Exception as e:
			print('Could not create a note for date ' +
					str(dateid) + ': ' + str(e))
			continue
		try:
			dates.set(dateid, note=noteid)
			db.commit()
		except Exception as e:
			print('Could not save the new note for date ' +
					str(noteid) + ': ' + str(e) +
					'\n - please check!')
			continue
	db.close()

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
