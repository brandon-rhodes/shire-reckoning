# -*- coding: utf-8 -*-

from __future__ import division

import re, sys
from math import *
from sr_svg import SVG

i = int(re.search(r'\d+', sys.argv[1]).group(0))

svg = SVG(sys.stdout, 24, 24)

svg.element('rect', x=0, y=0, width=24, height=24, fill='black', stroke_width=0)

svg.write('<clipPath id="lefthalf">')
svg.element('rect', x=0, y=0, width=12, height=24, fill='white', stroke_width=0)
svg.write('</clipPath>')

svg.write('<clipPath id="righthalf">')
svg.element('rect', x=12, y=0, width=12, height=24, fill='white', stroke_width=0)
svg.write('</clipPath>')

# 1st q: left black, right black -> white from right -> white
# 2nd q: left black -> white from right -> white, right white
# 3rd q: left white, right white -> black from right -> black
# 4th q: left white -> black from right -> black, right black

radius = 10
black, white = '#585858', '#ffffff'

steps = 72
halfsteps = steps/2
if i < halfsteps:
    oldcolor, newcolor = black, white
else:
    oldcolor, newcolor = white, black

j = i % halfsteps
x = radius * cos(pi*j/halfsteps)

def do(x, whichhalf, bgcolor, fgcolor):
    halfurl = 'url(#%shalf)' % whichhalf
    svg.element('circle', cx=12, cy=12, r=radius, fill=bgcolor,
                stroke_width=0, clip_path=halfurl)
    if x:
        svg.element('ellipse', cx=12, cy=12, rx=x, ry=radius, fill=fgcolor,
                    stroke_width=0, clip_path=halfurl)

if abs(x) < radius * 0.97:
    x *= 0.85

if x > 0:
    do(0, 'left', oldcolor, newcolor)
    do(x, 'right', newcolor, oldcolor)
else:
    do(-x, 'left', oldcolor, newcolor)
    do(0, 'right', newcolor, oldcolor)

svg.close()
