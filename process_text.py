#############################################################################################################
# 							Utilities to work with text														#
#############################################################################################################

import utilities as u

#When a 0 occurs, its log10() will be -inf. That will be replaced for the next value
VALUE_INF = -2.5

def delete_nones_from_list(list):
	"""
		Delete all the entries that are not tagged
		
		Args:
			list: tagged entries
		
		Returns:
			list without the entries tagged as None
	"""
	
	return [x for x in list if x[1] is not None]
		
class Grammatical_categories:
	"""
		It has all the functions related to grammatical_categories.
		
		Works with this classification: http://clic.ub.edu/corpus/webfm_send/18 
		
		Attributes:
			existing_categories:		list of all posible main categories
			complete_tagged_list:		list of all the words and their categories
			successfully_tagged_list:	list of words (that has been successfully tagged) and their categories
			complete_categories:		array of categories of all the words
			tagged_categories:			array of categories of the words successfully tagged
	
	"""
	
	def __init__(self, tagged_list):
	
		"""
			It takes a list of tagged info (usually words) 
			
			Example:
				input: [('Simon', 'Noun'), ('say', 'Verb'), ('House', 'Noun')]
			
			Args:
				tagged_list:		list of words and their category
				delete_not_tagged:	Allow to drop the untagged objects
				
			Returns:
				Dictionary of frequencies
		"""
		
		#More info: http://clic.ub.edu/corpus/webfm_send/18
		# Categories not in use: i, f, w, z
		self.existing_categories = ['a', 'c', 'd', 'n', 'p', 'r', 's', 'v']
		
		self.complete_tagged_list = tagged_list
		self.successfully_tagged_list = delete_nones_from_list(tagged_list)
		
		#Transform into an array to get only the categories
		import numpy as np
		
		#Categories of all the given words
		aux_array = np.asarray(self.complete_tagged_list)
		self.complete_categories = aux_array[:,1]
		
		#Categories of all the words tagged (without the 'None')
		aux_array = np.asarray(self.successfully_tagged_list)
		self.tagged_categories = aux_array[:,1]
		
	def _list_to_dictionary(self, list):
		"""
			Given a list it counts every the repetead words and put in a dictionay of frequencies
			
			Args:
				list:	list to be counted
				
			Returns:
				Dictionary of frequencies
		"""
		
		from collections import Counter
		
		return Counter(list)
	
	def get_complete_categories(self):
		"""
			It gives all the existing_categories in a dictionay
			
			Returns:
				Dictionary of frequencies of every categories in the text
		"""

		output = self._list_to_dictionary(self.tagged_categories)
		#print "\nThere are", len(output), "different complete categories in the given text"
			
		return output

	def get_main_categories(self):
		"""
			This gives an array with the frequencies of each main categegory
			
			Returns:
				Dictionary of frequencies of every categories in the text
		"""
		#keeps only the first letter of every category
		aux = [x[:1] for x in self.tagged_categories]

		#transform to a dictionay
		dict_categories = self._list_to_dictionary(aux)

		#print "\nThere are", len(dict_categories), "different main categories in the given text"
		
		#transform to give in the desired format
		output = []
		for categegory in self.existing_categories:
			output.append( dict_categories[categegory] )
			
		return output
		
	def get_main_categories_relative_frequency(self):
		"""
			Returns:
				Array of percentages of every categegory following the list self.existing_categories
		"""

		return u.divide_list_per_scalar(self.get_main_categories(), len(self.successfully_tagged_list))
		
	def get_main_categories_per_sentences(self, num_sentences):
		
		"""
			It calculate the mean of words of each grammatical categegory per sentence
			
			Args:
				num_sentences:	how many sentences has the text
			Returns:
				Array of values
		"""
		
		return u.divide_list_per_scalar(self.get_main_categories(), num_sentences)
		
	def get_ratio_main_verbs(self):
	
		"""
			It calculate the percentage of main verb of all the verbs
			
			Returns:
				percentage of main verbs
		"""
	
		verbs_list = [x for x in self.tagged_categories if x[:1] == 'v']
		
		self.main_verbs = 0
		self.aux_verbs = 0
		self.semi_aux_verbs = 0
		
		for verb in verbs_list:
			if verb[:2] == "vm":
				self.main_verbs += 1
				
			elif verb[:2] == "va":
				self.aux_verbs += 1

			else:
				self.semi_aux_verbs += 1
				
		if len(verbs_list) == 0:
			return 0
		else:
			return self.main_verbs/(1.0*len(verbs_list))
		
	def words_diversity(self, num_sentences):
		"""
			It gives an estimator of the words diversity. 
			It counts how many different words it has and then normalize that dividing per num_sentences
			
			Args:
				num_sentences:	how many words has the text
				
			Returns:
				A number descriving the words_diversity
		"""
		
		num_diferent_words = len(self._list_to_dictionary(self.complete_tagged_list))
			
		return num_diferent_words / (1.0*num_sentences)
		
	def main_verbs_per_sentence(self, num_sentences):
		
		return self.main_verbs/(1.0*num_sentences)
		
