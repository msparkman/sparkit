# sparkit
### This script is designed to look in a specific subreddit for a word/phrase and send out a notification if any submissions that match are found.

## Installation
1. Install [Python](https://www.python.org/downloads/). 
	- I used the latest at the time which was 3.6.1
2. Install [PRAW](https://github.com/praw-dev/praw)
	- `pip install praw`
	- The docs are available [here](https://praw.readthedocs.io/en/latest/)
3. Install [pytz](http://pythonhosted.org/pytz/)
	- `pip install pytz`
4. Add a properties.py file to the same directory level as sparkit.py. It has to contain the following properties:
	```
		# Credentials
		client_id='yourRedditClientID'
		client_secret='yourRedditClientSecret',
		user_agent='yourUserAgent'
		from_email='from@email.com'
		from_pass='fromEmailPassword'
		to_email='to@email.com'

		# Variables
		subreddit='all'
		searchPhrase='trump'
	```
	- You will need to replace the text in the quotes with your respective credentials.