import urllib
import os, inspect

tracker_home = os.path.dirname(os.path.abspath(
	inspect.getfile(inspect.currentframe()))) + '/..'
sys.path.append(tracker_home)

def check_dates(db, cl, nodeid, newvalues):
    dates = urllib.unquote(newvalues['dates'])
    dates = [ v.split('.', 3) for v in dates.split('\n') ]

    if len(dates) < 2:
	raise ValueError, 'Potrzebne są przynajmniej przybliżone daty ' + \
            'rozpoczęcia i zakończenia prac'
    prev = ( 0, 0, 0 )
    for yr, mo, dy, desc in dates:
	date = ( int(yr), int(mo), int(dy) )
	if date[0] < 1980 or date[0] > 2030:
	    raise ValueError, 'Data ' + str(date) + ' jest zbyt odległa'
        if date[1] < 0 or date[1] > 11:
	    raise ValueError, 'Nieprawidłowy miesiąc'
        if date[2] < 1 or date[2] > 31:
	    raise ValueError, 'Nieprawidłowy dzień miesiąca'
        if date[0] < prev[0] or (date[0] == prev[0] and (date[1] < prev[1] or
		(date[1] == prev[1] and date[2] < prev[2]))):
	    raise ValueError, 'Zła kolejność'

def init(db):
    # fire before changes are made
    db.issue.audit('set', check_dates)
    db.issue.audit('create', check_dates)

# vim: set filetype=python ts=4 sw=4 et si
#SHA: 3aafc622e20d33a2eb101ae4763158f5bc040bc6
