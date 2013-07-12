import httplib2, urllib2, feedparser, sys, pickle,re, codecs
import socks
from socket import *
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

def httpdate(dt):
    """Return a string representation of a date according to RFC 1123
    (HTTP/1.1).

    The supplied date must be in UTC.

    """
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
        dt.year, dt.hour, dt.minute, dt.second)

class Tweet:
  def __init__(self,username,fullname,tweet,timestamp,turl):
		self.username = username
		self.fullname = fullname
		self.tweet = tweet
		self.timestamp = timestamp
		self.turl = turl

class TwitterScraper:
	def __init__(self,username,count):
		t1 = datetime.now()

		self.username = username
		self.url =  "http://twitter.com/" + username

		conn = httplib2.Http(".cache")
		ims_str = httpdate(datetime.now() - timedelta(minutes=15))
		resp, content = conn.request(self.url,"GET",headers={'Cache-Control':'max-age=128800','If-Modified-Since':ims_str})

		soup = BeautifulSoup(content)

		fullnames = []
		usernames = []
		timestamps = []
		tweet_texts = []
		turls = []

		self.tweets = []

		for s in soup.findAll('strong', attrs={'class': 'fullname'}, limit=count):
			fullnames.append(s.contents)

		ss = soup.findAll('span', attrs={'class': 'username'}, limit=count+1)
		del ss[0] # Remove an empty twitter handle
		for s in ss:
			cs = s.findChildren()
			cs.pop(0)
			for c in cs:
				usernames.append(c.contents)

		for p in soup.findAll('p', attrs={'class': 'js-tweet-text'},limit=count):
			tweet_texts.append(p.contents)

		for s in soup.findAll('a', attrs={'class': 'tweet-timestamp'}, limit=count):
			timestamps.append(s['title'])

		for s in soup.findAll('a', attrs={'class': 'js-details'}, limit=count):
			turls.append(s['href'])

		for n in range(0,len(timestamps)):
			self.tweets.append(Tweet(usernames[n][0],fullnames[n][0],tweet_texts[n][0],timestamps[n],
				                 "http://twitter.com" + turls[n]))

		t2 = datetime.now()

		dt = t2 - t1

		print("[%d]us %s" % (dt.microseconds,username))

	def count(self):
		return len(self.tweets)

	def get_tweet(self,n):
		return self.tweets[n]

	def username(self,n):
		return self.tweets[n].username[0]

	def fullname(self,n):
		return self.tweets[n].fullname[0]

	def tweet(self,n):
		return self.tweets[n].tweet[0]

	def timestamp(self,n):
		return self.tweets[n].timestamp

	def url(self,n):
		return self.tweets[n].turl

