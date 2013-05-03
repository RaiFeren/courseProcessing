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
import calcStatistics

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
    inp, inpL = calcStatistics.calculateCS70Tests(studentData, courseData)
    t1, t2 = calcStatistics.calcCS5Tests(studentData, courseData)
    t3, t4 = calcStatistics.noMuddCS5Tests(studentData, courseData)
    c5v42p, c5v42l = calcStatistics.calc5vs42(studentData, courseData)

    # Render its results.
    makeGraph.drawBarGraph(inp, inpL, "cs70Results.pdf")
    makeGraph.drawBarGraph(t1, t2, "cs5Results.pdf")
    makeGraph.drawBarGraph(t3, t4, "cs5nmResults.pdf")
    makeGraph.drawBarGraph(c5v42p, c5v42l, "cs5v42Results.pdf")

    

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
