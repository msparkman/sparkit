from datetime import datetime, timedelta
import praw
import properties
import pytz
import smtplib

emailServer = smtplib.SMTP('smtp.gmail.com', 587)
emailServer.starttls()
emailServer.login(properties.from_email, properties.from_pass)

reddit = praw.Reddit(client_id=properties.client_id,
					 client_secret=properties.client_secret,
					 user_agent=properties.user_agent)

subreddit = reddit.subreddit(properties.subreddit)
print("Currently searching r/" + subreddit.display_name + " for \"" + properties.searchPhrase + "\"")

submissions = subreddit.new(limit=100)

# This should filter out submissions from before the time threshold
timeThreshold = datetime.utcnow() - timedelta(hours=properties.hoursAgo)
submissionList = [
	x for x in submissions
	if (datetime.utcfromtimestamp(x.created_utc) >= timeThreshold)
]

emailMessage = ""
for submission in submissionList:
	title = submission.title

	if properties.searchPhrase in title.lower():
		postDateTime = datetime.fromtimestamp(submission.created_utc)
		submissionMessage = submission.title + " | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p")
		print(submissionMessage)

		emailMessage += "\n" + submissionMessage

if (emailMessage != ""):
	try:
		emailServer.sendmail(properties.from_email, properties.to_email, emailMessage)
	except:
		print("Failed to send email")

emailServer.quit()