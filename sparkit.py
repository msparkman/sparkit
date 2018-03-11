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

	print("Currently searching r/" + subredditDisplayName + " for \"" + ",".join(searchPhrases) + "\"")

	submissions = subreddit.new(limit=100)

	# This should filter out submissions from before the time threshold
	timeThreshold = datetime.utcnow() - timedelta(hours=properties.hoursAgo)
	submissionList = [
		submission for submission in submissions
		if (datetime.utcfromtimestamp(submission.created_utc) >= timeThreshold)
	]

	if len(submissionList) < 1:
		continue
	
	emailMessage += "<h3 font-weight=\"bold\">Submissions found in r/" + subredditDisplayName + " for the search phrases (" + ",".join(searchPhrases) + "):</h3>"

	for submission in submissionList:
		title = submission.title

		for searchPhrase in searchPhrases:
			# Keep a hashset of submissions found to avoid duplicate rows in the email
			submissionList = []

			if searchPhrase.lower() in title.lower() and submission.id not in submissionList:
				submissionList.append(submission.id)

				postDateTime = datetime.fromtimestamp(submission.created_utc)
				print(submission.title + " | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p"))

				submissionMessage = "<a href=\"" + submission.shortlink + "\">" + submission.title + "</a> | " + postDateTime.strftime("%a %b %d %Y %I:%M:%S %p")
				emailMessage += submissionMessage + "<br /><br />"

if (emailMessage != ""):
	fromEmail = properties.from_email
	toEmail = properties.to_email

	msg = MIMEText(emailMessage, _subtype="html", _charset="UTF-8")
	msg['Subject'] = "Subreddit Search Information"
	msg['From'] = fromEmail
	msg['To'] = toEmail
	try:
		emailServer.sendmail(fromEmail, toEmail, msg.as_string())
		#print("\n" + emailMessage)
	except:
		print("Failed to send email")

emailServer.quit()