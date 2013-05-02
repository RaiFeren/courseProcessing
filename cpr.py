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


class Student(object):
    def __init__(self, mdata, gradYear):
        self.id_ = id(self)
        self.college_ = mdata[0]
        self.major_ = mdata[1:]
        self.gradYear_ = gradYear
        self.classes = []

    def addClass(cid, yr, sem):
        self.classes.append( (cid, (yr, sem)) )
 
## Bottom lines will be removed in next commit!
   
# students :: sid -> Student
#students = {}
# classes :: cid -> (Year, Sem) -> [sid]
#classes = {}


def parse(csvSrc):
    # sdata :: sid -> Student
    sdata = {}
    # cdata :: cid -> (Year, Sem) -> [sid]
    cdata = {}


    spec = csvSrc.readline()    

    curStudent = None

    for line in csvSrc[1:]:
        if not curStudent:
            curStudent = Student(line[1],line[0])
        curStudent.addClass(line[5], (line[3], line[4]))
        
        if line[7] != '':
            # Save the student
            if (len(curStudent.classes) != line[7]):
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

    # Render its results.

    return 0

def processArgs():
    try:
        # No argument flags, so give error if there is one!
        opts, args = getopt.getopt(sys.argv[1:],"")
        for arg in args:
            data = arg
    if data:
        return data
    else:
        return None


if __name__ == '__main__':
    src = processArgs()
    if src:
        main(src)
