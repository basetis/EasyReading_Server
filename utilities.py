#########################################################################################################
# 							general python utilities													#
#########################################################################################################
def divide_list_per_scalar(list, scalar):
	"""
		It divide each element in a list by some scalar number
		
		Args:
			list:	list of elements to be divided
			scalar:	dividend of every element of the list
			
		Returns:
			list with each element divided
	"""
	return	[x / (1.0*scalar) for x in list]

#########################################################################################################
# 							OS utilities																#
#########################################################################################################

def get_full_URI(name, extension, path=None):
	"""
		Check if the name of the document includes its extension, and if not, it adds it
		
		Then check if the path exists and if not, it creates it.
		
		Args:
			path_name:	name of the path to be checked
			name:		name of the document
			extension:	extension that should have the document
			
		Returns:
			name with it extesion and path like "Taggers/unigram.tagger"
	"""

	if extension is not None:
	
		#Check if extension has "."
		if extension[:1] != ".":
			extension = "." + extension
		
		#If file name shorter than extension, add it 
		if len(name) <= len(extension):
			name += extension
			
		#Check if it ends with the extension
		else:
			if name[-len(extension):] != extension:
				name += extension
		
	if path is not None:
		import os
		
		#if necessary creates the path
		if not os.path.exists(path):
			os.makedirs(path)
			
		return path + name
	
	else:
		return name
		
def delete_files(path, extension, check_sub_directories=False):

	"""
		It delete all the existing files in a path with the given extension
		
		Args:
			path:					where to look
			extension:				extension of the files that will be deleted
			check_sub_directories:	if true all subfolders will be inspected
	"""
	
	#info: http://stackoverflow.com/questions/7833715/python-deleting-certain-file-extensions
	import os
	
	for root, dirs, files in os.walk(path):
	
		#Only check the main folder except if specified by check_sub_directories
		if root == path or check_sub_directories:
		
			for currentFile in files:
				
				if currentFile.lower().endswith(extension):
					os.remove(os.path.join(root, currentFile))
					
def save_to_csv(doc_name, path, matrix, header=None):

	"""
		It saves some matrix with its header in a csv file
		
		Args:
			doc_name:	name of the csv to be saved
			path:		where to store the csv
			matrix:		main info of the csv
			header:		header of the csv
	"""
	
	import csv
	
	with open(path + doc_name, 'w') as f:
		writer = csv.writer(f, delimiter=";", lineterminator='\n')
		
		if header is not None:
			writer.writerow(header)
		
		writer.writerows(matrix)
		
def change_decimal_separator(doc_name, path, exceptions=None):

	"""
		It replaces all the "." in a csv for "," since decimal separator in europe is different than USA
		
		It also allows to have some exceptions
		
		Args:
			doc_name:	name of the csv to be processed
			path:		where it is the csv
			exceptions:	list of exceptions like [".txt", ".xlsx"]
	"""

	with open(path + doc_name, 'r') as f:
		filedata = f.read()

	filedata = filedata.replace('.', ',')
	
	if exceptions is not None:
		for excep in exceptions:
			filedata = filedata.replace(excep.replace('.', ','), excep)
	
	with open(path + doc_name, 'w+') as f:
		f.write(filedata)
		
#########################################################################################################
# 							pickle utilities															#
#########################################################################################################

PICKLE_EXTENSION = ".pkl"
	
def load_pickle(name, extension=PICKLE_EXTENSION, path=None):
	"""
		Gets a pickle object previously stored
		
		Args:
			name:	name of the pickle, it is not necessary to put the extension
			
		Returns:
			pickle object read
	"""
	
	#print "Loading", get_full_URI(name, extension, path)
	
	from cPickle import load
	
	uri = get_full_URI(name, extension, path)
	
	#read the pickle
	with open(uri, 'rb') as f:
		return load(f)
		
def save_pickle(object, name, extension=PICKLE_EXTENSION, path=None):
	"""
		Store an object into a pickle
		
		Args:
			object: object to be stored as a pickle
			name:	name of the pickle, it is not necessary to put the extension
	"""
	
	from cPickle import dump
	
	uri = get_full_URI(name, extension, path)
	
	#save the pickle
	with open(uri, 'wb') as f:
		dump(object, f, -1)

#########################################################################################################
# 							time utilities																#
#########################################################################################################
	
def fancy_string_time_from_seconds(seconds):
	"""
		It converts a time in seconds into a string that is beautiful to read
		
		Args:
			seconds:	time in seconds
			
		Returns:
			a fancy string like 1h 21m 42s
	"""
	
	#extract hours and minutes
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	
	#only print what it is not 0
	if h > 0:
		return "%dh %dm %02ds" % (h, m, s)
	else:
		if m >0 :
			return "%dm %02ds" % (m, s)
		else:
			return	"%.2fs" % s	
			
class Timer():
	"""
		Object used to show times of execution
		
		Args:
			t0:	time of the last measure
	"""

	def __init__(self):
		import time
		self.t0 = time.time()
		
	def get_time(self):
		"""
			It gives the time passed since the last measure. It restart everytime it is asked.
			
			Returns:
				time as string rounded at 2
		"""
		
		import time
		seconds = time.time() - self.t0
		
		self.__init__()
		
		return fancy_string_time_from_seconds(seconds)

def sleep(minutes):
	"""
		It sleep x minutes and keep showing how many minutes it has slept

		Args:
			minutes:	minutes to be slept
	"""
	
	import time
	minutes_waited = 0

	while minutes_waited <= minutes:
		print minutes_waited, "min waited"
		time.sleep(60)  # Delay for 1 minute (60 seconds)
		minutes_waited += 1
		
#########################################################################################################
# 							pandas utilities															#
#########################################################################################################

def csv_to_df(uri, delimiter=";", decimal = ","):
	"""
		Process a csv and gives its dataframe
		
		Args:
			uri:		uri of the csv
			delimiter:	char that separates diferents rows
			decimal:	char to separete decimals
			
		Returns:
			Dataframe with the info of the csv
	"""
	
	import pandas as pd
	
	return pd.read_csv(uri, delimiter=delimiter, decimal=decimal)
	
def df_to_csv(uri, df, separator=";", decimal = ","):
	"""
		Stores a dataframe in a csv file
		
		Args:
			uri:		uri of the csv
			separator:	char that separates diferents rows
			decimal:	char to separete decimals
			
	"""
	
	df.to_csv(uri, sep=separator, decimal = decimal)