# sparkit
### This script is designed to look in a specific subreddit for a each word/phrase from a list and send out a notification if any submissions that match are found.

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
		subredditSearches = {
			'motorcycles': [
				'suzuki',
				'sv1000s'
			],
			'bikesgonewild': [
				'track',
				'summer',
				'race'
			]
		}
		hoursAgo=1
	```
	- You will need to replace the text in the quotes above the Variables with your respective credentials.
	- You should replace 'motorcycles'/'bikesgonewild' with the subreddits you want to search and the listed text beneath each one with whatever phrases you want to search for.
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

## Troubleshooting
1. Error printing output in a cronjob
	- When running this script from a cronjob and still want the print statements to be used, you might encounter an error from a submission title containing a utf-8 character. You'll need to change the line that prints the found submission to be:
		`print(submission.title.encode('utf-8') + " | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p"))`
	- I noticed this issue when running my script from an aws ec2 instance but only when it ran automatically from a cronjob. If I ran the script manually to output the same submission matches, the error wouldn't occur. Also, the above fix seemed to blow up when I ran this script manually in windows which is why I am removing it from the source. I usually comment out the print statement when the script is running in the background anyways.