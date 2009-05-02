from google.appengine.ext import db

class Course(db.Model):
    """
    A course has a number of different properties.  We will have
    indices on latitude, longitude, and courseId
    """
    latitude = db.FloatProperty()
    longitude = db.FloatProperty()
    courseName = db.StringProperty()
    numberHoles = db.IntegerProperty()
    courseId = db.IntegerProperty()
    yearEstablished = db.IntegerProperty()
    zip = db.IntegerProperty()
    description = db.TextProperty()
    state = db.StringProperty()
    city = db.StringProperty()
    basketType = db.StringProperty()
    teeType = db.StringProperty()
    holesLT300 = db.IntegerProperty()
    holesBW300400 = db.IntegerProperty()
    holesGT400 = db.IntegerProperty()

class CourseReview(db.Model):
    """
    Course reviews consist of review text and a rating tied to the
    poster (through facebook id) and course (through course id)
    """
    courseID = db.IntegerProperty()
    reviewText = db.TextProperty()
    overallRating = db.IntegerProperty()
    fbUID = db.IntegerProperty()
    
