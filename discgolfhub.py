import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class CourseLocation(db.Model):
    latitude = db.FloatProperty()
    longitude = db.FloatProperty()
    courseName = db.StringProperty()
    numberHoles = db.IntegerProperty()
    courseId = db.IntegerProperty()

class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
    self.response.out.write(template.render(path, None))
    
class GPSCoords(webapp.RequestHandler):
    """
    We need a page for handling requests to get the gps coordinates
    of the different courses.  This prepares the data which we will
    send by to the requesting page as JSON.
    """
    def get(self):
        """
        Get is called when a request is triggered.
        """
        lat = float(cgi.escape(self.request.get('lat')))
        lon = float(cgi.escape(self.request.get('lon')))
        
        # Query for the GPS coordinates from the data store
        # We filter based on longitude first as we can only do 
        # inequalities on one property
        offset = 1.5
        query = db.Query(CourseLocation)
        query.filter('longitude >', lon - offset)
        query.filter('longitude <', lon + offset)
        
        results = query.fetch(limit=1000)
        coordinates = [] # coordinates are a list of (name, latitude, longitude) tuples
        for courseLocation in results:
            if courseLocation.latitude > (lat - offset) and courseLocation.latitude < (lat + offset):
                coordinates.append({'name': courseLocation.courseName, 
                                    'lat': courseLocation.latitude,
                                    'lon': courseLocation.longitude,
                                    'numholes': courseLocation.numberHoles,
                                    'id': courseLocation.courseId})
            
        # Have the template put the data into JSON format
        template_values = {'coordinates' : coordinates,}
        path = os.path.join(os.path.dirname(__file__), 'templates/coordinates_json.html')
        self.response.out.write(template.render(path, template_values))
        
class GetCourses(webapp.RequestHandler):
    """
    Get a CSV list of all the courses current in the database.
    """
    def get(self):
        page = int(cgi.escape(self.request.get('page')))

        query = db.Query(CourseLocation)
        query.filter('courseId >', (page - 1) * 500 - 1)
        query.filter('courseId <', page * 500)
        results = query.fetch(limit=1000);

        courses = []
        for courseLocation in results:
            courses.append({'id': courseLocation.courseId})

        template_values = {'courses': courses,}
        path = os.path.join(os.path.dirname(__file__), 'templates/courses_csv.html')
        self.response.out.write(template.render(path, template_values))


class XDReceiver(webapp.RequestHandler):
    """
    xd_receiver.htm is a required file for working with Facebook connect.
    We simply have the template do its thing
    """
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/connect/xd_receiver.htm')
        self.response.out.write(template.render(path, None))
        
class ConnectTest(webapp.RequestHandler):
    """
    Test the FB Connection
    """
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/connect/test.htm')
        self.response.out.write(template.render(path, None))

        
# Routes for WSGI application
application = webapp.WSGIApplication([('/', MainPage),
                                      ('/getpoints/', GPSCoords),
                                      ('/getcourses/', GetCourses)],
                                     debug=True)

# We use main because GAE will optimize based on this
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()


