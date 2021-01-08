# -*- coding: utf-8 -*-

import sys
from sr_svg import SVG
from shire_calendar import calendar

svg = SVG(sys.stdout, 631, 124)
write = svg.write
element = svg.element
dark = '#585858'

def dayx(dayname):
    return (calendar[1419, dayname].day_of_year() - 2) * 7

write('<g transform="translate(0,100)">')

# Text with white around it.

def wtext(x, y, s, color='black'):
    element('text', s, x=x, y=y, stroke_width=5, stroke='white',
            font_family='sans', font_weight='bold', font_size=9,
            style='text-anchor: middle')
    element('text', s, x=x, y=y, stroke_width=0, fill=color,
            font_family='sans', font_weight='bold', font_size=9,
            style='text-anchor: middle')


# Day boxes.

element('rect', x=0, y=0, width=210, height=7,
        fill='#00ffff', stroke_width=0)
element('rect', x=210, y=0, width=210, height=7,
        fill='#c0ffff', stroke_width=0)
element('rect', x=420, y=0, width=210, height=7,
        fill='#c0ff40', stroke_width=0)

element('line', x1=0, x2=631, y1=0.5, y2=0.5,
        stroke='black', stroke_width=1)
element('line', x1=0, x2=631, y1=7.5, y2=7.5,
        stroke='black', stroke_width=1)
for x in 210.5, 420.5:
    element('line', x1=x, x2=x, y1=7, y2=24,
            stroke='black', stroke_width=1)
for i in range(91):
    x = i * 7 + 0.5
    element('line', x1=x, x2=x, y1=0, y2=7,
            stroke='black', stroke_width=1)

# Month names.

element('text', 'January', x=105, y=19, stroke_width=0, fill='black',
        font_family='sans', font_weight='bold', font_size=9,
        style='text-anchor: middle')
element('text', 'February', x=315, y=19, stroke_width=0, fill='black',
        font_family='sans', font_weight='bold', font_size=9,
        style='text-anchor: middle')
element('text', 'March', x=525, y=19, stroke_width=0, fill='black',
        font_family='sans', font_weight='bold', font_size=9,
        style='text-anchor: middle')

write('</g>')

# Moon.

x = dayx('March 24') + 6.5

svg.write('<clipPath id="halfmoon">')
element('rect', fill='white', stroke_width=0,
        x=-40, y=-40, width=40, height=80)
svg.write('</clipPath>')

for x, y, phase, label in (
    (dayx('January 8') + 5.5, 50, 'f', '8th'),
    (dayx('January 8') + 105.5, 50, 'n', None),
    (dayx('January 8') + 205.5, 50, 'f', None),
    (dayx('February 22') + 1.5, 50, 'n', '22nd or earlier'),
    (dayx('February 22') + 5.5, 80, 'c', '22nd'),
    (dayx('March 8') + 2.5, 50, 'f', '8th'),
    (dayx('March 22') + 1.5, 50, 'n', '22nd or earlier'),
    (dayx('March 24') + 5.5, 80, 'c', '24th'),
    ):

    write('<g transform="translate(%s,%s)">' % (x, y))

    # Label.

    if label:
        wtext(0, -11, label)

    # Black backdrop

    element('circle', cx=0, cy=0, r=10.5, stroke_width=0, fill='white')
    element('circle', cx=0, cy=0, r=9.5, stroke_width=0, fill='black')

    # Line connecting down to month bar.

    element('line', x1=0, x2=0, y1=0, y2=100-y, stroke_width=1, stroke='black')

    # Moon itself.

    if phase == 'n':
        element('circle', cx=0, cy=0, r=7, stroke_width=0, fill=dark)
    else:
        element('circle', cx=0, cy=0, r=7, stroke_width=0, fill='white')
        if phase == 'c':
            element('circle', cx=0, cy=0, r=7, stroke_width=0, fill=dark,
                    clip_path='url(#halfmoon)')
            element('ellipse', cx=0, cy=0, rx=4, ry=6.8,
                    stroke_width=0, fill=dark)

    write('</g>')

# Draw measurements.

limits = ( dayx('January 8') + 5.5, dayx('February 22') + 1.5,
           dayx('March 8') + 2.5, dayx('March 22') + 1.5, )

for i, (color, label, label2) in enumerate((
    ('black', '43 days', '(somewhat short)'),
    ('#c00000', 'more than 16 days', '(impossible)'),
    ('black', '14 days', '(fairly short)'),
    )):
    x1, x2 = limits[i], limits[i+1]
    xa = (x1 + x2) / 2

    element('line', x1=x1, x2=x1, y1=5.5, y2=25,
            stroke_width=1, stroke='black')
    element('line', x1=x1, x2=x1 + 4, y1=7.5, y2=5.5,
            stroke_width=1, stroke='black')
    element('line', x1=x1, x2=x1 + 4, y1=7.5, y2=9.5,
            stroke_width=1, stroke='black')

    element('line', x1=x2, x2=x2, y1=5.5, y2=25,
            stroke_width=1, stroke='black')
    element('line', x1=x2, x2=x2 - 4, y1=7.5, y2=5.5,
            stroke_width=1, stroke='black')
    element('line', x1=x2, x2=x2 - 4, y1=7.5, y2=9.5,
            stroke_width=1, stroke='black')

    element('line', x1=x1, x2=x2, y1=7.5, y2=7.5,
            stroke_width=1, stroke='black')

    wtext(xa, 10, label, color=color)
    wtext(xa, 22, label2, color=color)

svg.close()
