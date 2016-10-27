"""
	The aim of this package is to guess the difficulty of a text.
	
	It has 2 main parts:
		* Natural Language Processing (NLP)
		* Machine Learning (ML)
		
	NLP allows to process text and extract some metrics and other stuff that will be usefull for the ML part
	
	ML gives tools to extract patterns about the data and finally guess the difficulty of a new text given
	its metrics
	
"""

from setuptools import setup

setup(name='EasyReading',
      version='0.1',
      description='LF Text Classifier',
      author='Arnau Villoro',
      author_email='arnau.villoro@basetis.com'
     )
