## @namespace cpr
# File full of helper functions
# @author Rai Feren, Beryl Egerter
#
# Various helper functions for doign things with data
import re

def getTimes():
	x = range(2002,2014)
	y = []

def getClassYear(grad, currYear):
	""" given a graduation year, calculates if the student was a
		-1: not enrolled,
		0: freshman
		1: sophomore
		2: junior
		3: senior
		during currYear """
	time = int(grad) - int(currYear)
	if time == 0:
		return 3
	elif time == 1:
		return 2
	elif time == 2:
		return 1
	elif time == 3:
		return 0
	else:
		return -1

def countClass(classYear,students, ids, currYear):
	count = [1 for i in ids if getClassYear(students[i].gradYear_, classYear) == currYear]
	return sum(count)

def getStudentsByYear(students, classes, course_id):
	cs = classes[course_id].keys()
	x = [(int(i[0]), classes[course_id][i]) for i in cs]
	return x

def getClassifiedStudentsByYear(students, classes, course_id):
	base = getStudentsByYear(students, classes, course_id)
	axes = [yr for (yr,x) in base]
	populations = [[countClass(i,students,x,yr) for i in range(4)] for (yr,x) in base]
	return (axes, populations)

def getKeys(courses, classId, lab):
	return [i for i in courses.keys() if (re.search(classId, i) and \
        (not re.search("L", i)) == (not lab))]

def numSemester(sem):
	if sem == "FA  ":
		return 0.5
	else:
		return 0

def collapse(x):
	results = {}
	for i in x:
		for y,s in i:
			if y in results.keys():
				results[y] += s
			else:
				results[y] = s
	#retList = [(y,results[y]) for y in results.keys()]
	#retList.sort()
	return results

def get105data(students, courses):

    # get all data into a dictionary where years key to student lists
    cids = getKeys(courses, "105", False)
    x = [[(int(i[0])+numSemester(i[1]), courses[cid][i]) \
    for i in courses[cid].keys()] for cid in cids ]
    x = collapse(x)
    # change the students list to a count of frosh/soph/jun/sen
    counts = {}
    for i in x.keys():
        counts[i] = {0:0, 1:0, 2:0, 3:0}

    for y in x.keys():
        st = x[y]
        for s in st:
            t = getClassYear(students[s].gradYear_, y)
            print t
            print counts[y][t]
            counts[y][t]+= 1

    for y in x.keys():
        print counts[i]

	return x
