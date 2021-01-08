#!/usr/bin/env python
#
# Test suite for the shire_calendar module.

import traceback
from shire_calendar import calendar

successes = 0

def report(error_message=None):
    global successes
    if error_message:
        print 'line %d.' % traceback.extract_stack()[0][1],
        print 'Error', error_message
    else:
        successes += 1

# Test whether the various date constructors work correctly.

def test(sd, year, month, day):
    if (sd.year, sd.month, sd.day) == (year, month, day):
        report()
    else:
        report('date %s != %s %s %s' % (sd, year, month, day))

test(calendar[1419, 'September 22'], 1419, 'September', 22)
test(calendar[1419, 'Midyear'], 1419, 'Midyear', 1)
test(calendar[1419, 'Overlithe'], 1419, 'Overlithe', 1)
test(calendar[1419, 'December 30'], 1419, 'December', 30)
test(calendar[1419, 'Lithe 1'], 1419, 'Lithe', 1)

# Determine both whether asking for a particular day of the year
# works, and also whether Shiredate objects correctly report their own
# day of the year.

def doytest(n, month, day, is_leapyear=False):
    m, d = calendar.day_of_year(n, is_leapyear)
    if m != month or d != day:
        report('date %s %s != %s %s' % (month, day, m, d))
    else:
        sd = calendar[1419 + bool(is_leapyear), month, day]
        if sd.day_of_year() != n:
            report('date %s returns day_of_year %d != %d' % (sd.day_of_year(), n))
        else:
            report()

doytest(1, 'Yule', 2)                   # for a non-leap-year
doytest(2, 'January', 1)
doytest(3, 'January', 2)
doytest(180, 'June', 29)
doytest(181, 'June', 30)
doytest(182, 'Lithe', 1)
doytest(183, 'Midyear', 1)
doytest(184, 'Lithe', 2)
doytest(185, 'July', 1)
doytest(186, 'July', 2)
doytest(363, 'December', 29)
doytest(364, 'December', 30)
doytest(365, 'Yule', 1)

doytest(1, 'Yule', 2, True)             # same tests for a leap year
doytest(2, 'January', 1, True)
doytest(3, 'January', 2, True)
doytest(180, 'June', 29, True)
doytest(181, 'June', 30, True)
doytest(182, 'Lithe', 1, True)
doytest(183, 'Midyear', 1, True)
doytest(184, 'Overlithe', 1, True)
doytest(185, 'Lithe', 2, True)
doytest(186, 'July', 1, True)
doytest(187, 'July', 2, True)
doytest(364, 'December', 29, True)
doytest(365, 'December', 30, True)
doytest(366, 'Yule', 1, True)

# Use the examples from the bottom of calendar.html to determine
# whether conversion to and from Gregorian dates occurs correctly.

def gregtest(gyear, gmonth, gday, month, day):
    cm, cd = calendar.gregorian(gyear, gmonth, gday)
    if (cm, cd) == (month, day):
        report()
    else:
        report('Gregorian %s %s %s returned %s %s, not %s %s'
               % (gyear, gmonth, gday, cm, cd, month, day))

gregtest(2005,2,27, 'March',8)          # non leap year
gregtest(2005,2,28, 'March',9)
gregtest(2005,3,1, 'March',10)
gregtest(2005,3,2, 'March',11)
gregtest(2005,6,18, 'June',29)
gregtest(2005,6,19, 'June',30)
gregtest(2005,6,20, 'Lithe',1)
gregtest(2005,6,21, 'Midyear',1)
gregtest(2005,6,22, 'Lithe',2)
gregtest(2005,6,23, 'July',1)
gregtest(2005,6,24, 'July',2)

gregtest(2008,2,27, 'March',8)          # leap year
gregtest(2008,2,28, 'March',9)
gregtest(2008,2,29, 'March',10)
gregtest(2008,3,1, 'March',11)
gregtest(2008,3,2, 'March',12)
gregtest(2008,6,17, 'June',29)
gregtest(2008,6,18, 'June',30)
gregtest(2008,6,19, 'Lithe',1)
gregtest(2008,6,20, 'Midyear',1)
gregtest(2008,6,21, 'Overlithe',1)
gregtest(2008,6,22, 'Lithe',2)
gregtest(2008,6,23, 'July',1)
gregtest(2008,6,24, 'July',2)

# Finish.

print successes, 'test cases ran successfully'
