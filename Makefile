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

# For each page to be produced in the ./html/ directory, create and
# include a rule listing the dates for which the page will want to
# display events.

INDEX_DATES := $(shell bin/index_dates)
INDEX_FILES := $(patsubst %, html/index-%.html, $(INDEX_DATES))
$(INDEX_FILES): pages/index.ptl python/sr_moon.py

ATOM_FILES := $(patsubst %, html/atom-%.xml, $(INDEX_DATES))
atom: $(ATOM_FILES)
$(ATOM_FILES): pages/atom.ptl

CAL_FILE := html/calendar.html
$(CAL_FILE): pages/calendar.ptl

FAQ_FILE := html/faq.html
$(FAQ_FILE): pages/faq.ptl

MOON_FILE := html/moon.html
$(MOON_FILE): pages/moon.ptl python/sr_moon.py data/moons

MOON_UPDATE_FILE := html/moon-update.html
$(MOON_UPDATE_FILE): pages/moon.ptl

ARCHIVE_MONTHS := $(shell PYTHONPATH=$(PYTHONPATH) bin/archive_months)
ARCHIVE_FILES := html/archive.html
ARCHIVE_FILES += $(patsubst %, html/archive-%/index.html, $(ARCHIVE_MONTHS))

PAGE_FILES := $(INDEX_FILES) $(CAL_FILE) $(ARCHIVE_FILES) $(FAQ_FILE) $(MOON_FILE) $(MOON_UPDATE_FILE)

$(PAGE_FILES) $(ATOM_FILES) $(ARCHIVE_FILES): python/sr_entries.py \
 data/entries python/sr_html.ptl
$(ARCHIVE_FILES): pages/archive.ptl python/sr_html.ptl python/sr_moon.py

#PAGE_RULES := $(patsubst %, .make/%, $(PAGES))

#$(INDEX_PAGES) $(PAGE_RULES): pages/index.ptl
#$(INDEX_PAGES): pages/index.ptl
#$(PAGE_RULES): .make/%: bin/page_rules
#	bin/page_rules $* $@

#include $(PAGE_RULES)

#$(PAGE_FILES): $(EVENT_FILES)

# Actual page composition.

$(PAGE_FILES): html/%.html: bin/page_compose python/shire_calendar.py \
 python/design.ptl python/sr_entries.py data/transforms.py data/tidy.conf
	$(PYTHON) bin/page_compose $* .page
	mkdir -p $$(dirname $@)
	cp .page $@
	chmod a+r $@

$(ATOM_FILES): html/%.xml: bin/page_compose
	$(PYTHON) bin/page_compose $* $@
	chmod a+r $@

all: $(PAGE_FILES) $(ATOM_FILES)

# Graphics.

html/images/phases-excerpt-1024.jpg: images/phases-excerpt-1024.jpg
	cp $< $@

all: html/images/phases-excerpt-1024.jpg

html/images/banner.png: images/banner.py python/sr_svg.py
	python images/banner.py > images/.tmp.svg \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg

all: html/images/banner.png

#

html/images/problems.png: images/problems.py python/sr_svg.py\
 python/shire_calendar.py
	python images/problems.py > images/.tmp.svg \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg

all: html/images/problems.png

#

html/images/phaseeqn.png: images/phaseeqn.tex
	tex images/phaseeqn.tex \
	&& (umask 022; dvipng -D 110 -T tight --gamma 2.0 -o $@ phaseeqn.dvi) \
	&& rm -f phaseeqn.dvi phaseeqn.log

all: html/images/phaseeqn.png

#

SKYGLOBE_IMAGES := $(patsubst %, html/images/skyglobe%.png, 1 2 3 4 F)
$(SKYGLOBE_IMAGES): %: images/skyglobe.py python/sr_svg.py
	python images/skyglobe.py $@ > images/.tmp.svg \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg

all: $(SKYGLOBE_IMAGES)

#

PHASE_IMAGES := $(patsubst %, html/images/phases/%.png, $(shell seq 0 71))
$(PHASE_IMAGES): %: images/phase.py python/sr_svg.py
	python images/phase.py $@ > images/.tmp.svg \
	&& mkdir -p $$(dirname $@) \
	&& umask 022 && inkscape -z -e $@ images/.tmp.svg

all: $(PHASE_IMAGES)

images/test.svg: bin/test2
	bin/test2 > images/test.svg

#

.PHONY: test
test:
	python test/test-shire_calendar.py
