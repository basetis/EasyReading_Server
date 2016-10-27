books_path = "Books/"
books_extension = ".txt"

import utilities

def get_book(url, name, fancy_name, path = None):
	"""
		Tries to open the book from local. If not posible it fetches it from the internet.
		
		It has all the necessary functions to do so.
		
		Args:
			url:		URL where the book can be found
			name:		Name of the book in the website/HD 
			fancy_name:	Real name of the book
			
		Returns:
			The text inside the book
	"""
	
	import codecs
	
	def get_book_from_url(url):
		"""
			Args: 
				url: url with some text to read
			
			Returns: 
				The text in the give url
		"""
		
		if url is not None:
			if len(url) > 0:
				import urllib
				
				response = urllib.urlopen(url)
				return response.read().decode('utf8')
			
		else:
			print "No url to retrive the book"

	def save_text_to_txt(name, text, path = None):
		"""
			Store the given text in a document with the given name
			
			Args:
				name: name of the document that it is going to be saved
				text: text to be saved
		"""
			
		uri = utilities.get_full_URI(name, books_extension, path)
		
		with codecs.open(uri, "w", "utf8") as f:#allow working with spanish letters
			f.write(text)
	
	def open_txt(name, path = None):
		"""
			Open the document with the specified name
			
			Args:
				name: name of the document to be opened
		"""
		
		uri = utilities.get_full_URI(name, books_extension, path)
				
		with codecs.open(uri, "r", "utf8") as f:
			filedata = f.read()

		return filedata

	if path is not None:	
		print "\nObtaining", path + fancy_name, "book"
	else:
		print "\nObtaining", fancy_name, "book"
	
	if path is None:
		path = books_path
	
	#Try to get it from local
	try:
		text = open_txt(name, path)
		
	#If not posible, download it
	except IOError:
	
		print "Book", fancy_name, "not in disk."
		print "Downloading it from", url
		
		text = get_book_from_url(url)
		save_text_to_txt(name, text, path)
		
	if len(text) <= 0:
		print "Error when retriving the book"
		
	return text
	
def keep_the_useful_part(text, start_text, end_text):
	"""
		It allows to cut the text given the real start and end. 
		
		Cuts the text that are not part of the real text itself, like anotations, credits, copyright...
		
		Args:
			text:	what to cut
			start:	start position of the real text
			end:	end position of the real text
			
		Returns:
			The useful part of the text
	"""
	
	print "Processing the book"
	
	if len(start_text) > 0:
		start_of_the_book = text.find(start_text)
	else:
		start_of_the_book = None
		
	if len(end_text) > 0:
		end_of_the_book = text.rfind(end_text)
	else:
		end_of_the_book = None
	
	return text[ start_of_the_book : end_of_the_book ]

def tokenize(text):
	"""
		It splits text into sentences and words (what its called tokenize)
		
		Args:
			text:		what will be split
			
		Returns:
			sentences:	list of sentences inside the text
			words:		list of words inside the text
	"""
	
	def format_text(text):
		"""
			It clears some common formating errors
		"""

		def recursive_replace(s, sub, new):
		    while sub in s:
		        s = s.replace(sub, new)
		    return s
		    
		text = recursive_replace(text, "  ", " ")
		text = text.replace("\n", ".\n")
		text = recursive_replace(text, "..\n\n", ".\n")
		text = recursive_replace(text, "\n\n", "\n")
		text = recursive_replace(text, " .", ".")

		return text

	text = format_text(text)

	#partial fork of nltk to solve problems with missing data in the server
	from m_nltk import word_tokenize, sent_tokenize
	
	print "Tokenizing sentences"
	sentences = sent_tokenize(text, "spanish")
	
	print "Tokenizing words"
	words = word_tokenize(text, "spanish")
	
	return sentences, words

	
class Book():
	"""
		Object to work with books.
		
		First it opens the book (from local or url if not found).
		
		Then it reads its text (it can be splited)
		
		Then it is tokenized into sentences and words
		
		Args:
			fancy_name:	Real name of the book
			name:		Name of the book in the website/HD 
			url:		URL where the book can be found
			start:		Fragment of the start of the book, to delete all before that
			end:		Fragment of the end of the book, to delete all after that
			path:		Path of the Book
	"""

	def __init__(self, fancy_name, name = None, url = None, start = None, end = None, path = None):
	
		self.url = url
		self.path = path
		
		if name is None:
			self.name = fancy_name
		else:
			self.name = name
			
		self.fancy_name = fancy_name
		
		raw_text = get_book(url, self.name, self.fancy_name, path)
		
		if start is not None and end is not None:
			self.text = keep_the_useful_part(raw_text, start, end)
		else:
			self.text = raw_text
		
		self.sentences, self.words = tokenize(self.text)
		
		if self.path is not None:
			print self.path + fancy_name, "has been processed"
		else:
			print fancy_name, "has been processed"
		
	def get_tokenized_info(self):
		"""
			This functions gives all the tokeni info. 
			That will be used to analize the book.
			
			Returns:
				text:		all the text from the book
				sentences:	list of sentences inside the text
				words:		list of words inside the text 
		"""
		return self.text, self.sentences, self.words

#############################################################################################################
# 							Spanish books																	#
#############################################################################################################
		
def get_cervantes():
	
	cervantes = Book("Don Quijote",
						"pg2000",
						"http://www.gutenberg.org/cache/epub/2000/pg2000.txt",
						"Primera parte del ingenioso hidalgo don Quijote de la Mancha",
						"End of Project Gutenberg's Don Quijote, by Miguel de Cervantes Saavedra")
	
	return cervantes.get_tokenized_info()
	
def get_argentina():
	#Poemas antiguos
	argentina = Book("La Argentina (poemas)",
						"pg25317",
						"http://www.gutenberg.org/cache/epub/25317/pg25317.txt",
						"CANTO PRIMERO.",
						"End of the Project Gutenberg EBook of La Argentina")
	
	return argentina.get_tokenized_info()
	
def get_politica():
	politica = Book("La Politica de los Estados Unidos en el Continente Americano",
						"pg45508",
						"http://www.gutenberg.org/cache/epub/45508/pg45508.txt",
						"LA OCUPACI",
						"Nota del Transcriptor")
	
	return politica.get_tokenized_info()

	
#############################################################################################################
# 							Catalan books																	#
#############################################################################################################
	
def get_carner():
	
	carner = Book("La creacio d'Eva i altres contes",
						"pg17219",
						"http://www.gutenberg.org/cache/epub/17219/pg17219.txt",
						"LA CREACI",
						"End of Project Gutenberg's La creaci")
	
	return carner.get_tokenized_info()
	
def get_tradicions():
	
	tradicions = Book("Tradicions religiosas de Catalunya",
						"pg35817",
						"http://www.gutenberg.org/cache/epub/35817/pg35817.txt",
						"Las tradicions religiosas",
						"End of the Project Gutenberg EBook of Tradicions religiosas de Catalunya")
	
	return tradicions.get_tokenized_info()
	
def get_sawyer():
	
	sawyer = Book("Les Aventures De Tom Sawyer",
						"pg30890",
						"http://www.gutenberg.org/cache/epub/30890/pg30890.txt",
						"-Tom!",
						"End of Project Gutenberg's Les Aventures De Tom Sawyer, by Mark Twain")
	
	return sawyer.get_tokenized_info()
 
 
 
#If it is not imported, run that	
if __name__ == '__main__':
	get_cervantes()