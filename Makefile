# Makefile for the Shire-Reckoning web site

SHELL=/bin/zsh
PYTHONPATH := ./python:$(PYTHONPATH)
export PYTHONPATH

# Define "all" as the default build target.

all:

# For each file in the ./events/ directory, create and include a rule
# that lists the dates for which the file provides entries.

#EVENT_FILES := $(wildcard events/*)
#EVENT_RULES := $(patsubst events/%, .make/%, $(EVENT_FILES))

#.DELETE_ON_ERROR: $(EVENT_RULES)
#$(EVENT_RULES): .make/%: events/% bin/event_rules python/sr_events.py
#	bin/event_rules events/$* > $@

#include $(EVENT_RULES)

# For each page to be produced in the ./docs/ directory, create and
# include a rule listing the dates for which the page will want to
# display events.

# INDEX_DATES := $(shell bin/index_dates)
# INDEX_FILES := $(patsubst %, docs/index-%.html, $(INDEX_DATES))
# $(INDEX_FILES): pages/index.ptl python/sr_moon.py

# ATOM_FILES := $(patsubst %, docs/atom-%.xml, $(INDEX_DATES))
# atom: $(ATOM_FILES)
# $(ATOM_FILES): pages/atom.ptl

INDEX_FILE := docs/index.html
$(INDEX_FILE): pages/index.ptl pages/index.html

CAL_FILE := docs/calendar.html
$(CAL_FILE): pages/calendar.ptl

FAQ_FILE := docs/faq.html
$(FAQ_FILE): pages/faq.ptl

MOON_FILE := docs/moon.html
$(MOON_FILE): pages/moon.ptl python/sr_moon.py data/moons

MOON_UPDATE_FILE := docs/moon-update.html
$(MOON_UPDATE_FILE): pages/moon.ptl

ARCHIVE_MONTHS := $(shell PYTHONPATH=$(PYTHONPATH) bin/archive_months)
ARCHIVE_FILES := docs/archive.html
ARCHIVE_FILES += $(patsubst %, docs/archive-%/index.html, $(ARCHIVE_MONTHS))

PAGE_FILES := $(INDEX_FILE) $(CAL_FILE) $(ARCHIVE_FILES) $(FAQ_FILE) $(MOON_FILE) $(MOON_UPDATE_FILE)

$(PAGE_FILES) $(ARCHIVE_FILES): python/sr_entries.py \
 data/entries python/sr_html.ptl
$(ARCHIVE_FILES): pages/archive.ptl python/sr_html.ptl python/sr_moon.py

# Actual page composition.

$(PAGE_FILES): docs/%.html: bin/page_compose python/shire_calendar.py \
 python/design.ptl python/sr_entries.py data/transforms.py data/tidy.conf
	$(PYTHON) bin/page_compose $* .page
	mkdir -p $$(dirname $@)
	mv .page $@

all: $(PAGE_FILES)

# Graphics.

docs/images/phases-excerpt-1024.jpg: images/phases-excerpt-1024.jpg
	cp $< $@

all: docs/images/phases-excerpt-1024.jpg

docs/images/banner.png: images/banner.py python/sr_svg.py
	python images/banner.py > images/.tmp.svg \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg

all: docs/images/banner.png

#

docs/images/problems.png: images/problems.py python/sr_svg.py\
 python/shire_calendar.py
	python images/problems.py > images/.tmp.svg \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg

all: docs/images/problems.png

#

docs/images/phaseeqn.png: images/phaseeqn.tex
	tex images/phaseeqn.tex \
	&& (umask 022; dvipng -D 110 -T tight --gamma 2.0 -o $@ phaseeqn.dvi) \
	&& rm -f phaseeqn.dvi phaseeqn.log

all: docs/images/phaseeqn.png

#

SKYGLOBE_IMAGES := $(patsubst %, docs/images/skyglobe%.png, 1 2 3 4 F)
$(SKYGLOBE_IMAGES): %: images/skyglobe.py python/sr_svg.py
	python images/skyglobe.py $@ > images/.tmp.svg \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg && rm images/.tmp.svg

all: $(SKYGLOBE_IMAGES)

#

PHASE_IMAGES := $(patsubst %, docs/images/phases/%.png, $(shell seq 0 71))
$(PHASE_IMAGES): %: images/phase.py python/sr_svg.py
	python images/phase.py $@ > images/.tmp.svg \
	&& mkdir -p $$(dirname $@) \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg \
	&& rm images/.tmp.svg

all: $(PHASE_IMAGES)

images/test.svg: bin/test2
	bin/test2 > images/test.svg

#

.PHONY: test
test:
	python test/test-shire_calendar.py
