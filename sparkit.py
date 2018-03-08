import praw
import properties
import pytz
import smtplib

from datetime import datetime, timedelta
from email.mime.text import MIMEText

emailServer = smtplib.SMTP('smtp.gmail.com', 587)
emailServer.starttls()
emailServer.login(properties.from_email, properties.from_pass)

reddit = praw.Reddit(client_id=properties.client_id,
					 client_secret=properties.client_secret,
					 user_agent=properties.user_agent)

emailMessage = ""
for subreddit in properties.subredditList:
	subreddit = reddit.subreddit(properties.subreddit)
	print("Currently searching r/" + subreddit.display_name + " for \"" + ",".join(properties.searchPhrases) + "\"")

	submissions = subreddit.new(limit=100)

	# This should filter out submissions from before the time threshold
	timeThreshold = datetime.utcnow() - timedelta(hours=properties.hoursAgo)
	submissionList = [
		submission for submission in submissions
		if (datetime.utcfromtimestamp(submission.created_utc) >= timeThreshold)
	]

	if len(submissionList) < 1:
		continue

	'''
	Try to use a map of subreddits to their specific search criteria
	subredditSearches = {
		'motorcycles': [
			'honda'
		],
		'politics': [
			'trump'
		]
	}
	'''

	emailMessage += "Submissions found for r/" + subreddit + ":<br /> "

	for submission in submissionList:
		title = submission.title

		for searchPhrase in properties.searchPhrases:
			# Keep a hashset of submissions found to avoid duplicate rows in the email
			submissionList = []

			if searchPhrase.lower() in title.lower() and submission.id not in submissionList:
				submissionList.append(submission.id)

				postDateTime = datetime.fromtimestamp(submission.created_utc)
				print(submission.title + " | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p"))

				submissionMessage = "<a href=\"" + submission.shortlink + "\">" + submission.title + "</a> | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p")
				emailMessage += "<br />" + submissionMessage

if (emailMessage != ""):
	fromEmail = properties.from_email
	toEmail = properties.to_email

	msg = MIMEText(emailMessage, _subtype="html", _charset="UTF-8")
	msg['Subject'] = "Subreddit (" + properties.subreddit + ") Information"
	msg['From'] = fromEmail
	msg['To'] = toEmail
	try:
		emailServer.sendmail(fromEmail, toEmail, msg.as_string())
	except:
		print("Failed to send email")

emailServer.quit()