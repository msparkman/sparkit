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
		hoursAgo=1
	```
	- You will need to replace the text in the quotes with your respective credentials.
5. (Optional) Schedule the script to run automatically:
	1. Windows: Add a scheduled task via schtasks
		- In a windows terminal (Command Prompt, cmder, etc), type the following:
			`schtasks /Create /SC HOURLY /TN SparkitTask /TR "<python.exe path> <script path>"`
		- You can replace HOURLY with the other acceptable Task Scheduler intervals.
		- NOTE: When I first executed this schtasks command, it added the task successfully (you can check the active tasks in Task Scheduler) and showed that it would run every hour after the initial trigger time, but it didn't seem to run when the task was created. I ended up editing the task to start a few minutes later and it ran just fine.
	2. Unix: Add a crontab
		- Edit the cronjobs via `crontab -e`
		- Add a line with the following: `0 * * * * <python path> <sparkit directory>/sparkit.py`
		- This will run at the bottom of every hour