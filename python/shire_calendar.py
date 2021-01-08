# The Shire Calendar

import operator, time
from bisect import *

month_list = ([ (i*30, m) for i, m in enumerate(
    ['July', 'August', 'September', 'October', 'November', 'December', 'Yule']
    ) ] + [ (i*30 + 182, m) for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'Lithe']
    ) ] + [ (363, 'Midyear'), (364, 'Overlithe') ])

month_dict = dict( (k,v) for (v,k) in month_list )

# The Shiredate represents a particular day of a particular year.

class Shiredate(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        if month in ('Midyear', 'Overlithe'):
            self.name = month
        else:
            self.name = '%s %d' % (month, day)

    def __str__(self):
        return '<%s %d, %d S.R.>' % (self.month, self.day, self.year)

    def __cmp__(self, d):
        if isinstance(d, Shiredate):
            return cmp(self.ordinal(), d.ordinal())
        elif hasattr(d, 'date'):
            return cmp(self.ordinal(), d.date.ordinal())
        else:
            return id(self) - id(d)

    def __sub__(self, d):
        return self.ordinal() - d.ordinal()

    # Determine whether this is a leap year.

    def is_leapyear(self):
        return not (self.year % 4) and bool(self.year % 100)

    # Determine ...

    def index(self):
        month, day = self.month, self.day
        if month == 'Lithe' and day == 2:
            return 0
        return month_dict[month] + day

    # First day of the week returns 0, last day returns 6.

    def day_of_week(self):
        i = self.index()
        if i < 364:
            return i % 7
        return None

    # Determine which day of the year this is (with the first day of
    # the year being 1, and the last being 365 or 366).

    def day_of_year(self):
        i = self.index()
        leap = self.is_leapyear()
        return (i + 183 + leap) % (365 + leap) + 1

    # Return which day this is since the beginning of year S.R. 1
    # (where the first day of S.R. 1 itself gets the ordinal 1).

    def ordinal(self):
        y = self.year - 1
        return y*365 + y/4 - y/100 + self.day_of_year()

#

class Calendar(object):

    # Retrieve an object from the calendar; possible forms of the
    # "selector" argument are given in the comments that follow.

    def __getitem__(self, selector):

        if isinstance(selector, str):
            year, month, day = selector.strip().split()
            return Shiredate(int(year), month, int(day))

        elif isinstance(selector, tuple) or isinstance(selector, list):
            if len(selector) == 2:
                # calendar[1418, 'September 22']
                # calendar[1418, 'Midyear']
                year, monthday = selector
                if ' ' not in monthday:
                    month, day = monthday, 1
                else:
                    month, day = monthday.strip().split()
                return Shiredate(int(year), month, int(day))

            elif len(selector) == 3:
                # calendar[1418, 'September', 22]
                year, month, day = selector
                return Shiredate(int(year), month, int(day))

        raise RuntimeError, 'Cannot build date from %r' % (selector,)

    # Return the month and day...

    def day_of_index(self, i):
        j = bisect_left(month_list, (i, None))
        if not j: return ('Lithe', 2)
        offset, month = month_list[j-1]
        return month, i - offset

    # Return the month and day of the n'th day of the year, where d=1
    # returns the first day ('Yule', 2).

    def day_of_year(self, nth, is_leapyear=False):
        leap = bool(is_leapyear)
        i = (nth - 184 - leap) % (365 + leap)
        return self.day_of_index(i)

    # Retrieve the name of the Shire day that corresponds to a
    # particular date in the Gregorian calendar.

    def gregorian_solar(self, year, month, day):
        # Determine difference between date and previous 22 June
        def gr(year, month, day):
            return round(time.mktime((year, month, day+1, 0,0,0,0,0,0)) / 86400.)
        d = gr(year, month, day)
        june22 = gr(year, 7, 2)  #makes October match
        if d < june22: june22 = gr(year - 1, 6, 22)
        return self.day_of_index(int(d - june22))

    def gregorian(self, year, month, day):
        # Determine difference between date and previous 1 June
        def gr(year, month, day):
            return round(time.mktime((year, month, day+1, 0,0,0,0,0,0)) / 86400.)
        d = gr(year, month, day)
        june22 = gr(year, 6, 22)  #makes October match
        if d < june22: june22 = gr(year - 1, 7, 1)
        return self.day_of_index(int(d - june22))

# Create a calendar instance that clients can easily import.

calendar = Calendar()
