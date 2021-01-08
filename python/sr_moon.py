# Moon phase, where "fraction" can be the fraction of a day; the
# "offset" gives how far into the year 1418 the first new moon occurs.

from shire_calendar import calendar
import math, ephem

twopi = 2 * math.pi
y1419 = calendar[1419, 'Yule', 2].ordinal()
gbase = ephem.date('1941/12/25')

# We ignore the moon.phase attribute, since it merely gives percent
# illumination; instead we need how far around the moon its terminator
# has progressed this month.

# --    .25     .5    -     --
# 0     .25     .5    .75    1

def adjust(phase):
    #adjustment = .05 * (max(0, 1 - 4 * phase) +
    #                    max(0, 2 * phase - 1))
    #adjustment = .1 * abs(phase - 0.5)
    if phase < 0.25:
        adjustment = .05 * (1 - 4 * phase)
    elif phase > 0.5:
        adjustment = .05 * (2 * phase - 1)
    else:
        adjustment = 0
    return (phase + adjustment) % 1.0
    #return realphase
    #adjustment = .1 * max(0, .375 - abs(phase - 0.875))

def phase(shiredate, fraction=0.0):
    d = gbase + shiredate.ordinal() - y1419 + fraction
    moon = ephem.Moon(d)
    realphase = ((moon.colong + moon.libration_long) / twopi + 0.25) % 1.0
    return adjust(realphase)

def img(phase, attributes=''):
    if attributes:
        attributes = ' ' + attributes
    return ('<img src="/images/phases/%d.png" height=24 width=24'
            ' alt="moon %.1f%% full"%s>' % (
        int(72 * phase), phase * 100, attributes))
