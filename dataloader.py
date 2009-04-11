from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search

class CourseLocationsLoader(bulkload.Loader):
    def __init__(self):
        # Let's tie this sucker into the db model
        fields = [('latitude', float),
                  ('longitude', float),
                  ('courseName', str),
                  ('numberHoles', int),
                  ('courseId', int),
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
        bulkload.Loader.__init__(self, 'CourseLocation', fields)
        
if __name__ == '__main__':
    bulkload.main(CourseLocationsLoader())
