import re

states = [
    "Alabama",
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
    "Wyoming",
]

class PDGABot:
    """
    This class goes through each of the courses on the PDGA website
    and harvests bits of metadata about the course, storing it
    to a central data location
    """
    def harvestCourseIds(self):
        import urllib
        import csv
        from xml.dom import minidom
        csvWriter = csv.writer(open('./courses.csv', 'w'))
        # Unfortunately referential-integrity tanked
        # baseUrl = 'http://referential-integrity.com/DiscGolfCourseGmap/xml/mapXml/'
        baseUrl = 'http://www.pdga.com/courses-by-state'
        coursesPerPage = 40
        courses = []
        for state in states:
            page = 0
            coursesOnPage = 1
            while coursesOnPage > 0:
                url = baseUrl + '?pageNum_Courses=' + str(page) + '&SearchState=' + state
                resultpage = urllib.urlopen(url).read()
                results = re.findall('[?]id=(\d+)', resultpage)
                for item in results:
                    courses.append(item)
                coursesOnPage = len(results)
                page += 1
            print 'Courses after ' + state + ': ' + str(len(courses))
        csvWriter.writerow(courses)

    def downloadCoursePages(self):
        import urllib
        import csv
        import os
        idreader = csv.reader(open('courses.csv'))
        for row in idreader: # there is just one
            row.sort()
            for id in row:
                if (not os.path.exists('coursepages/' + str(id) + '.htm')):
                    print "Downloading course " + str(id)
                    f = open('coursepages/' + str(id) + '.htm', 'w')
                    f.write(urllib.urlopen('http://www.pdga.com/course-details?id=' + str(id)).read())
                    f.close()

    def processPagesToCsv(self):
        import csv
        import os
        courses = []
        idreader = csv.reader(open('courses.csv'))
        for row in idreader:
            for id in row:
                if (os.path.exists('coursepages/' + str(id) + '.htm')):
                    courses.append(self.processPage('coursepages/' + str(id) + '.htm', id))
        
        csvWriter = csv.writer(open('coursedata.csv', 'w'))
        for course in courses:
            csvWriter.writerow([
                course['lat'],
                course['lon'],
                course['name'],
                course['id'],
                course['numholes'],
                course['established'],
                course['zip'],
                course['description'],
                course['state'],
                course['city'],
                course['basket_type'],
                course['teetype'],
                course['holesLT300'],
                course['holesBW300400'],
                course['holesGT400']])


    def processPage(self, filename, courseId):
        f = open(filename, 'r')
        text = f.read()
        f.close()
        course = {}

        latres = re.search('latitude=(-?\d+[.]\d+)', text)
        lonres = re.search('longitude=%20(-?\d+[.]\d+)', text)
        zipres = re.search('zipcode=(\d+)', text)
        yearres = re.search('<strong>Course Established:</strong>\s*(\d+)\s*', text)
        descriptionres = re.search('<strong>Description:</strong>\s*(.*)\s*</td>', text)
        nameres = re.search('<h2>\s*(.*)\s*</h2>', text)
        courselenres = re.search('<strong>Course Length:</strong>&nbsp;(\d+)', text)
        altcourselenres = re.search('<strong>Alternate Course Length:</strong>&nbsp;(\d+)', text)
        cityres = re.search('\s+(\w.+),\s+<a href="/courses-by-state[?]SearchState', text)
        stateres = re.search('/courses-by-state[?]SearchState=(.+)&order=city', text)
        holesres = re.search('<strong>Holes:</strong>&nbsp;(\d+)&nbsp;(.+)</td>', text)
        teetyperes = re.search('Type:</strong>&nbsp;(.*)</td>', text);
        lt300res = re.search('ALT="Less than 300 ft" HEIGHT=32 BORDER=0 ALIGN=ABSCENTER><br>\s+<b>(\d+)</b>', text)
        bw300400res = re.search('ALT="300-400 ft" HEIGHT=32 BORDER=0 ALIGN=ABSCENTER><br>\s+<b>(\d+)</b>', text)
        gt400res = re.search('ALT="More than 400 ft" HEIGHT=32 BORDER=0 ALIGN=ABSCENTER><br>\s+<b>(\d+)</b>', text)

        course['id'] = courseId
        if nameres is not None:
            course['name'] = nameres.group(1)
        else: course['name'] = ''

        if yearres is not None:
            course['established'] = yearres.group(1)
        else: course['established'] = -1

        if latres is not None and lonres is not None:
            course['lat'] = latres.group(1)
            course['lon'] = lonres.group(1)
        else: course['lat'] = course['lon'] = 0.0
        
        if zipres is not None:
            course['zip'] = zipres.group(1)
        else: course['zip'] = 0

        if descriptionres is not None:
            try:
                course['description'] = descriptionres.group(1).encode('utf-8', 'ignore')
            except:
                course['description'] = ''
        else: course['description'] = ''

        if cityres is not None:
            course['city'] = cityres.group(1)
        else: course['city'] = ''

        if stateres is not None:
            course['state'] = stateres.group(1)
        else: course['state'] = ''

        if courselenres is not None:
            course['length'] = courselenres.group(1)
        else: course['length'] = -1

        if altcourselenres is not None:
            course['alternate_length'] =  altcourselenres.group(1)
        else: course['alternate_length'] = -1

        if holesres is not None:
            course['numholes'] = holesres.group(1)
            course['basket_type'] = holesres.group(2)
        else:
            course['numholes'] = -1
            course['basket_type'] = ''

        if teetyperes is not None:
            course['teetype'] = teetyperes.group(1)
        else: course['teetype'] = ''

        if lt300res is not None:
            course['holesLT300'] = lt300res.group(1)
        else: course['holesLT300'] = -1

        if bw300400res is not None:
            course['holesBW300400'] = bw300400res.group(1)
        else: course['holesBW300400'] = -1

        if gt400res is not None:
            course['holesGT400'] = gt400res.group(1)
        else: course['holesGT400'] = -1

        return course
                         
if __name__ == '__main__':
    import sys
    flags = 'p'
    if len(sys.argv) > 1:
        flags = sys.argv[1]
    bot = PDGABot()
    if 'h' in flags:
        bot.harvestCourseIds()
    if 'd' in flags:
        bot.downloadCoursePages()
    if 'p' in flags:
        bot.processPagesToCsv()
