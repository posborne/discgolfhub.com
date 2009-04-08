# This makefile provides an easy way to carry out some of the management
# tasks associated with the project

APPCFG = /home/osbpau/dev/python/google_appengine/appcfg.py

install:
	$(APPCFG) update ./
