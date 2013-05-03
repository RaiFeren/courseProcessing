## @namespace cpr
# File full of helper functions
# @author Rai Feren, Beryl Egerter
# 
# Various helper functions for doign things with data


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
	time = grad - currYear
	if time = 0:
		return 3
	elif time = 1:
		return 2
	elif time = 2:
		return 1
	elif time = 3:
		return 0
	else:
		return -1
