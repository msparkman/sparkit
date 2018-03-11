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

subredditSearches = properties.subredditSearches
emailMessage = ""
for subredditToSearch in subredditSearches:
	subreddit = reddit.subreddit(subredditToSearch)
	searchPhrases = subredditSearches[subredditToSearch]
	subredditDisplayName = subreddit.display_name

	searchPhrasesString = ",".join(searchPhrases)
	print("Currently searching r/" + subredditDisplayName + " for \"" + searchPhrasesString + "\"")

	submissions = subreddit.new(limit=100)

	# This should filter out submissions from before the time threshold
	timeThreshold = datetime.utcnow() - timedelta(hours=properties.hoursAgo)
	submissionList = [
		submission for submission in submissions
		if (datetime.utcfromtimestamp(submission.created_utc) >= timeThreshold)
	]

	if len(submissionList) < 1:
		continue
	
	submissionsFound = False
	subredditMessage = "<h3>Submissions found in r/" + subredditDisplayName + " for the search phrases (" + searchPhrasesString + "):</h3>"

	for submission in submissionList:
		title = submission.title

		for searchPhrase in searchPhrases:
			# Keep a hashset of submissions found to avoid duplicate rows in the email
			submissionList = []

			if searchPhrase.lower() in title.lower() and submission.id not in submissionList:
				submissionsFound = True
				submissionList.append(submission.id)

				postDateTime = datetime.fromtimestamp(submission.created_utc)
				print(submission.title + " | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p"))

				submissionMessage = "<a href=\"" + submission.shortlink + "\">" + submission.title + "</a> | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p")
				subredditMessage += submissionMessage + "<br /><br />"

	# Skip this subreddit since no submission matches were found
	if not submissionsFound:
		continue

	emailMessage += subredditMessage

if (emailMessage != ""):
	fromEmail = properties.from_email
	toEmail = properties.to_email

	msg = MIMEText(emailMessage, _subtype="html", _charset="UTF-8")
	msg['Subject'] = "Subreddit Search Information"
	msg['From'] = fromEmail
	msg['To'] = toEmail
	try:
		emailServer.sendmail(fromEmail, toEmail, msg.as_string())
	except:
		print("Failed to send email")

emailServer.quit()