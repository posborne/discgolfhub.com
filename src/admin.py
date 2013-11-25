import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from models import Course

class ClearCourses(webapp.RequestHandler):
    def get(self):
        query = db.Query(Course)
        res = query.fetch(500)
        while len(res) > 0:
            db.delete(res)
            res = query.fetch(500)
        self.response.out.write("Complete")
            
# Routes for WSGI application
application = webapp.WSGIApplication([('/admin/clearcourses/', ClearCourses),],
                                     debug=True)

# We use main because GAE will optimize based on this
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

