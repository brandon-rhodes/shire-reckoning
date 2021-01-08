# -*- coding: utf-8 -*-

import re, sys
from math import *
from sr_svg import SVG

svg = SVG(sys.stdout, 140, 90, 'x="-6"')
element = svg.element

which = re.search(r'(.)\.', sys.argv[1]).group(1)
dark = '#585858'

# Dome of "snow globe"

svg.write('<clipPath id="tophalf">')
element('rect', x=0, y=0, width=120, height=60, fill='white', stroke_width=0)
svg.write('</clipPath>')

element('circle', cx=60, cy=60, r=60,
        stroke_width=0, fill='black', clip_path='url(#tophalf)')

# Dotted line of travel

if which == '1':
    x, w = 90, 30
elif which == '2':
    x, w = 30, 90
elif which == 'F':
    x, w = 0, 120
elif which == '3':
    x, w = 0, 90
elif which == '4':
    x, w = 0, 30

svg.write('<clipPath id="travelpath">')
element('rect', x=x, y=0, width=w, height=60, fill='white', stroke_width=0)
svg.write('</clipPath>')

element('ellipse', cx=60, cy=60, rx=43, ry=43, fill='none',
        stroke_width=2, stroke='#909090', clip_path='url(#travelpath)',
        stroke_dasharray='5,2')

# Bottom of "snow globe"

element('ellipse', cx=60, cy=65, rx=60, ry=10,
        stroke_width=0, fill='#727250')
element('rect', x=0, y=60, width=120, height=5,
        stroke_width=0, fill='#727250')

element('ellipse', cx=60, cy=60, rx=60, ry=10,
        stroke_width=0, fill='#406040')

element('text', 'N', x=60, y=82, stroke_width=0, fill='black',
        font_family='sans', font_weight='bold', font_size=8,
        style='text-anchor: middle')
element('text', 'E', x=-1, y=70, stroke_width=0, fill='black',
        font_family='sans', font_weight='bold', font_size=8,
        style='text-anchor: end')
element('text', 'W', x=121, y=70, stroke_width=0, fill='black',
        font_family='sans', font_weight='bold', font_size=8,
        style='text-anchor: start')

# Directional arrow.

#svg.write('<g transform="%s">' % transform)
if which == '1':
    transform = 'rotate(69)'
elif which == '2':
    transform = 'rotate(15)'
elif which == 'F':
    transform = 'rotate(43)'
elif which == '3':
    transform = 'rotate(-13)'
elif which == '4':
    transform = 'rotate(-67)'


svg.write('<g transform="translate(60, 60) %s">' % transform)

svg.write('<clipPath id="arrowarc">')
element('polygon', fill='white', stroke_width=0,
        points="0,0 2,-60 -14,-60")
svg.write('</clipPath>')

element('circle', cx=0, cy=0, r=49, stroke='#909090', stroke_width=3,
        fill='none', clip_path='url(#arrowarc)')
element('polygon', stroke_width=0, fill='#909090',
        points='6,-49 0,-53 0,-45')

svg.write('</g>')

# Moon.

if which == '1':
    transform = 'translate(90 30) rotate(45 0 0)'
    slender = dark
elif which == '2':
    transform = 'translate(30 30) rotate(-45 0 0)'
    slender = 'white'
elif which == 'F':
    transform = 'translate(60 17)'
    slender = 'white'
elif which == '3':
    transform = 'translate(90 30) rotate(-135 0 0)'
    slender = 'white'
elif which == '4':
    transform = 'translate(30 30) rotate(135 0 0)'
    slender = dark

svg.write('<g transform="%s">' % transform)

element('circle', cx=0, cy=0, r=7, stroke_width=0, fill=dark)

svg.write('<clipPath id="halfmoon">')
element('rect', fill='white', stroke_width=0, x=0, y=-40, width=80, height=80)
svg.write('</clipPath>')

if which != 'F':
    element('circle', cx=0, cy=0, r=7,
            stroke_width=0, fill='white', clip_path='url(#halfmoon)')
    element('ellipse', cx=0, cy=0, rx=4, ry=6.8,
            stroke_width=0, fill=slender)
else:
    element('circle', cx=0, cy=0, r=7,
            stroke_width=0, fill='white')

svg.write('</g>')

svg.close()
