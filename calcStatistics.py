## @namespace calcStatistics
# Calculates various statistics in a cool way.
# @author Rai Feren, Beryl Egerter

def calcNonMajors(studentData, courseData, selection):
    times = selection.keys()
    times.sort()
    for time in times:
        yearData = int(time[0])+1
        if time[1] == 'FA  ':
            yearData -= 0.5
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
        yearData = int(time[0])+1
        if time[1] == 'FA  ':
            yearData -= 0.5
        years = {'H': 0, 'S': 0, 'M': 0, 'Z': 0, 'P': 0}

        for sid in selection[time]:
            years[studentData[sid].college_] += 1

        yield(yearData, years['H'], years['S'],
              years['M'], years['Z'], years['P'])



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

