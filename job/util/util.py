import bson
import os
import pymongo
import time
from clients.twitterapi import TwitterAPI
from dateutil.parser import parse


def insert_tweet_in_mongo(tweet, 
                          tweets_collection):
    if tweets_collection.find_one({'tweet_id': tweet['tweet_id']}) is None:
        tweets_collection.insert_one(tweet)


def insert_user_in_mongo(user,
                         users_collection):
    if users_collection.find_one({'user_id': user['user_id']}) is None:
        users_collection.insert_one(user)


def insert_tweets_in_mongo(tweets, 
                           tweets_collection):
    for tweet in tweets:
        insert_tweet_in_mongo(tweet, tweets_collection)


def insert_users_in_mongo(users, 
                          users_collection):
    for user in users:
        insert_user_in_mongo(user, users_collection)


def insert_in_mongo_by_hashtag(tweets, 
                               hashtag,
                               tweets_collection,
                               users_collection):
    users = [{'user_id': tweet['user']['id'],
              'user_name': tweet['user']['name'],
              'user_followers_count': tweet['user']['followers_count'],
              'user_location': tweet['user']['location'],
              'tweets': []}
             for tweet in tweets]

    tweets = [{'tweet_hashtag': hashtag,
               'tweet_id': tweet['id'],
               'tweet_text': tweet['text'],
               'tweet_hour_created_at': parse(tweet['created_at']).hour,
               'tweet_lang': tweet['lang']}
             for tweet in tweets]

    insert_users_in_mongo(users, 
                          users_collection)
    insert_tweets_in_mongo(tweets, 
                           tweets_collection)
    # make_references_from_users_to_its_tweets()


def insert_in_mongo_by_hashtags(hashtags,
                                twitter_api,
                                tweets_collection,
                                users_collection):
    for hashtag in hashtags:
        tweets = twitter_api.search_tweets(hashtag, 100)
        insert_in_mongo_by_hashtag(tweets, 
                                   hashtag, 
                                   tweets_collection, 
                                   users_collection)
