
GRAPH_PATH = "ML/Graphs/"

import utilities as u

def show_difficulties_distribution(y):
	"""
		Shows how many text are of every difficulty

		Args:
			y:	list of difficulties
	"""
	num_a = 0
	num_b = 0
	num_c = 0

	for m_y in y:
		if m_y == "A":
			num_a += 1
		elif m_y == "B":
			num_b += 1
		elif m_y == "C":
			num_c += 1

	print "A:", num_a, "/ B:", num_b, "/ C:", num_c

def scatter_plot_from_lists(var1, var2, title="graph_temp", path = GRAPH_PATH, xlabel=None, ylabel=None):
	"""
		It saves a scatter plot from 2 lists

		Args:
			var1:	first list of values
			var2:	second list of values
			title:	title of the plot
			path:	where to store the plot
			xlabel:	label for the x axis
			ylabel:	label for the y axis
	"""

	import matplotlib.pyplot as plt
	plt.plot(var1, var2)
	
	if xlabel is not None:
		plt.xlabel(xlabel)
		
	if ylabel is not None:
		plt.ylabel(ylabel)
		
	plt.title(title)
	#plt.show()
	
	#export plot and clear it
	plt.savefig(path + title + ".png")
	plt.clf()

def scatter_plot(index1, index2):

	"""
		Given 2 index variables it will export a scatter_plot.
		
		It loads some information that uses the ML partition
		
		Args:
			index1:	index for the x values of the scatter_plot
			index2: index for the y values of the scatter_plot
	"""

	#get headers
	import process_text as pt
	headers = pt.get_metrics_header()
	
	#get info
	import text_batch_process as tbp
	matrix, tag = tbp.load_ML_variables()

	#change difficulty label to color tag
	for index, item in enumerate(tag):
		if item == 'A':
			tag[index] = 'g'
			
		elif item == 'B':
			tag[index] = 'b'
			
		elif item == 'C':
			tag[index] = 'r'
	
	#extract info
	import numpy as np
	aux = np.array(matrix)
	
	var1 = aux[:, index1]
	var2 = aux[:, index2]
	xlabel = headers[index1]
	ylabel = headers[index2]
	
	#plot
	import matplotlib.pyplot as plt
	plt.scatter(var1, var2, color=tag)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(xlabel + " vs " + ylabel)
	#plt.show()
	
	#export plot and clear it
	plt.savefig(GRAPH_PATH + str(index1) + " vs " + str(index2) + ".png")
	plt.clf()

def plot_all():
	"""
		Plot scatter plots of all the combinations of the current metrics
	"""

	timer = u.Timer()
	print "\nPlotting all the combinations"
	
	#delete existing png files
	u.delete_files(GRAPH_PATH, ".png")
	
	import process_text as pt
	
	#do all the possible combination
	for i in range(0, len(pt.get_metrics_header())):
	
		for j in range(0, len(pt.get_metrics_header())):
		
			if i != j:
				print "ploting", i, "vs", j
				scatter_plot(i, j)
	
	print "\nAll graphs created in", timer.get_time()
	
def get_correlation_matrix():
	"""
		It saves a csv with the correlation matrix of the variables used in ML
	"""

	path_ML = "ML/"
	input_doc = "all_data.csv"
	output_doc = "Correlation_matrix.csv"
	
	import pandas as pd
	
	df = u.csv_to_df(path_ML + input_doc)
	df = df[1:]
	
	u.df_to_csv(path_ML + output_doc, df.corr())
	
	
	
#If it is not imported, run that	
if __name__ == '__main__':
	plot_all()
	get_correlation_matrix()