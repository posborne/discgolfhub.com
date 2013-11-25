import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class XDReceiver(webapp.RequestHandler):
    """
    xd_receiver.htm is a required file for working with Facebook connect.
    We simply have the template do its thing
    """
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'xd_receiver.htm')
        self.response.out.write(template.render(path, None))
        
# Routes for WSGI application
application = webapp.WSGIApplication([('/xd_receiver.htm', XDReceiver),],
                                     debug=True)

# We use main because GAE will optimize based on this
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()


