## @namespace cpr
# Main Driver for Processing Course Data.
# @author Rai Feren, Beryl Egerter
# 
# This is the main driver for the course processor.
#
# Usage: `python cpr.py <data source file>`
import re
import os, sys, getopt
import csv

import makeGraph

class Student(object):
    def __init__(self, mdata, gradYear):
        self.id_ = id(self)
        self.college_ = mdata[0]
        self.major_ = mdata[1:]
        self.gradYear_ = gradYear
        self.classes = []

    def addClass(self, cid, ctag):
        self.classes.append( (cid, ctag) )


 
def parse(csvSrc):
    # sdata :: sid -> Student
    sdata = {}
    # cdata :: cid -> (Year, Sem) -> [sid]
    cdata = {}

    spec = None
    curStudent = None

    for line in csvSrc:
        if not spec:
            spec = True
            continue
        # Get data
        gradYear,major1,major2,cYear,cSem,cID,college,courseCount,un1,un2 \
            = line
        cTag = (cYear, cSem, college)
        # Handle Students
        if not curStudent:
            curStudent = Student(major1,gradYear)
        assert curStudent != None
        curStudent.addClass(cID, cTag)

        # Handle class data
        if not cID in cdata:
            cdata[cID] = {cTag: []}
        elif not cTag in cdata[cID]:
            cdata[cID][cTag] = []
        cdata[cID][cTag].append(curStudent.id_)

        # If its time to move onto a new student, do so.
        if courseCount != '':
            # Save the student
            if (len(curStudent.classes) != int(courseCount)):
                print "ERROR: Student's classes don't add up?!"
            sdata[curStudent.id_] = curStudent
            curStudent = None


    if curStudent:
        print "ERROR: Student left over?!"
    students = sdata
    return sdata, cdata

def calcNonMajors(studentData, courseData, selection):
    times = selection.keys()
    times.sort()
    for time in times:
        yearData = int(time[0])+1
        if time[1] == 'FA  ':
            yearData -= 0.5
        csMajors = 0
        nonMajors = 0
        for sid in selection[time]:
            if studentData[sid].major_ in ['CSI', 'CSM', 'MCB']:
                csMajors += 1
            else:
                nonMajors += 1
        yield(yearData, csMajors, nonMajors)


def calculateTests(studentData, courseData):

    try:
        selection = courseData['CSCI070  HM ']
    except KeyError, e:
        print courseData.keys()
        raise e
    results = [x for x in calcNonMajors(studentData, courseData, selection)]

    return (results, 
            {'charts':['CS Major', 'Non-CS Major'], 
             'x': 'Year', 'y':'Population', 'title':'Who takes CS 70'})

def main(srcFile):
    # Open the file.
    rawText = open(srcFile, 'r')
    if not rawText:
        print "Problem with the source file!"
        return -1
    # Parse it.
    textRead = csv.reader(rawText) 
    studentData, courseData = parse(textRead)

    # Run tests on the parsed data
    inp, inpL = calculateTests(studentData, courseData)

    # Render its results.
    makeGraph.drawBarGraph(inp, inpL, "results.pdf")
    return 0

def processArgs():
    try:
        # No argument flags, so give error if there is one!
        opts, args = getopt.getopt(sys.argv[1:],"")
        for arg in args:
            data = arg
    except Exception, e:
        raise e

    if data != None:
        return data
    else:
        return None


if __name__ == '__main__':
    src = processArgs()
    if src:
        main(src)
