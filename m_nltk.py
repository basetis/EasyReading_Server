"""
	This object is used as a workaround when nltk don't find some of it's data
	
	It first try to find the resources from local, if not found it imports from nltk

	This is useful for using nltk in a server without needing to download nltk data
"""

def sent_tokenize(text, language = "spanish"):
	"""
		It splits the text into sentences
		
		Args:
			text:		text to be splited
			language:	language of the tokenizer to be used
			
		Returns:
			List of sentences
	"""
	
	#try to use from local
	try:
		from utilities import load_pickle
		tokenizer = load_pickle(language, ".pickle", path="nltk_data/tokenizer/punkt/")
			
		return tokenizer.tokenize(text)
	
	#if not, use nltk
	except IOError:
		from nltk import sent_tokenize
		
		return sent_tokenize(text, language)
		
def word_tokenize(text, language = "spanish"):
	"""
		It splits the text into words
		
		Args:
			text:		text to be splited
			language:	language of the tokenizer to be used
			
		Returns:
			List of words
	"""
	
	#try to use from local
	try:
		from nltk.tokenize.treebank import TreebankWordTokenizer
		
		_treebank_word_tokenize = TreebankWordTokenizer().tokenize
	
		return [token for sent in sent_tokenize(text)
            for token in _treebank_word_tokenize(sent)]
		
	#if not, use nltk
	except IOError:
		from nltk import word_tokenize
		
		return word_tokenize(text, language)