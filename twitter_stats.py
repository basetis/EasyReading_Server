import utilities as u
import datetime, time

#needs to be updated with a registred twitter app
TWITTER_API_KEY = 'XXXX'
TWITTER_API_KEY_SECRET = 'YYYY' 
TWITTER_ACCESS_TOKEN = 'ZZZZ'
TWITTER_ACCESS_TOKEN_SECRET = 'WWWW'

COMPETITION_NAME = '#smartCATchallenge'
COMPETITION_START_DATE = datetime.datetime.strptime('17/10/2016 10:00', '%d/%m/%Y %H:%M')
COMPETITION_END_DATE = datetime.datetime.strptime('23/10/2016 10:00', '%d/%m/%Y %H:%M')

TWITTER_PATH = "Twitter/"
PARTICIPANTS = "Apps.txt"
RESULTS_CSV = "Results_SmartCAT.csv"
TWITTER_PICKLE = "Votes"
LAST_UPDATE = "Last update"

def check_hashtag(hashtag):
	"""
		Checks if the given string is a hashtag, if not it adds a #
	"""
	
	if hashtag[:1] != "#":
		return "#" + hashtag
	else:
		return hashtag

def count_tweets_of_app(app_name):
	"""
		Counts how many tweets are with the hashtag app_name and COMPETITION_NAME from diferent users

		Args:
			app_name:	name of the app of whose tweets are to be counted

		Returns:
			num of votes (tweets)
	"""

	from TwitterSearch import TwitterSearchOrder, TwitterSearch, TwitterSearchException
	try:
		tso = TwitterSearchOrder() # create a TwitterSearchOrder object
		tso.set_keywords([check_hashtag(app_name), COMPETITION_NAME]) # let's define all words we would like to have a look for

		# it's about time to create a TwitterSearch object with our secret tokens
		ts = TwitterSearch(
			consumer_key = TWITTER_API_KEY,
			consumer_secret = TWITTER_API_KEY_SECRET,
			access_token = TWITTER_ACCESS_TOKEN,
			access_token_secret = TWITTER_ACCESS_TOKEN_SECRET)

		# this is where the fun actually starts :)
		users = []
		#count = 0

		for tweet in ts.search_tweets_iterable(tso):

			user = tweet['user']['id']

			#Check if tweet if from the same user
			if user not in users:
				#more info https://dev.twitter.com/overview/api/tweets
				time_tweet = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')

				if (COMPETITION_START_DATE < time_tweet) & (time_tweet < COMPETITION_END_DATE):
					users.append(user)
					#count += 1 + tweet["retweet_count"]
					#print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

		return len(users)

	except TwitterSearchException as e: # take care of all those ugly errors if there are some
		print(e)
		return -1

def calculate_oldest():
	"""
		It calculates the votes for the 15 oldest apps to be counted. 
		Then it stores the votes in a csv in the column of the day calculated

		After reading it saves the values in the csv
	"""
	import pandas as pd
	import time

	try:
		uri = TWITTER_PATH + RESULTS_CSV
		date = time.strftime("%d/%m/%Y")

		df = pd.read_csv(uri, delimiter=";", decimal=",", index_col=0)

		#ask for 15 apps and store new values if correct
		for i in xrange(15):
			#Order by last update
			df = df.sort_values(by=[LAST_UPDATE], ascending=[True])

			name_app = df.index[0]
			num_votes = count_tweets_of_app(name_app)

			print name_app, "=>", num_votes

			if num_votes >= 0:
				#Store votes and last update
				df.set_value(name_app, date, num_votes)
				df.set_value(name_app, LAST_UPDATE, time.time())

		#Reorder by votes of last day
		df = df.sort_values(by=[date], ascending=[False])

		#Save results to csv
		df.to_csv(uri, sep=";", decimal = ",") 

		print "\n", df[date], 

	except IOError:
		print "CSV not found, aborting"



if __name__ == '__main__':
	"""
		It calculates 15 apps every 15 minutes and store the votes in a csv
	"""
	while True:
		calculate_oldest()
		#sleep 15 minutes 
		print "\n\nThis process will sleep 15 minutes due to Twitter api limits\n"
		u.sleep(15)