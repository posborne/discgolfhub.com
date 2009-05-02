import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from models import Course

FB_API_KEY = '05ef2c8b16b7e5d99da222965006275a'
FB_APP_SECRET = 'be0fdb491f54bf358109c1e0b0605b03'
FB_APP_ID = 45846472395

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
      query = db.Query(Course)
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
                              'id': courseLocation.courseId,
                              'city': courseLocation.city,
                              'state': courseLocation.state})
          
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
    
    query = db.Query(Course)
    query.filter('courseId >', (page - 1) * 500 - 1)
    query.filter('courseId <', page * 500)
    results = query.fetch(limit=1000);
    
    courses = []
    for courseLocation in results:
      courses.append({'id': courseLocation.courseId})
      template_values = {'courses': courses,}
      path = os.path.join(os.path.dirname(__file__), 'templates/courses_csv.html')
      self.response.out.write(template.render(path, template_values))
      
class CourseMap(webapp.RequestHandler):
  """
  Render the course locator page.
  """
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'templates/courselocations.html')
    self.response.out.write(template.render(path, None))
    
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
    
class RedirectHome(webapp.RequestHandler):
  def get(self):
    self.redirect("/home/")

class GetCoursePage(webapp.RequestHandler):
  """
  Get and redner the specified course page.  Course pages are
  requested in the form /course?id=#### with #### being the courses
  PDGA course id
  """
  def get(self):
    courseId = int(cgi.escape(self.request.get('id')))

    query = db.Query(Course)
    query.filter('courseId =', courseId)
    results = query.fetch(1)
    
    if len(results) < 1:
      template_values = {'courseId' : courseId}
      path = os.path.join(os.path.dirname(__file__), 'templates/coursenotfound.html')
      self.response.out.write(template.render(path, template_values))
    else:
      # There should just be one course
      course = results[0]
      
      query = db.Query(CourseReview)
      query.filter('courseId =', courseId)
      results = query.fetch(25)
      reviews = []
      for review in results:
          reviews.append({'fbuid': review.fbUID,
                          'rating': review.overallRating,
                          'review': review.reviewText })
      
      templatevals = {'courseName': course.courseName, 
                      'lat': course.latitude,
                      'lon': course.longitude,
                      'numholes': course.numberHoles,
                      'id': course.courseId,
                      'description': course.description,
                      'city': course.city,
                      'state': course.state,
                      'zip' : course.zip,
                      'teeType': course.teeType,
                      'basketType': course.basketType,
                      'holesLT300': course.holesLT300,
                      'holesBW300400': course.holesBW300400,
                      'holesGT400': course.holesGT400 
                      'reviews' : reviews }
      
      path = os.path.join(os.path.dirname(__file__), 'templates/coursepage.html')
      self.response.out.write(template.render(path, templatevals))

class AddCourseReview(webapp.RequestHandler):
    """
    Handle the adding of courses.  Before this is done we need to verify
    that the request is associated with a legitimate facebook session
    to avoid fraudelent entries.  We also do validation of the data
    """
    from lib.facebook import *
    def get(self):
        rating = int(cgi.escape(self.request.post("courseRating")))
        review = string(cgi.escape(self.request.post("review")))
        courseId = int(cgi.escape(self.request.post("courseId")))
        fb = Facebook(FB_API_KEY, FB_APP_SECRET)
        if not fb.validate_cookie_signature(self.request.cookies):
            self.response.out.write("NOT LOGGED IN")
        else:
            cr = CourseReview(courseID = courseId,
                              reviewText = review,
                              overallRating = rating,
                              fbUID = fb.uid);

# Routes for WSGI application
application = webapp.WSGIApplication([('/', RedirectHome),
                                      ('/home/', MainPage),
                                      ('/getpoints/', GPSCoords),
                                      ('/getcourses/', GetCourses),
                                      ('/coursemap/', CourseMap),
                                      ('/coursepage/', GetCoursePage),
                                      ('/addcoursereview/', AddCourseReview),],
                                     debug=True)

# We use main because GAE will optimize based on this
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

