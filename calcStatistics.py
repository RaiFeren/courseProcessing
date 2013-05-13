## @namespace calcStatistics
# Calculates various statistics in a cool way.
# @author Rai Feren, Beryl Egerter
import re

import re

def calcNonMajors(studentData, courseData, selection):
    times = selection.keys()
    times.sort()
    for time in times:
        yearData = int(time[0])#+1
        if time[1] == 'FA  ':
            yearData += 0.5
        csMajors = 0
        nonMajors = 0
        undeclared = 0
        for sid in selection[time]:
            if studentData[sid].major_ in ['CSI', 'CSM', 'MCB']:
                csMajors += 1
            elif studentData[sid].major_ in ['UND']:
                undeclared += 1
            else:
                nonMajors += 1
        yield(yearData, csMajors, nonMajors, undeclared)


def calcCampus(studentData, courseData, selection):
    times = selection.keys()
    times.sort()
    for time in times:
        yearData = int(time[0])#+1
        if time[1] == 'FA  ':
            yearData += 0.5
        years = {'H': 0, 'S': 0, 'M': 0, 'Z': 0, 'P': 0}

        for sid in selection[time]:
            years[studentData[sid].college_] += 1

        yield(yearData, years['H'], years['S'],
              years['M'], years['Z'], years['P'])

def basicSum(studentData, courseData, selection):
    times = selection.keys()
    times.sort()
    for time in times:
        yearData = int(time[0])#+1
        if time[1] == 'FA  ':
            yearData += 0.5
        yield(yearData, len(selection[time]))



def calculateCS70Tests(studentData, courseData):
    selection = courseData['CSCI070  HM ']
    results = [x for x in calcNonMajors(studentData, courseData, selection)]

    return (results,
            {'charts':['CS Major', 'Non-CS Major', 'Undeclared'],
             'x': 'Year', 'y':'Population', 'title': 'CS 70 by Rough Major',
             'size': (350, 220)})

def calcCS5Tests(studentData, courseData):
    selection = courseData['CSCI005  HM ']
    results = [x for x in calcCampus(studentData, courseData, selection)]

    return (results,
            {'charts':['HMC', 'Scripps', 'CMC', 'Pitzer', 'Pomona'],
             'x': 'Year', 'y':'Population', 'title': 'CS 5 by Campus',
             'size': (350, 220)})

def noMuddCS5Tests(studentData, courseData):
    selection = courseData['CSCI005  HM ']
    results = [(x[0],x[2], x[3], x[4], x[5])
               for x in calcCampus(studentData, courseData, selection)]

    return (results,
            {'charts':['Scripps', 'CMC', 'Pitzer', 'Pomona'],
             'x': 'Year', 'y':'Population', 'title': 'CS 5 without Mudd',
             'size': (350, 220)})

def calc5vs42(studentData, courseData):
    selection5 = courseData['CSCI005  HM ']
    selection42 = courseData['CSCI042  HM ']

    resultsVS = [(x[0], x[1], y[1])
                 for x in results5 for y in results42 if x[0] == y[0]]

    return (resultsVS,
            {'charts':['CS 5', 'CS 42'],
             'x': 'Year', 'y':'Population', 'title': 'CS 5 vs CS 42',
             'size': (350, 220)})

            

# Distance between CS70 and Algs
def distToAlgs(studentData, courseData):
    classRE = re.compile('''^CSCI(\d\d\d)(..)(\w\w)''')
    results = {}
    for sid in studentData.values():
        sem70 = None
        sem140 = None
        distance = None
        for class_ in sid.classes:
            classMatch = re.match(classRE, class_[0])
            if not classMatch:
                continue
            time = int(class_[1][0])+1
            if class_[1][1] == 'FA  ':
                time -= 0.5
            if classMatch.group(1) == '070':            
                sem70 = time
            elif classMatch.group(1) == '140':
                sem140 = time
        if sem70 and sem140:
            distance = 2*(sem140-sem70) # Get num semesters passed.
            if distance < 0:
                print 'This person is negative?!', sid
            if not sid.gradYear_ in results:
                results[sid.gradYear_] = []
            results[sid.gradYear_].append(distance)
    print results

    return None, None

# Plot % of current CS Class taking each CS Course.
def percentCourse(studentData, courseData):
    return None, None


def test(courseData):
    
    parsedKeys = [re.match('''^CSCI(\d\d\d)(..)(\w\w)''', x) 
                  for x in courseData.keys()]
    transformed = [(x.group(1), x.group(2), x.group(3)) 
                   for x in parsedKeys if x]
    print transformed


