from google.appengine.tools import bulkloader

class CourseLoader(bulkloader.Loader):
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
        bulkloader.Loader.__init__(self, 'Course', fields)

loaders = [CourseLoader]

