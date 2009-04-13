from google.appengine.ext import db
# from google.appengine.ext import bulkload
import models

class CourseLoader(Loader):
    def __init__(self):
        # Let's tie this sucker into the db model
        fields = [('latitude', float),
                  ('longitude', float),
                  ('courseName', str),
                  ('courseId', int),
                  ('numberHoles', int),
                  ('yearEstablished', int),
                  ('zip', int),
                  ('description', str),
                  ('state', str),
                  ('city', str),
                  ('basketType', str),
                  ('teeType', str),
                  ('holesLT300', int),
                  ('holesBW300400', int),
                  ('holesGT400', int),]
        Loader.__init__(self, 'Course', fields)

#if __name__ == '__main__':
#    Loader.main(CourseLocationsLoader())