def calc105Population(studentData, courseData):
    # get all data into a dictionary where years key to student lists
    cids = getKeys(courseData, "105", False)
    x = [[(int(i[0])+numSemester(i[1]), courseData[cid][i]) \
    for i in courseData[cid].keys()] for cid in cids ]
    x = collapse(x)
    # change the students list to a count of frosh/soph/jun/sen
    counts = {}
    for i in x.keys():
        counts[i] = [0,0,0,0]
        for s in x[i]:
            t = getClassYear(studentData[s].gradYear_, i)
            # print i, t
            #print "year: " + str(i) + " gradYear: " + \
            #    str(studentData[s].gradYear_) + " calcYear: " + str(t)
            if t == -1:
                print "-1 for year " + str(i) + " " + studentData[s].__repr__()
            elif studentData[s].college_ == "H":
                counts[i][t] = counts[i][t] + 1
            else:
                print studentData[s].college_
    results = [(yr, counts[yr][0], counts[yr][1], counts[yr][2], \
                counts[yr][3]) for yr in counts.keys()]
    results.sort()

    return (results,
            {'charts':['Freshmen', 'Sophomores', 'Juniors', 'Seniors'],
             'x': 'Year', 'y': 'Population',
             'title': 'Population of CS105 (Mudd Students Only)',
             'size': (500, 220)})


def calcPopbyClass(studentData, courseData, courseNumStr):
    # get all data into a dictionary where years key to student lists
    cids = getKeys(courseData, courseNumStr, False)
    print "CourseIds found: ", cids
    x = [[(int(i[0])+numSemester(i[1]), courseData[cid][i]) \
    for i in courseData[cid].keys()] for cid in cids ]
    x = collapse(x)
    # change the students list to a count of frosh/soph/jun/sen
    counts = {}
    for i in x.keys():
        counts[i] = [0,0,0,0]
        for s in x[i]:
            t = getClassYear(studentData[s].gradYear_, i)
            # print i, t
            #print "year: " + str(i) + " gradYear: " + \
            #    str(studentData[s].gradYear_) + " calcYear: " + str(t)
            if t == -1:
                print "-1 for year " + str(i) + " " + studentData[s].__repr__()
            elif studentData[s].college_ == "H":
                counts[i][t] = counts[i][t] + 1
            else:
                print studentData[s].college_
    results = [(yr, counts[yr][0], counts[yr][1], counts[yr][2], \
                counts[yr][3]) for yr in counts.keys()]
    results.sort()

    return (results,
            {'charts':['Freshmen', 'Sophomores', 'Juniors', 'Seniors'],
             'x': 'Course Year', 'y': 'Population',
             'title': 'Population of '+courseNumStr+' (Mudd Students Only)',
             'size': (500, 220)})

def calcPopbyGrad(studentData, courseData, courseNumStr):
    cids = getKeys(courseData, courseNumStr, False)
    print "CourseIds found: ", cids
    x = [[(int(i[0])+numSemester(i[1]), courseData[cid][i]) \
    for i in courseData[cid].keys()] for cid in cids ]
    x = collapse(x)

    # counts is class year: [num semester taken (8)]
    counts = {}
    for i in x.keys():
        for sid in x[i]:
            gradYear = studentData[sid].gradYear_
            if not gradYear in counts.keys():
                counts[gradYear] = [0,0,0,0]
            yearNum = getClassYear(int(gradYear), i)
            counts[gradYear][yearNum] = counts[gradYear][yearNum] + 1
    results = [(int(yr), counts[yr][0], counts[yr][1], counts[yr][2],
                counts[yr][3]) for yr in counts.keys()]
    results.sort()

    return (results,
        {'charts':['Freshman Year', 'Sophomore Year', 'Junior Year', 'Senior Year'],
             'x': 'Graduation Year', 'y': 'Population',
             'title': 'Population of '+courseNumStr+' by Grad Year (Mudd Students Only)',
             'size': (500, 220)}
        )



## Gets the keys for all classes with a certain identifier.
# @param lab Boolean. Whether to return the labs for the
# course or the actual classes
def getKeys(courses, classId, lab):
    return [i for i in courses.keys() if (re.search(classId, i) and \
        (not re.search("L", i)) == (not lab))]


## collapses a list of [ [(year, [students] ), ... ], ... ] to {year:[students]}
def collapse(x):
    results = {}
    for i in x:
        for y,s in i:
            if y in results.keys():
                results[y] += s
            else:
                results[y] = s
    return results

def numSemester(sem):
    if sem == "FA  ":
        return 0.5
    else:
        return 0

# todo: this is probably wrong, fix it!
def getClassYear(grad, currYear):
    """ given a graduation year, calculates if the student was a
        -1: not enrolled,
        0: freshman
        1: sophomore
        2: junior
        3: senior
        during currYear """
    time = int(grad) - currYear
    if time < 1 and time >= 0:
        return 3
    elif time < 2 and time >= 0:
        return 2
    elif time < 3 and time >= 0:
        return 1
    elif time < 4 and time >= 0:
        return 0
    else:
        return -1