def average_len(list):
	"""
		Args:
			list: list to be used
			
		Returns:
			Average length of every object in the list
	"""
	
	lengths = [len(i) for i in list]
	return 0 if len(lengths) == 0 else (float(sum(lengths)) / len(lengths)) 
	
def get_info(text, sentences, words):
	"""
		This function is used to transform a text to an array of useful information to be used in ML.
		
		Args:
			text: raw input text
			sentences: tokenized text into sentences
			words: tokenized text into words
			
		Returns:
			Array of metrics of the text
	"""
	
	info = []
	
	info.append( len(words)/(1.0*len(sentences)) )	#words/sentences average
	info.append( average_len(words) ) 				#letters/word average
	
	from text_tagger import cess_esp
	tagger = cess_esp()
	
	tagged_words = tagger.uni.tag(words)
	
	#Check that it is posible to tag at least 1 word
	if len(delete_nones_from_list(tagged_words)) > 0:

		gram_cat = Grammatical_categories(tagged_words)
		
		#frequencies of each categegory in the text
		for freq  in gram_cat.get_main_categories_relative_frequency():
			info.append(freq)
		
		for freq in gram_cat.get_main_categories_per_sentences(len(sentences)):
			info.append(freq)
			
		info.append(gram_cat.get_ratio_main_verbs())	#main_verbs/verbs
		
		info.append(gram_cat.words_diversity(len(sentences)))
		
		info.append(gram_cat.main_verbs_per_sentence(len(sentences)))
		
		def add_log_vars():
			"""
				Do the log of every variable and add those vars to the existing
			"""
			
			import numpy as np
			aux = np.log10(info)

			#replace -infinite values for a fixed value
			aux[np.isneginf(aux)] = VALUE_INF

			return info + aux.tolist()

		#return add_log_vars()
		return info

	else:
		return None
	
def get_metrics_header():
	"""
		It gives the names of the metrics calculated for every text
		
		Returns:
			Array of names
	"""
	
	headers = ["words_p_sen", "letters_p_word",
				'%adjective', '%conjunction', '%determiner', '%noun', 
				'%pronoun', '%adverb', '%preposition', '%verb',
				'adjective_p_sen', 'conjunction_p_sen', 'determiner_p_sen', 'noun_p_sen', 
				'pronoun_p_sen', 'adverb_p_sen', 'preposition_p_sen', 'verb_p_sen',
				"main_verbs/total_verbs", "words_diversity", "main_verbs_per_sen"]

	#headers += ["log_" + x for x in headers]

	return headers
	
def process_text_from_document(doc_name, doc_path = None):
	"""
		Process 1 text document to get all the metrics
		
		Args:
			doc_name:	name of the document to be processed
			doc_path:	path of the document to be processed
			
		Returns:
			A row-like array of all the metrics extracted from the text
	"""
	
	from preprocess import Book
	
	#print text_path + folder + "/" + doc_name
				
	mBook = Book(doc_name, path = doc_path)
	text, sentences, words = mBook.get_tokenized_info()
				
	return get_info(text, sentences, words)
	
