# This makefile provides an easy way to carry out some of the management
# tasks associated with the project

APPCFG = /home/osbpau/dev/python/google_appengine/appcfg.py
APPSVR = /home/osbpau/dev/python/google_appengine/dev_appserver.py
BULKUPLOADER = /home/osbpau/dev/python/google_appengine/bulkloader.py

install:
1;1704;0c	$(APPCFG) update --email=osbpau@gmail.com ./

appserver:
	$(APPSVR) --disable_static_caching ./

appserverclearstore:	
	$(APPSVR) --disable_static_caching --clear_datastore ./	

appserverpub:
	$(APPSVR) --disable_static_caching --address=posborne.homelinux.com ./

updatelogs:
	$(APPCFG) request_logs ./ logs.txt

uploadlocal:
	$(BULKUPLOADER) --config_file=dataloader.py --filename=util/coursedata.csv --kind=Course --app_id=discgolfhub --url=http://localhost:8080/rapi


uploadserver:
	$(BULKUPLOADER) --config_file=dataloader.py --filename=util/coursedata.csv --kind=Course --app_id=discgolfhub --url=http://02-alpha.latest.discgolfhub.appspot.com/rapi

