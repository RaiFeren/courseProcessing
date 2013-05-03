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

	data = [(0,4,10,3), (0,3,5,7), (2,1,8,0)]

	theme.get_options()
	# make graph
	can = canvas.init("example.pdf")
	chart_object.set_defaults(area.T, size = (150, 120), y_range = (0, 15),
		x_coord = category_coord.T(data, 0))
	chart_object.set_defaults(bar_plot.T, data = data)

	bar_plot.fill_styles.reset()
	plot1=bar_plot.T(label="freshmen", cluster=(0,3))
	plot2=bar_plot.T(label="sophomores", hcol=2, cluster=(1,3))
	plot3=bar_plot.T(label="juniors", hcol=3, cluster=(2,3))
	#plot4=bar_plot.T(label="seniors", hcol=4, cluster=(3,4))

	ar = area.T(loc=(250,0),
            x_axis=axis.X(label="X label", format="/a-30{}%d"),
            y_axis=axis.Y(label="Y label", tic_interval=2))
	ar.add_plot(plot1, plot2, plot3)
	ar.draw()
	for x in (ar.x_pos(10) - 20, ar.x_pos(20)- 10, ar.x_pos(30) - 10):
		zap.zap_horizontally(can, line_style.default, fill_style.white,
    		x, ar.y_pos(65), x+16, ar.y_pos(65) + 4, 4, 4)
	can.close()
