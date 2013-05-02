## @namespace cpr
# Main Driver for Processing Course Data.
# @author Rai Feren, Beryl Egerter
# 
# This is the main driver for the course processor.
#
# Usage: `python cpr.py <data source file>`
import re
import os, sys, getopt

class Student(object):
    def __init__(self, mdata, gradYear):
        self.id_ = id(self)
        self.college_ = mdata[0]
        self.major_ = mdata[1:]
        self.gradYear_ = gradYear
        self.classes = []

    def addClass(cid, yr, sem):
        self.classes.append( (cid, (yr, sem)) )
    
# students :: id -> Student
students = {}
# classes :: id -> (Year, Sem) -> [Student]
classes = {}


def parse(rawText):
    return []

def main(srcFile):
    rawText = open(srcFile)
    if not rawText:
        print "Problem with the source file!"
        return -1

    # Open the file.
    # Parse it.
    parse(srcFile)
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
