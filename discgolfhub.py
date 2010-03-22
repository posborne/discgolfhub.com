import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from models import Course
from models import CourseReview
from facebook import Facebook

BETA = True
if BETA:
    FB_API_KEY = 'ca48b6923a4819cd461499d22e9f1f83'
    FB_APP_SECRET = '6e8ef7efd6cbd9e2d9fb5899292d2f42'
    FB_APP_ID = 93004867073
    GMAPS_API_KEY = 'ABQIAAAA4J1xeUoGXO89TjdkJmYHURRP7-MGB6iNRSSeiUtdfHP8TsV3ZBRCpa9fNzG5UgXgeKQ4xMljQKOd6g'
else: # RELEASE VERSION
    FB_API_KEY = '05ef2c8b16b7e5d99da222965006275a'
    FB_APP_SECRET = 'be0fdb491f54bf358109c1e0b0605b03'
    FB_APP_ID = 45846472395
    GMAPS_API_KEY = 'ABQIAAAA4J1xeUoGXO89TjdkJmYHURRP7-MGB6iNRSSeiUtdfHP8TsV3ZBRCpa9fNzG5UgXgeKQ4xMljQKOd6g'

class FacebookRequestHandler(webapp.RequestHandler):

    def __init__(self):
        webapp.RequestHandler.__init__(self)

    def get_facebook(self):
        fb = Facebook(FB_API_KEY, FB_APP_SECRET)
        if fb.check_session(self.request):
            return fb
        else:
            return None

class MainPage(FacebookRequestHandler):
    """
    Render the homepage.
    """
    def get(self):
        query = db.Query(CourseReview)
        query.order("-ratingTimestamp")
        results = query.fetch(3)
        
        # cut down the review text to 140 characters
        for review in results:
            if (len(review.reviewText) > 143):
                review.reviewText = review.reviewText[:140] + "..."
          
            # grab the course name for each course
            courseQuery = db.Query(Course)
            courseQuery.filter("courseId =", review.courseID)
            result = courseQuery.fetch(1)[0]
            review.courseName = result.courseName
    
        template_values = {'recent_reviews': results, 
                           'facebook': self.get_facebook()}
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, template_values))
    
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
        template_values = {'coordinates' : coordinates, }
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
        results = query.fetch(limit=1000)
        
        courses = []
        for courseLocation in results:
            courses.append({'id': courseLocation.courseId})
            template_values = {'courses': courses, }
            path = os.path.join(os.path.dirname(__file__), 'templates/courses_csv.html')
            self.response.out.write(template.render(path, template_values))
      
class CourseMap(FacebookRequestHandler):
    """
    Render the course locator page.
    """
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/courselocations.html')
        template_vals = {'gmaps_api_key': GMAPS_API_KEY, 'facebook': self.get_facebook() }
        self.response.out.write(template.render(path, template_vals))
    
class XDReceiver(FacebookRequestHandler):
    """
    xd_receiver.htm is a required file for working with Facebook connect.
    We simply have the template do its thing
    """
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/connect/xd_receiver.htm')
        self.response.out.write(template.render(path, None))
    
class RedirectHome(FacebookRequestHandler):
    def get(self):
        self.redirect("/home/")

class GetCoursePage(FacebookRequestHandler):
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
            reviewquery = CourseReview.all().filter('courseID =', int(courseId))
            #reviewquery.order('-ratingTimestamp')
            reviews = reviewquery.fetch(25)
            
            courseRating = 0
            for review in reviews:
                courseRating += float(review.overallRating) / len(reviews)
                review.reviewText = review.reviewText.replace('\n', '<br />')
                 
            templatevals = {'courseRating': courseRating,
                            'courseName': course.courseName,
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
                            'holesGT400': course.holesGT400,
                            'reviews' : reviews ,
                            'gmaps_api_key': GMAPS_API_KEY,
                            'facebook': self.get_facebook() }
            path = os.path.join(os.path.dirname(__file__), 'templates/coursepage.html')
            self.response.out.write(template.render(path, templatevals))

class AddCourseReview(FacebookRequestHandler):
    """
    Handle the adding of courses.  Before this is done we need to verify
    that the request is associated with a legitimate facebook session
    to avoid fraudelent entries.  We also do validation of the data
    """
    def post(self):
        rating = int(cgi.escape(self.request.get("rating_select")))
        review = str(cgi.escape(self.request.get("reviewtext")))
        courseId = int(cgi.escape(self.request.get("courseId")))
        fb = Facebook(FB_API_KEY, FB_APP_SECRET)
        if fb.check_session(self.request):
            courseQuery = db.Query(Course)
            courseQuery.filter('courseId =', courseId)
            cr = CourseReview(courseID=courseId,
                              reviewText=review,
                              overallRating=rating,
                              fbUID=long(fb.uid))
            cr.put()
        self.redirect('/coursepage/?id=' + str(courseId))

class About(FacebookRequestHandler):
    def get(self):
        self.response.out.write("Coming Soon...")
        
class Equipment(FacebookRequestHandler):
    def get(self):
        self.response.out.write("Coming Soon...")

class Search(FacebookRequestHandler):
    def get(self):
        query_text = cgi.escape(self.request.get("query"))
        q = Course.all().search(query_text).fetch(50)
        courses = []
        for course in q:
            coursevals = {'courseName': course.courseName,
                          'lat': course.latitude,
                          'lon': course.longitude,
                          'numholes': course.numberHoles,
                          'id': course.courseId,
                          'description': course.description.replace('\n', '<br />'),
                          'city': course.city,
                          'state': course.state,
                          'zip' : course.zip,
                          'teeType': course.teeType,
                          'basketType': course.basketType,
                          'holesLT300': course.holesLT300,
                          'holesBW300400': course.holesBW300400,
                          'holesGT400': course.holesGT400 }
            courses.append(coursevals)

        template_vals = {'courses': courses,
                         'query_text': query_text,
                         'gmaps_api_key': GMAPS_API_KEY,
                         'facebook': self.get_facebook() }
        path = os.path.join(os.path.dirname(__file__), 'templates/searchpage.html')
        self.response.out.write(template.render(path, template_vals))

# Routes for WSGI application
application = webapp.WSGIApplication([('/', RedirectHome),
                                      ('/home/', MainPage),
                                      ('/getpoints/', GPSCoords),
                                      ('/getcourses/', GetCourses),
                                      ('/coursemap/', CourseMap),
                                      ('/coursepage/', GetCoursePage),
                                      ('/addcoursereview/', AddCourseReview),
                                      ('/about/', About),
                                      ('/equipment/', Equipment),
                                      ('/search/', Search), ],
                                     debug=True)

# We use main because GAE will optimize based on this
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

