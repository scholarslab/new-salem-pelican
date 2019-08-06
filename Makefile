PY?=python3
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

SSH_HOST=corgi.lib.virginia.edu
SSH_HOST_NAME=corgi
SSH_PORT=22
SSH_TARGET_DIR=/websites/salem.lib.virginia.edu

GITHUB_PAGES_BRANCH=gh-pages

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           copy over old salem static content, regenerate site, copy over new static content'
	@echo '   make html-static                    only copy over new static content'
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          start/restart develop_server.sh    '
	@echo '   make stopserver                     stop local server                  '
	@echo '   make ssh_upload                     upload the web site via SSH        '
	@echo '   make rsync_upload                   upload the web site via rsync+ssh  '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

html:
	python lunrcorpus.py
	cat content/search/corpus.json | scripts/build-index > content/search/idx.json
	if test -d $(BASEDIR)/old-salem; then rsync -tHa --stats --delete $(BASEDIR)/old-salem/ $(OUTPUTDIR)/; fi
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
	if test -d $(BASEDIR)/static-salem; then cp -v -R $(BASEDIR)/static-salem/* $(OUTPUTDIR)/; fi
	if test -d $(BASEDIR)/static-salvrec; then cp -v -R $(BASEDIR)/static-salvrec/* $(OUTPUTDIR)/; fi
	if test -d $(BASEDIR)/static-uph1wit; then cp -v -R $(BASEDIR)/static-uph1wit/* $(OUTPUTDIR)/; fi

html-static:
	if test -d $(BASEDIR)/static-salem; then cp -v -R $(BASEDIR)/static-salem/* $(OUTPUTDIR)/; fi
	if test -d $(BASEDIR)/static-salvrec; then cp -v -R $(BASEDIR)/static-salvrec/* $(OUTPUTDIR)/; fi
	if test -d $(BASEDIR)/static-uph1wit; then cp -v -R $(BASEDIR)/static-uph1wit/* $(OUTPUTDIR)/; fi

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve:
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) -m pelican.server $(PORT)
else
	cd $(OUTPUTDIR) && $(PY) -m pelican.server
endif

serve-global:
ifdef SERVER
	cd $(OUTPUTDIR) && $(PY) -m pelican.server 80 $(SERVER)
else
	cd $(OUTPUTDIR) && $(PY) -m pelican.server 80 0.0.0.0
endif

devserver: html
ifdef PORT
	$(BASEDIR)/develop_server.sh restart $(PORT)
else
	$(BASEDIR)/develop_server.sh restart
endif

stopserver:
	$(BASEDIR)/develop_server.sh stop
	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'

publish:
	python lunrcorpus.py
	cat content/search/corpus.json | scripts/build-index > content/search/idx.json
	if test -d $(BASEDIR)/old-salem; then rsync -tHa --stats --delete $(BASEDIR)/old-salem/ $(OUTPUTDIR)/; fi
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)
	if test -d $(BASEDIR)/static-salem; then cp -v -R $(BASEDIR)/static-salem/* $(OUTPUTDIR)/; fi
	if test -d $(BASEDIR)/static-salvrec; then cp -v -R $(BASEDIR)/static-salvrec/* $(OUTPUTDIR)/; fi
	if test -d $(BASEDIR)/static-uph1wit; then cp -v -R $(BASEDIR)/static-uph1wit/* $(OUTPUTDIR)/; fi

ssh_upload: publish
	scp -P $(SSH_PORT) -r $(OUTPUTDIR)/* $(SSH_HOST):$(SSH_TARGET_DIR)

ssh_config_upload: publish
	scp -P $(SSH_PORT) -r $(OUTPUTDIR)/* $(SSH_HOST_NAME):$(SSH_TARGET_DIR)

rsync_upload: publish
	rsync -e "ssh -p $(SSH_PORT)" -P -rvzc --stats --delete $(OUTPUTDIR)/ $(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

rsync_config_upload: publish
	rsync -e "ssh -p $(SSH_PORT)" -P -rvzc --stats --delete $(OUTPUTDIR)/ $(SSH_HOST_NAME):$(SSH_TARGET_DIR) --cvs-exclude

github: publish
	ghp-import -m "Generate Pelican site" -b $(GITHUB_PAGES_BRANCH) $(OUTPUTDIR)
	git push origin $(GITHUB_PAGES_BRANCH)

.PHONY: html help clean regenerate serve serve-global devserver stopserver publish ssh_upload rsync_upload dropbox_upload ftp_upload s3_upload cf_upload github
