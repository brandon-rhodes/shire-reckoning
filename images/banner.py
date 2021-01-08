# -*- coding: utf-8 -*-

import sys
from sr_svg import SVG

svg = SVG(sys.stdout, 960, 40)

svg.element('rect', x=0, y=0, width=1024, height=36,
            fill='#600000', stroke_width=0)
svg.element('line', x1=0, x2=1024, y1=4.5, y2=4.5,
            stroke='#ffffb0', stroke_width=1)
svg.element('line', x1=0, x2=1024, y1=7.5, y2=7.5,
            stroke='#ffffb0', stroke_width=1)
svg.element('line', x1=0, x2=1024, y1=32.5, y2=32.5,
            stroke='#ffffb0', stroke_width=1)
svg.element('line', x1=0, x2=1024, y1=35.5, y2=35.5,
            stroke='#ffffb0', stroke_width=1)

# Original text submitted to http://www.tengwar.art.pl/tengwar/ott/start.php
#
# Narvinyë Nénimë Súlìmë Víressë Lótessë Náríë Cermië Urimë Yavannië
# Narquelië Hísimë Ringarë. (as Quenya)
#
# Narwain Nínui Gwaeron Gwirith Lothron Nórui Cerveth Urui Ivanneth
# Narbeleth Hithui Girithron. (as Sindarin)
#
# Then this was organized as the last six Sindarin names, then all
# twelve Quenya month names, then the first six Sindarins names - so
# that when this image is centered and possibly truncated, the pretty
# Quenya names are in the middle.

svg.element('text',
            'al7rl3 .7.Õ `r]5l3 6]7wljl3 9`3.Õ s`7`37h6- '
            '5#6yT5Ì$ 5~V5%t$ 8~Mjt$ y~B7R,R j~N1R,R 5~C7~B`V '
            'aR6t%`V `M7Tt$ hÍEyE5"%`V 5#6zRjT`V 9~BiTt$ 7Ts#7R- '
            '6]7é]Õ6 6`V6.Õ sè]Ý7h6 sè`7`3 jh37h6 6hF7.Õ '
            , x=3, y=22, stroke='#ffffb0', fill='#ffff80', stroke_width=0.5,
            font_family='Tengwar Elfica', font_weight='normal', font_size=12)

svg.close()
