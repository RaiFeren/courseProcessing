## @namespace cpr
# Graphmaker
# @author Rai Feren, Beryl Egerter
# 
# This is where graphing occurs
# This file depends on pychart.
# We use pychart because it was the first thing that installed without errors
# on Beryl's computer.
#
# You can find pychart at: http://home.gna.org/pychart/

from pychart import *

def exampleGraph(students, classes):
	# here you would pull data from dictionaries but I'm just going to make stuff up
	# instead

	data = [(2008,0,3,6,3),(2009,0,4,10,2), (2010,1,3,7,4), (2011,1,4,5,4)]

	theme.get_options()

	# draw graph
	can = canvas.init("example.pdf")
	chart_object.set_defaults(area.T, 
		size = (150, 120), # size of graph
		y_range = (0, 15), # bounds on y axis
		x_coord = category_coord.T(data, 0)) #where the x coord info comes from

	chart_object.set_defaults(bar_plot.T, data = data) #set it as a bar plot, give data

	# reset in between drawing things?
	bar_plot.fill_styles.reset()

	# to make legend
	# for clusters, first number is order of occurence, second 
	# number is how many columns there are
	plot1=bar_plot.T(label="freshmen", cluster=(0,4))
	plot2=bar_plot.T(label="sophomores", hcol=2, cluster=(1,4))
	plot3=bar_plot.T(label="juniors", hcol=3, cluster=(2,4))
	plot4=bar_plot.T(label="seniors", hcol=4, cluster=(3,4))

	# draw legend
	ar = area.T(loc=(250,0),
            x_axis=axis.X(label="X label", format="/a-30{}%d"),
            y_axis=axis.Y(label="Y label", tic_interval=2))
	ar.add_plot(plot1, plot2, plot3, plot4)
	ar.draw()

	# clean up after ourselves
	can.close()
