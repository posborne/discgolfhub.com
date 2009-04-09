# This makefile provides an easy way to carry out some of the management
# tasks associated with the project

APPCFG = /home/osbpau/dev/python/google_appengine/appcfg.py
APPSVR = /home/osbpau/dev/python/google_appengine/dev_appserver.py

install:
	$(APPCFG) update --email=osbpau@gmail.com ./

appserver:
	$(APPSVR) --disable_static_caching ./

updatelogs:
	$(APPCFG) request_logs ./ logs.txt