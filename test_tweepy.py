import tweepy, time
from pymongo import MongoClient
import AccessTokens
## local mongodb connection
client = MongoClient("localhost", 27017)
db = client["test"]
collection = db["nba_raw"]

## tweepy search API
API_KEY = AccessTokens.API_KEY
API_SECRET = AccessTokens.API_SECRET
ACCESS_TOKEN = AccessTokens.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = AccessTokens.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

query = "nba"
max_tweets = 2500
searched_tweets = []

## search results
last_id = -1
count = 100

while len(searched_tweets) < max_tweets:
    try:
        time.sleep(5.2)
        print "\nretrieving 100 tweets from %d" %(last_id-1)

        new_tweets = api.search(
            q=query, 
            count=count, 
            max_id=str(last_id - 1),
            lang="en")

        if not new_tweets:
            print "--nothing--"

        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
        print len(searched_tweets), last_id

        result = collection.insert_many([status._json for status in new_tweets])
        print result.inserted_ids[:10]

    except tweepy.TweepError as _e:
        print _e