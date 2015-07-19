import re

sub_links = [
    ( re.compile('\\buser:(?P<u>\w+)'),
      '<a href="http://www.openstreetmap.org/user/\g<u>">user:\g<u></a>' ),
    ( re.compile('\#(?P<ws>\s*)(?P<id>\d+)\\b'),
      '<a href="issue\g<id>">#\g<ws>\g<id></a>' ),
]
sub_nolinks = [
    ( re.compile('\\b(?P<num>DW\s*\d\d\d)\\b'),
      '<span class="droga-w">\g<num></span>' ),
    ( re.compile('\\b(?P<num>DK\s*\d\d?)\\b'),
      '<span class="droga-k">\g<num></span>' ),
    ( re.compile('\\b(?P<num>E\s*\d\d\d?)\\b'),
      '<span class="droga-e">\g<num></span>' ),
    ( re.compile('\\b(?P<num>A\s*\d)\\b'),
      '<span class="droga-a">\g<num></span>' ),
    ( re.compile('\\b(?P<num>S\s*\d\d?)\\b'),
      '<span class="droga-s">\g<num></span>' ),
]

def prettify(message):
    for cre, replacement in sub_links + sub_nolinks:
        message = cre.sub(replacement, message)

    return message

def prettify_nolink(message):
    for cre, replacement in sub_nolinks:
        message = cre.sub(replacement, message)

    return message

def init(instance):
    instance.registerUtil('prettify', prettify)
    instance.registerUtil('prettify_nolink', prettify_nolink)

if "__main__" == __name__:
    print " user:222", prettify(" user:222")
    print " #555", prettify(" #555")
    print " DW 555", prettify(" DW 555")
    print " DK55", prettify(" DK55")
    print " E 555", prettify(" E 555")
    print " A7", prettify(" A7")
    print " S8", prettify(" S8")
