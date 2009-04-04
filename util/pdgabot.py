states = ["Alabama",
          "Alaska",
          "Arizona",
          "Arkansas",
          "California",
          "Colorado",
          "Connecticut",
          "Delaware",
          "Florida",
          "Georgia",
          "Hawaii",
          "Idaho",
          "Illinois",
          "Indiana",
          "Kansas",
          "Kentucky",
          "Louisiana",
          "Maine",
          "Maryland",
          "Massachusetts",
          "Michigan",
          "Minnesota",
          "Mississippi",
          "Missouri",
          "Montana",
          "Nebraska",
          "Nevada",
          "New%20Hampshire",
          "New%20Jersey",
          "New%20Mexico",
          "New%20York",
          "North%20Carolina",
          "North%20Dakota",
          "Ohio",
          "Oklahoma",
          "Oregon",
          "Pennsylvania",
          "Rhode%20Island",
          "South%20Carolina",
          "South%20Dakota",
          "Tennessee",
          "Texas",
          "Utah",
          "Vermont",
          "Virginia",
          "Washington",
          "West%20Virginia",
          "Wisconsin",
          "Wyoming",]

class PDGABot:
    """
    This class goes through each of the courses on the PDGA website
    and harvests bits of metadata about the course, storing it
    to a central data location
    """
    def harvestSite(self):
        import urllib
        import csv
        from xml.dom import minidom
        import Geohash
        csvWriter = csv.writer(open('/tmp/courseloc.csv', 'w'))
        baseUrl = 'http://referential-integrity.com/DiscGolfCourseGmap/xml/mapXml/'
        for state in states:
            url = baseUrl + state + '.xml'
            print "Importing " + state
            xmldoc = minidom.parseString(urllib.urlopen(url).read())
            courses = xmldoc.getElementsByTagName('course')
            for course in courses:
                courseName = course.attributes['name'].value
                numberHoles = int(course.attributes['numholes'].value)
                courseId = int(course.attributes['id'].value)
                latitude = float(course.attributes['lat'].value)
                longitude = float(course.attributes['lon'].value)
                csvWriter.writerow([latitude,
                                    longitude,
                                    courseName,
                                    numberHoles,
                                    courseId,])

if __name__ == '__main__':
    bot = PDGABot()
    bot.harvestSite()
