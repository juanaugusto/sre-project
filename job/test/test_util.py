
import os
import pymongo
import unittest
from util.util import insert_tweet_in_mongo
from util.util import insert_user_in_mongo
from util.util import insert_tweets_in_mongo
from util.util import insert_users_in_mongo
from util.util import find_tweets_by_tweets_ids
from util.util import update_user_in_mongo
from util.util import insert_references_from_users_to_tweets_in_mongo
from util.util import get_users_with_tweets_references
from util.util import insert_in_mongo_by_hashtag


MONGO_ROOT_USERNAME = os.environ['MONGO_ROOT_USERNAME']
MONGO_ROOT_PASSWORD = os.environ['MONGO_ROOT_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']

class TestJobUtil(unittest.TestCase):

    def setUp(self):
        """For each test, ensure that database was dropped before.
        """
        self.mongo_client = pymongo.MongoClient(
                                'mongodb://%s:%s@%s:27017/admin' % 
                                (MONGO_ROOT_USERNAME, 
                                 MONGO_ROOT_PASSWORD, 
                                 MONGO_HOST))
        
        # Ensure also that DB not exists before starting to Test
        self.mongo_client.drop_database('twitterDB')

        # Instantiate collections
        self.tweets_collection = self.mongo_client.twitterDB.tweets
        self.users_collection = self.mongo_client.twitterDB.users
    
    def tearDown(self):
        """After each test, ensure that database was dropped.
        """
        self.mongo_client.drop_database('twitterDB')

    def test_insert_one_tweet_in_mongo(self):
        """Test that can insert one tweet in Mongo."""
        tweet = {
            'tweet_hashtag': '#xpto',
            'tweet_id': 10,
            'tweet_text': 'TT',
            'tweet_hour_created_at': 23,
            'tweet_lang': 'en'
        }
        insert_tweet_in_mongo(tweet, self.tweets_collection)
        tweets = list(self.tweets_collection.find({}))
        self.assertEqual(len(tweets), 1)


    def test_insert_one_user_in_mongo(self):
        """Test that can insert one user in Mongo."""
        user = {
            'user_id': 1,
            'user_name': 'Test',
            'user_followers_count': 999,
            'user_location': 'France',
            'tweets': []
        }
        insert_user_in_mongo(user, self.users_collection)
        users = list(self.users_collection.find({}))
        self.assertEqual(len(users), 1)

    def test_insert_two_tweets_in_mongo(self):
        """Test that can insert multiple tweets in Mongo."""
        tweets = [
            {
                'tweet_hashtag': '#xpto',
                'tweet_id': 10,
                'tweet_text': 'TT',
                'tweet_hour_created_at': 23,
                'tweet_lang': 'en'
            },
            {
                'tweet_hashtag': '#xpto',
                'tweet_id': 11,
                'tweet_text': 'TT1',
                'tweet_hour_created_at': 22,
                'tweet_lang': 'pt'
            }
        ]
        insert_tweets_in_mongo(tweets, self.tweets_collection)
        tweets = list(self.tweets_collection.find({}))
        self.assertEqual(len(tweets), 2)

    def test_insert_two_users_in_mongo(self):
        """Test that can insert multiple users in Mongo."""
        users = [
            {
                'user_id': 1,
                'user_name': 'Test',
                'user_followers_count': 999,
                'user_location': 'France',
                'tweets': []
            },
            {
                'user_id': 2,
                'user_name': 'Test2',
                'user_followers_count': 99,
                'user_location': 'BR',
                'tweets': []
            }        
        ]
        insert_users_in_mongo(users, self.users_collection)
        users = list(self.users_collection.find({}))
        self.assertEqual(len(users), 2)

    def test_update_user_in_mongo(self):
        """Test that an existing user in Mongo can be updated."""
        user = {
            'user_id': 1,
            'user_name': 'Test',
            'user_followers_count': 999,
            'user_location': 'France',
            'tweets': []
        }
        tweet = {
            'tweet_hashtag': '#xpto',
            'tweet_id': 2,
            'tweet_text': 'TT',
            'tweet_hour_created_at': 23,
            'tweet_lang': 'en'
        }
        insert_user_in_mongo(user, self.users_collection)
        insert_tweet_in_mongo(tweet, self.tweets_collection)

        user = list(self.users_collection.find({'user_id': 1}))[0]
        tweet = list(self.tweets_collection.find({'tweet_id': 2}))[0]

        user['tweets'] = [tweet['_id']]

        update_user_in_mongo(user, self.users_collection)
        user = None
        user = list(self.users_collection.find({'user_id': 1}))[0]

        self.assertEqual(user['tweets'], [tweet['_id']])        

    def test_find_tweets_by_tweets_ids(self):
        """Test that can find tweets in Mongo by tweets ids."""
        tweets = [
            {
                'tweet_hashtag': '#xpto',
                'tweet_id': 10,
                'tweet_text': 'TT',
                'tweet_hour_created_at': 23,
                'tweet_lang': 'en'
            },
            {
                'tweet_hashtag': '#xpto',
                'tweet_id': 11,
                'tweet_text': 'TT1',
                'tweet_hour_created_at': 22,
                'tweet_lang': 'pt'
            }
        ]
        insert_tweets_in_mongo(tweets, self.tweets_collection)

        tweets = find_tweets_by_tweets_ids([11],
                                           self.tweets_collection)

        self.assertEqual(len(tweets), 1)

    def test_insert_references_from_users_to_tweets_in_mongo(self):
        """Test that for an already existing user and tweets, 
           can insert references from users to its tweets.
        """
        user = {
            'user_id': 1,
            'user_name': 'Test',
            'user_followers_count': 999,
            'user_location': 'France',
            'tweets': []
        }
        tweet = {
            'tweet_hashtag': '#xpto',
            'tweet_id': 2,
            'tweet_text': 'TT',
            'tweet_hour_created_at': 23,
            'tweet_lang': 'en'
        }
        insert_user_in_mongo(user, self.users_collection)
        insert_tweet_in_mongo(tweet, self.tweets_collection)  

        references = {1: [2]}
        
        insert_references_from_users_to_tweets_in_mongo(
            references,
            self.tweets_collection,
            self.users_collection
        )

        user = list(self.users_collection.find({'user_id': 1}))[0]
        tweet = list(self.tweets_collection.find({'tweet_id': 2}))[0]

        self.assertEqual(user['tweets'], [tweet['_id']])

    def test_get_users_with_tweets_references(self):
        """Test given statuses, can obtain the references from users to its tweets"""

        # In {'user': {'id': 1}, 'id': 3},
        # 3 is the id of tweet and
        # 1 is the id of user
        self.assertEqual(
            get_users_with_tweets_references([{'user': {'id': 1}, 'id': 3},
                                              {'user': {'id': 2}, 'id': 4} 
                                              {'user': {'id': 1}, 'id': 2}]),
            {1: [3, 2], 2: [4]}
        )

    def test_cannot_associate_same_tweet_more_than_once_to_user(self):
        """Test when try to insert an already existing tweet,
           that will not be created a duplicated reference to tweets
           from the user.
        """
        status = {
            'user': {
                'id': 2,
                'name': 'test',
                'followers_count': 3,
                'location': 'BR' 
            },
            'id': 1,
            'text': 'Tweet text',
            'created_at': 'Fri Feb 06 10:17:18 +0000 2015',
            'lang': 'pt'
        }

        insert_in_mongo_by_hashtag([status], 
                                   '#test',
                                   self.tweets_collection,
                                   self.users_collection)
        insert_in_mongo_by_hashtag([status], 
                                   '#test',
                                   self.tweets_collection,
                                   self.users_collection)

        user = list(self.users_collection.find({'user_id': 2}))[0]
        
        self.assertEqual(
            len(user['tweets']),
            1
        )
