
from app import app
from test.fixtures.fixtures import get_tweets
from test.fixtures.fixtures import get_users
from unittest.mock import patch
import pymongo
import os
import unittest


MONGO_ROOT_USERNAME = os.environ['MONGO_ROOT_USERNAME']
MONGO_ROOT_PASSWORD = os.environ['MONGO_ROOT_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']

class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs only in the beginning of this TestSuite
        """
        cls.api_app = app.test_client()
        cls.mongo_client = pymongo.MongoClient(
            'mongodb://%s:%s@%s:27017/admin' % 
            (MONGO_ROOT_USERNAME, 
            MONGO_ROOT_PASSWORD, 
            MONGO_HOST))
        
        # Ensure also that DB not exists before starting to Test
        cls.mongo_client.drop_database('twitterDB')

        cls.tweets_collection = cls.mongo_client.twitterDB.tweets
        cls.users_collection = cls.mongo_client.twitterDB.users

        # Populate DB with users and tweets
        cls.tweets_collection.insert(get_tweets())
        cls.users_collection.insert(get_users())

    @classmethod
    def tearDownClass(cls):
        """Runs only after the completion of this TestSuite
        """
        cls.mongo_client.drop_database('twitterDB')

    @patch('app.logging')
    def test_it_gives_404_in_route_that_does_not_exists(cls, mock):
        """Test non existing route returns always 404."""
        response = cls.api_app.get('/anything')
        cls.assertEqual(response.status_code, 404)

    @patch('app.logging')
    def test_what_users_with_most_followers(cls, mock):
        """Test route that informs the 5 users with most followers."""
        response = cls.api_app.get('/what/users/most/followers')

        with open('/app/test/fixtures/test_what_users_with_most_followers.json') as file_:
            api_json_return = file_.read()
        
        cls.assertEqual(response.data.decode('utf-8'),
                        api_json_return)

    @patch('app.logging')
    def test_total_tweets_per_hour(cls, mock):
        """Test route that informs the total of tweets per hour of day."""
        response = cls.api_app.get('/total/tweets/hour')
        
        with open('/app/test/fixtures/test_total_tweets_per_hour.json') as file_:
            api_json_return = file_.read()
        
        cls.assertEqual(response.data.decode('utf-8'),
                        api_json_return)

    @patch('app.logging')
    def test_total_tweets_per_hashtag_and_language_location_for_user_with_one_tweet(cls, mock):
        """Test route that informs total of tweets per hashtag 
           and language location for a user with one tweet.
        """
        response = cls.api_app.get('/total/tweets/hashtag/language/location/14')

        with open('/app/test/fixtures/test_total_tweets_per_hashtag_and_language_location_for_user_with_one_tweet.json') as file_:
            api_json_return = file_.read()
        
        cls.assertEqual(response.data.decode('utf-8'),
                        api_json_return)

    @patch('app.logging')
    def test_total_tweets_per_hashtag_and_language_location_for_user_with_many_tweets(cls, mock):
        """Test route that informs total of tweets per hashtag 
           and language location for a user with many tweets.
        """
        response = cls.api_app.get('/total/tweets/hashtag/language/location/10')

        with open('/app/test/fixtures/test_total_tweets_per_hashtag_and_language_location_for_user_with_many_tweets.json') as file_:
            api_json_return = file_.read()
        
        cls.assertEqual(response.data.decode('utf-8'),
                        api_json_return)

    @patch('app.logging')
    def test_total_tweets_per_hashtag_and_language_location_for_non_existent_user(cls, mock):
        """Test route that informs total of tweets per hashtag 
           and language location for a non existing user returns error.
        """
        response = cls.api_app.get('/total/tweets/hashtag/language/location/100')
        cls.assertEqual(response.status_code, 500)








