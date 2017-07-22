import datetime
import praw
import properties
import pytz
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(properties.from_email, properties.from_pass)

reddit = praw.Reddit(client_id=properties.client_id,
					 client_secret=properties.client_secret,
					 user_agent=properties.user_agent)

subreddit = reddit.subreddit(properties.subreddit)
print("Currently searching r/" + subreddit.display_name + " for \"" + properties.searchPhrase + "\"")

emailMessage = ""
for submission in subreddit.hot(limit=10):
	title = submission.title

	if properties.searchPhrase in title.lower():
		postDateTime = datetime.datetime.fromtimestamp(submission.created_utc)
		submissionMessage = submission.title + " | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p")
		print(submissionMessage)

		emailMessage += "\n" + submissionMessage

if (emailMessage != ""):
	try:
		server.sendmail(properties.from_email, properties.to_email, emailMessage)
	except:
		print("Failed to send email")

server.quit()