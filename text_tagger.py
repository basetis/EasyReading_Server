#-*- coding: utf8 -*-

"""
Tagger to use in spanish and all the functions needed to work with it.

More info:
	http://stackoverflow.com/questions/14732465/nltk-tagging-spanish-words-using-a-corpus
	https://github.com/alvations/spaghetti-tagger
"""
from nltk import UnigramTagger, BigramTagger, TrigramTagger
import utilities

N_GRAM_NAMES = ["unigram", "bigram", "trigram"]
NOMWE_TEXT = "nomwe"
TAGGER_EXTENSION = '.tagger'

TAGGER_PATH = "Taggers/"

def train_tagger(corpus_name, corpus):
	"""
	Train the taggers and saves them
	
	Args:
		corpus_name: 	name of the corpus used to create the tagger
		corpus: 		corpus for creating the tagger
	"""
	
	#List of n-gram taggers names
	complete_names = [corpus_name + '_' + x for x in N_GRAM_NAMES]
	
	# Training UnigramTagger
	tagger1 = UnigramTagger(corpus)
	utilities.save_pickle(tagger1, complete_names[0], TAGGER_EXTENSION, TAGGER_PATH)
	print "UnigramTagger trained with", corpus_name
	
	# Training BigramTagger
	tagger2 = BigramTagger(corpus)
	utilities.save_pickle(tagger2, complete_names[1], TAGGER_EXTENSION, TAGGER_PATH)
	print "BigramTagger trained with", corpus_name
	
	# Training TrigramTagger
	tagger3 = TrigramTagger(corpus)
	utilities.save_pickle(tagger3, complete_names[2], TAGGER_EXTENSION, TAGGER_PATH)
	print "TrigramTagger trained with", corpus_name
	

# Function to unchunk corpus
def unchunk(corpus):
	"""
	Given a corpus it splits all the Multi-Word Expressions
	
	Args:
		corpus: corpus to use
	"""
	nomwe_corpus = []
	for i in corpus:
		nomwe = " ".join([j[0].replace("_", " ") for j in i])
		nomwe_corpus.append(nomwe.split())
	return nomwe_corpus

class Tagger():
	"""
	Tagger trained using cess_esp corpus
	
	Attributes:
		mwe:	Indicates if we want to recognize Multi-Word Expressions as one token
		uni:	UnigramTagger
		bi:		BigramTagger
		tri:	TrigramTagger
	"""
	
	def __init__(self, name_tagger, corpus, mwe=True):
		"""
		When initialized it will load all the taggers. They are:
			* UnigramTagger
			* BigramTagger
			* TrigramTagger
			
		If not possible it will create them, and save them.

		If Multi-Word Expressions are not allowed its necessary to split them 
		and then use a UnigramTagger to be trained
		
		Args:
			name_tagger:	root part of the name of the tagger, like cess_esp
			corpus:			corpus that will train the tagger
			mwe:			It can allow Multi-Word Expressions
		"""
		
		self.mwe = mwe
		
		if not mwe:
			name_tagger += '_' + NOMWE_TEXT
			
		#set the names of the taggers like: 
		#		cess_es_unigram.tagger,			cess_es_bigram.tagger
		#	or	cess_es_nomwe_unigram.tagger,	cess_es_nomwe_bigram.tagger
		complete_names = [name_tagger + '_' + x for x in N_GRAM_NAMES]
		
		# Try to load the taggers.		
		try:	
			for x in complete_names:
				utilities.load_pickle(x, TAGGER_EXTENSION, TAGGER_PATH).tag(['hola'])
		
		#If it not work create them
		except IOError:
			print "\n*** First-time use of", name_tagger, " taggers ***"
			print "Training taggers ..."
			
			timer = utilities.Timer()
			
			if self.mwe:
				cess_sents = corpus.tagged_sents()
				train_tagger(name_tagger, cess_sents)
			
			else:
				#Without mutliwords we need to split them
				cess_sents = unchunk(corpus.tagged_sents())
				
				#We need the mwe tagger to train
				aux_tagger = tagger(name_tagger, corpus, mwe=True)
				tagged_cess_nomwe = aux_tagger.uni.tag_sents(cess_sents)
				train_tagger(name_tagger + '_' + NOMWE_TEXT, tagged_cess_nomwe)
			
			print "\nAll taggers trained in", timer.get_time(), "seconds"
			
		# Load tagger
		self.uni = utilities.load_pickle(complete_names[0], TAGGER_EXTENSION, TAGGER_PATH)
		self.bi = utilities.load_pickle(complete_names[1], TAGGER_EXTENSION, TAGGER_PATH)
		self.tri = utilities.load_pickle(complete_names[2], TAGGER_EXTENSION, TAGGER_PATH)

		### TODO: Set backoffs for every tagger ###

def cess_esp(mwe=True):
	"""
	This gives a tagger created with the corpus CESS_ESP
	
	Args:
		mwe:	It can allow Multi-Word Expressions
	"""
	
	from nltk.corpus import cess_esp as corpus
	
	return Tagger('cess_esp', corpus, mwe)
	
def cess_cat(mwe=True):
	"""
	This gives a tagger created with the corpus CESS_CAT
	
	Args:
		mwe:	It can allow Multi-Word Expressions
	"""
	
	from nltk.corpus import cess_cat as corpus
	
	return Tagger('cess_cat', corpus, mwe)
	
	
	
#If it is not imported, run that	
if __name__ == '__main__':
	mtagger = cess_esp()
	print mtagger.uni.tag('A la patata le gusta bailar ska .'.split())