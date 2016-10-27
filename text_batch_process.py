TEXT_PATH = "Texts/"
ML_PATH = "ML/"
#text_extension = ".txt"

import utilities as u

# Those are the names of the 2 objects that will be used for the ML part
x_ML_name = "x" # X is a matrix of features
y_ML_name = "y" # Y a list of tags

csv_name = "all_data.csv"

def get_difficulty(text):
	"""
		It takes a text that contains the difficulty tag and returns it 
		
		Example:
			A1_cine2 --> A1
		
		Args:
			text:	name of the document 
			
		Returns:
			Difficulty tag, it should be like A1, A2, B1, C2 or A, B, C
	"""

	#tag = text[:2]	#If difficulty is taged like A1, A2, B1, B2, C1, C2
	tag = text[:1]	#If difficulty is taged like A, B, C
	
	return tag
			
def store_results(x, y, file_names, change_decimal_separator=True):

	"""
		Function that store all the variables needed for the ML part.
		
		It saves the metrics (x) and the difficult labels (y) in pickle objects.
		It also stores a CSV with all the information.
	"""
	
	#first store x, y as pickle objects
	u.save_pickle(x, x_ML_name, path = ML_PATH)
	u.save_pickle(y, y_ML_name, path = ML_PATH)
	
	import process_text as pt
	import numpy as np
	
	header = ["File"] + pt.get_metrics_header() + ["Difficulty"]
	matrix = np.c_[file_names, x, y]
	
	#Then save a CSV with all the data
	u.save_to_csv(csv_name, ML_PATH, matrix, header)
	
	#Locally a decimal is write like 3,14 not 3.14
	#By default it changes that
	if change_decimal_separator:
		u.change_decimal_separator(csv_name, ML_PATH, [".txt"])

def process_all_texts():
	"""
		Reads all the texts presents in the folders inside TEXT_PATH.
		
		It retrives some metrics that will be stored and used in the ML part
		
		Returns:
			x:	Matrix of metrics with size n*m, where =>
						n = num of texts processed
						m = num of different characteristics
			y:	Array with difficulty tags
	"""
	
	#used to calculate how the preprocessing part lasts
	timer = u.Timer()
	print "Starting to process all the texts"

	import os
	import process_text as pt

	# For the ML part, it will try to solve something like a*x = y
	x = []
	y = []
	file_names = []

	#Explore every folder inside TEXT_PATH
	for folder in os.listdir(os.getcwd() + "/" + TEXT_PATH):

		#check that it is really a folder, not a file
		if "." not in folder:
		
			#Get every document
			documents = os.listdir(os.getcwd() + "/" + TEXT_PATH + folder)
			actual = 1
			for doc_name in documents:

				print "\n\nProcessing text", actual, "/", len(documents), "inside", folder
				actual += 1

				x.append(pt.process_text_from_document(doc_name, TEXT_PATH + folder + "/"))
				y.append(get_difficulty(doc_name))
				
				file_names.append(folder + "/"+ doc_name)
			
	print len(y), "texts processed in", timer.get_time(), "seconds"
	
	store_results(x, y, file_names)
	
	return x, y
		
def load_ML_variables(process = False):
	"""
		It retrives x, y objects to be used in the ML part. It will try to load from pickle objects and
		if it fails it will calculate them.
		
		It is posible to force the machine to calculate x and y instead of reading from pickle objects
		
		Args:
			process:	if true, it will process all the texts instead of loading x and y
	"""

	#if asked by user, process anyway
	if process:
		x, y = process_all_texts()
		
	#if not, try to load previously processed data
	else:
		try:
			x = u.load_pickle(x_ML_name, path = ML_PATH)
			y = u.load_pickle(y_ML_name, path = ML_PATH)
			
		except IOError:
		
			print "Pickle objects not found, starting batch process"
			x, y = process_all_texts()
	
	return x, y

	
	
#If it is not imported, run that	
if __name__ == '__main__':
	process_all_texts()