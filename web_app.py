print '\nStarting Server...'
from flask import Flask, request, jsonify
import json

TOKEN = 'XXXX' #Personal

app = Flask(__name__)

@app.route('/test')
def test():
	"""
		Used to test the conection it will return some random text
	"""
	return "Server working!"

@app.route("/doMagic", methods=["POST"])
def doMagic():
	"""
		Extract the text from the given JSON. 
		Then do some checks to verify that the data is in the correct format
		Finally it classify its text
	"""

  	try:
		# parse input data
		try:
			data = request.json
		except:
			print 'Value Error'
			raise ValueError

		if data is None:
			print 'Value Error: data is None'
			raise ValueError

		#security layer before processing
		try:
			if data.get('token') == TOKEN:
				# extract and validate text
				try:
					text = data.get("text")
					
					#verify that there is text
					if not text:
						print 'Value Error: data is None'
						raise ValueError

					#apliquem el processat
					from ML_classifier import classify_new_text
					tag = classify_new_text(text)
					#tag = 'sampleTag' #testing purpose, delete

					# return 200 Success
					return jsonify({"tag":tag})
							
				except (TypeError, KeyError):
					raise ValueError
			else:
				return 'Authentication error', 403

		except (TypeError, KeyError):
			raise ValueError		
	except ValueError:
		# if bad request data, return 400 Bad Request
		return 'Bad request data', 404

if __name__ == '__main__':
	app.run()