def process_text_from_string(text):
	"""
		Process 1 text given as a string
		
		Args:
			text:	string containing all the text
			
		Returns:
			A row-like array of all the metrics extracted from the text
	"""
	from preprocess import tokenize
	sentences, words = tokenize(text)
	
	return get_info(text, sentences, words)

#############################################################################################################
# 							Functions to inspect															#
#############################################################################################################

def get_midle_values(list, start = -1, size_to_display=10, print_them = True):
	"""
		Shows some items in a long list
		
		Args:
			list:				list which will be used to show values
			start:				first element to display, if=0 it will start in the middle
			size_to_display:	how many elemens will be displaed
			print_them:			if True prints the items
	"""
	
	#default start is the middle
	if start < 0:
		start = len(list)/2
	
	#Check if there are enough items
	if size_to_display > len(list):
		print "It is not posible to show that number of objects"
		size_to_display = len(list)
	
	#change start if there are not enough elemens
	if start + size_to_display >= len(list):
		print "Not posible to start at", start
		start = len(list) - size_to_display
		
	end = start + size_to_display
	items = list[start:end]
	
	if print_them:
		print "\nSome items in the list are:\n", items
	
	return items
	
def efficiency_tagger(list, words):
	"""
		Counts the efficiency of a tagger and the number of words not tagged
			
		Efficiency defined as words_tagged/total_words
		
		Args:
			list: tagged entries
	"""
	count_tagged = len(delete_nones_from_list(list))
	
	tagged_percent = 100*count_tagged/(1.0*len(words))
	
	print "\nEfficiency tagger: %.2f%%" % tagged_percent, "(Percentage tagged)"
	print "Words not tagged:", len(list) - count_tagged
	
#############################################################################################################
# 							Testing part																	#
#############################################################################################################	

def calculate_metrics(text, sentences, words):
	"""
		Calculates some metrics from a given text
		
		Args:
			text: raw input text
			sentences: tokenized text into sentences
			words: tokenized text into words
	"""
	
	print "\nIt has:"
	print "\t", len(text), "characters"
	print "\t", len(sentences), "sentences"
	print "\t", len(words), "words"
	print "\t", len(words)/(1.0*len(sentences)), "words/sentences average"
	print "\t", average_len(words), "letters/word average"
	
def test_tagger(tagged_words, words):
	"""
		Test a little bit how the tagger is working
		
		Args:
			tagged_list:		list of words and their category
			words:				list of words	
	"""
	efficiency_tagger(tagged_words, words)

	get_midle_values(tagged_words)
	
	frequencies = Grammatical_categories(tagged_words).get_main_categories_relative_frequency()
	
	print "\nFrequencies for each grammatical categegory:\n", frequencies

	
import preprocess

def test_spanish():
	"""
		Use the book cervantes to test the tagger.
		
		It uses the tagger trained with the CESS_ESP corpus
	"""
	text, sentences, words = preprocess.get_cervantes()
	
	calculate_metrics(text, sentences, words)

	from text_tagger import cess_esp
	tagger = cess_esp()
	
	print "Starting to tag"
	
	tagged_words = tagger.uni.tag(words)
	
	test_tagger(tagged_words, words)

def test_catalan():
	"""
		Use the book 'La creacio d'Eva i altres contes' to test the tagger.
		
		It uses the tagger trained with the CESS_CAT corpus
	"""
	text, sentences, words = preprocess.get_carner()
	
	calculate_metrics(text, sentences, words)

	from text_tagger import cess_cat
	tagger = cess_cat()
	
	print "Starting to tag"
	
	tagged_words = tagger.uni.tag(words)

	test_tagger(tagged_words, words)

	
	
#If it is not imported, run that	
if __name__ == '__main__':
	test_spanish()