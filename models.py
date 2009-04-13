from google.appengine.ext import db

class Course(db.Model):
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
