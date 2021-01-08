# Entries

import re
from bisect import bisect_left, bisect_right

import sr
from shire_calendar import Shiredate, calendar

#

class Entry(object):
    def __init__(self):
        self.text = ''
        self.characters = set()
        self.through = None
        self.types = []

    def __cmp__(self, other):
        if isinstance(other, Shiredate):
            return self.date.__cmp__(other)
        elif isinstance(other, Entry):
            return self.date.__cmp__(other.date)
        else:
            return id(self) - id(other)

    def render(self):
        if 'footnote' in self.types:
            return '<p class=footnote>[%s]</p>' % self.text.strip()
        else:
            return '<p>%s</p>' % self.text

#

def load_entries():
    entries = []
    entry = None
    letter = 'a'
    for line in open('data/entries'):
        m = re.match(r'([A-Za-z]*): (.*)', line)
        if m:
            name, value = m.groups()
            if name == 'Year':
                year = int(value)
            elif name == 'Date':
                date = calendar[year, value]
                if entry is not None:
                    entries.append(entry)
                    if entry.date == date:
                        letter = chr(ord(letter) + 1)
                    else:
                        letter = 'a'
                else:
                    letter = 'a'
                entry = Entry()
                entry.date = date
                entry.tag = '%d-%s-%d%s' % (date.year, date.month,
                                            date.day, letter)
            elif name == 'Through':
                entry.through = calendar[year, value]

            elif name in ('Character', 'Characters'):
                characters = value.split()
                if 'company' in characters:
                    characters.remove('company')
                    characters.extend('Frodo Sam Merry Pippin Gandalf Aragorn'
                                      ' Boromir Legolas Gimli'.split())
                for character in characters:
                    entry.characters.add(character)

            elif name == 'Type':
                entry.types.extend(value.split())

        else:
            entry.text += line
            for character in sr.characters:
                if character in line:
                    entry.characters.add(character)
    entries.append(entry)
    return entries

# Read in all entries, storing them in a tuple for efficient slicing.

all_entries = tuple(load_entries())

# Return a list of entries for the given inclusive range of dates.

def get(date, date2=None):
    i0 = bisect_left(all_entries, date)
    i1 = bisect_right(all_entries, date2 or date)
    return all_entries[i0:i1]

def date_before(date):
    i = bisect_left(all_entries, date)
    if i == 0:
        return None
    else:
        return all_entries[i-1].date

def date_after(date):
    i = bisect_right(all_entries, date)
    if i == len(all_entries):
        return None
    else:
        return all_entries[i].date

# Return the "last few" entries on or before a given date, trying to
# go back far enough to include entries for the previous "howmany"
# interesting dates.

def lastfew(date, howmany):
    i = j = bisect_right(all_entries, date) - 1
    dates_seen = 0
    last_date = None
    while i >= 0:
        entry = all_entries[i]
        if entry.date != last_date:
            last_date = entry.date
            dates_seen += 1
            if dates_seen > howmany:
                break
        i -= 1
    return all_entries[j:i+1:-1]

# Return a list of "recent" entries, defined as entries on or before
# the given date, but not more than the "limit" number of days before.

def recent(date, limit):
    entries = [ ]
    i = bisect_right(all_entries, date) - 1
    while i >= 0:
        entry = all_entries[i]
        days_ago = date - entry.date
        if days_ago > limit:
            break
        entries.append(entry)
        entry.days_ago = days_ago
        i -= 1
    return entries

# Return a list of entries, sorted most-recent-first, that includes
# all entries for the given "date", plus whatever earlier entries are
# necessary to make sure each of the characters in the collection
# "mentions" are mentioned at least once in the list of entries.

def search(date, mentions):
    mentions = set(mentions)            # so we can modify it
    entries = [ ]
    i = bisect_right(all_entries, date)
    while i and mentions:
        i -= 1
        entry = all_entries[i]
        if entry.date == date or (entry.date < date
                                  and entry.characters & mentions):
            entries.append(entry)
            entry.days_ago = date - entry.date
            mentions -= entry.characters
    return entries

# Given a flat list of entries, group adjacent entries that have the
# same date, producing a list of lists.

def group_by_date(entries):
    glist = []
    group = None
    for entry in entries:
        if group and group[0].date == entry.date:
            group.append(entry)
        else:
            group = [ entry ]
            glist.append(group)
    return glist
