import re

sub_links = [
    ( re.compile('\\buser:(?P<u>\w+)'),
      '<a href="http://www.openstreetmap.org/user/\g<u>">user:\g<u></a>' ),
    ( re.compile('\#(?P<ws>\s*)(?P<id>\d+)\\b'),
      '<a href="issue\g<id>">#\g<ws>\g<id></a>' ),
]
sub_nolinks = [
    ( re.compile('\\bDW(\s+nr\.?)?\s*(?P<num>\d\d\d)\\b'),
      '<span class="droga-w">\g<num></span>' ),
    ( re.compile('\\bDK(\s+nr\.?)?\s*(?P<num>\d\d?)\\b'),
      '<span class="droga-k">\g<num></span>' ),
    ( re.compile('\\b(?P<num>E\s*\d\d\d?)\\b'),
      '<span class="droga-e">\g<num></span>' ),
    ( re.compile('\\b(?P<num>A\s*\d)\\b'),
      '<span class="droga-a">\g<num></span>' ),
    ( re.compile('\\b(?P<num>S\s*\d\d?)\\b'),
      '<span class="droga-s">\g<num></span>' ),
]

def prettify(message):
    if not message:
	return ''
    for cre, replacement in sub_links + sub_nolinks:
        message = cre.sub(replacement, message)

    return message

def prettify_nolink(message):
    if not message:
	return ''
    for cre, replacement in sub_nolinks:
        message = cre.sub(replacement, message)

def location_link(issue):
    if not issue:
	return ''
    dist = 400 # metres
    left = float(issue.lon) - 360.0 * (dist / 0.5 / 40000000)
    right = float(issue.lon) + 360.0 * (dist / 0.5 / 40000000)
    top = float(issue.lat) + 360.0 * (dist / 40000000)
    bottom = float(issue.lat) - 360.0 * (dist / 40000000)
    src = 'remonty.openstreetmap.pl%2Fremonty%2Fissue' + str(issue.id)

    osmlink  = 'http://osm.org/#map=' + str(issue.z) + '/' + \
	 str(issue.lat) + '/' + str(issue.lon)
    josmlink = 'http://127.0.0.1:8111/load_and_zoom?left=' + str(left) + \
	'&right=' + str(right) + '&top='  + str(top) + \
	'&bottom=' + str(bottom) + '&changeset_source=' + src + \
	'&changeset_comment=Aktualizacja%20remontu'

    return '<a href="issue' + str(issue.id) + '">' + \
	str(issue.location) + '</a><span class="permalinks">' + \
	'(<a href="' + osmlink + '">osm</a>)' + \
	'(<a href="' + josmlink + '">JOSM</a>)' + '</span>'

def init(instance):
    instance.registerUtil('prettify', prettify)
    instance.registerUtil('prettify_nolink', prettify_nolink)
    instance.registerUtil('location_link', location_link)

if "__main__" == __name__:
    print " user:222", prettify(" user:222")
    print " #555", prettify(" #555")
    print " DW 555", prettify(" DW 555")
    print " DK55", prettify(" DK55")
    print " E 555", prettify(" E 555")
    print " A7", prettify(" A7")
    print " S8", prettify(" S8")
