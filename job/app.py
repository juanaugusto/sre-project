import bson
import os
import pymongo
import time
from clients.twitter.api import TwitterAPI
from dateutil.parser import parse


BEARER_TOKEN = os.environ['BEARER_TOKEN']
MONGO_ROOT_USERNAME = os.environ['MONGO_ROOT_USERNAME']
MONGO_ROOT_PASSWORD = os.environ['MONGO_ROOT_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']
HASHTAGS = os.environ['HASHTAGS']

time.sleep(10) # Wait Mongo DB be ready

mongo_client = pymongo.MongoClient('mongodb://%s:%s@%s:27017/admin' % 
                                    (MONGO_ROOT_USERNAME, 
                                     MONGO_ROOT_PASSWORD, 
                                     MONGO_HOST))

tweets_collection = mongo_client.twitterDB.tweets
users_collection = mongo_client.twitterDB.users

twitter_api = TwitterAPI(BEARER_TOKEN)

hashtags_array = HASHTAGS.split(';')

while True:

    for hashtag in hashtags_array:
        try:
            tweets = twitter_api.search_tweets(hashtag, 100)
        except:
            continue

        for tweet in tweets:
            tweet_id = tweet['id']
            tweet_text = tweet['text']
            tweet_hour_created_at = parse(tweet['created_at']).hour
            tweet_lang = tweet['lang']
            user_id = tweet['user']['id']
            user_name =  tweet['user']['name']
            user_followers_count = tweet['user']['followers_count']
            user_location = tweet['user']['location']

            try:
                if tweets_collection.find_one({'tweet_id': tweet_id}) is None:
                    tweet_object_id = tweets_collection.insert_one({
                        'tweet_hashtag': hashtag,
                        'tweet_id': tweet_id,
                        'tweet_text': tweet_text,
                        'tweet_hour_created_at': tweet_hour_created_at,
                        'tweet_lang': tweet_lang,
                    }).inserted_id

                    if users_collection.find_one({'user_id': user_id}) is None:
                        users_collection.insert_one({
                            'user_id': user_id,
                            'user_name': user_name,
                            'user_followers_count': user_followers_count,
                            'user_location': user_location,
                            'tweets': []
                        })

                    user = users_collection.find_one({'user_id': user_id})
                    user_object_id = user['_id']
                    del user['_id']
                    user['tweets'] += [tweet_object_id]

                    users_collection.find_one_and_update(
                        {"_id": user_object_id}, 
                        {"$set": user}, 
                        upsert=True
                    )
            except:
                continue

        time.sleep(2) # Wait 2 seconds before hit Twitter API

    time.sleep(600) # Wait 10 minutes before hit Twitter API again