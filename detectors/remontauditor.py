import urllib
import sys
import os, inspect

tracker_home = os.path.dirname(os.path.abspath(
	inspect.getfile(inspect.currentframe()))) + '/..'
sys.path.append(tracker_home)
import search_py2

def check_dates(db, cl, nodeid, newvalues):
    dates = newvalues['dates']

    if len(dates) < 1:
	raise ValueError, 'Potrzebne są przynajmniej przybliżone daty ' + \
            'rozpoczęcia i zakończenia prac'

def flush_dates(db, cl, nodeid, oldvalues):
    # TODO: drop nameddate objects that have been unlinked from the issue
    # object

def add_location(db, cl, nodeid, newvalues):
    ll = ( newvalues['lat'], newvalues['lon'] )
    #ret = search_py2.reverse(ll)['result']
    try:
        ret = search_py2.reverse(ll)['addressparts']

	if 'state' in ret:
	    ret['state'] = ret['state'].replace('województwo ', '')
	parts = [ 'road', 'village', 'town', 'city', 'county', 'state' ]

	if 'county' in ret and 'city' in ret and \
		ret['county'] == ret['city']:
	    parts.remove('county')
	if 'county' in ret and 'town' in ret and \
		ret['county'] == ret['town']:
	    parts.remove('county')

	newvalues['location'] = ', '.join([ ret[l] for l in parts if l in ret ])

	if 'country' in ret and ret['country'] != 'Polska':
	    newvalues['location'] += ', ' + ret['country']
    except:
	newvalues['location'] = str(ll)
	raise

def init(db):
    # fire before changes are made
    db.issue.audit('set', check_dates)
    db.issue.audit('create', check_dates)
    db.issue.audit('create', add_location)

    # fire after changes are made
    db.issue.audit('set', flush_dates)

# vim: set filetype=python ts=4 sw=4 et si fileencoding=utf8
#SHA: 3aafc622e20d33a2eb101ae4763158f5bc040bc6
