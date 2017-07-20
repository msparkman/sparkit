import praw
import properties

reddit = praw.Reddit(client_id=properties.client_id,
					 client_secret=properties.client_secret,
					 user_agent=properties.user_agent)
reddit.config._ssl_url = None

print('Read-Only: ' + str(reddit.read_only))

subreddit = reddit.subreddit('learnpython')
print(subreddit.display_name)