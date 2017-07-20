# sparkit

###Installation
1. Install [Python](https://www.python.org/downloads/). 
	- I used the latest at the time which was 3.6.1
2. Go to the [PRAW GitHub](https://github.com/praw-dev/praw) to see its readme on how to install.
	- Alternatively you can just do `pip install praw`
	- The docs are available [here](https://praw.readthedocs.io/en/latest/)
3. Add a properties.py file to the same directory level as sparkit.py. It has to contain the following properties:
	```
		client_id='yourRedditClientID'
		client_secret='yourRedditClientSecret',
		user_agent='yourUserAgent'
	```
	- You will need to replace the text in the quotes with your respective credentials.