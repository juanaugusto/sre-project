import httpretty
import json
import unittest
import urllib.parse
from clients.twitterapi import TwitterAPI
from unittest.mock import MagicMock
from requests.exceptions import HTTPError
from requests.exceptions import ConnectTimeout


class TestTwitterAPI(unittest.TestCase):
    
    @httpretty.activate
    def setUp(self):        
        httpretty.register_uri(
            httpretty.POST,
            'https://api.twitter.com/oauth2/token',
            body='{"token_type":"bearer","access_token": "AAAA"}',           
            status=200
        )

        self.api_key = 'xpto1'
        self.api_secret_key = 'xpto2'
        self.twitter_client = TwitterAPI(self.api_key, self.api_secret_key)

    def tearDown(self):
        httpretty.reset()

    @httpretty.activate
    def test_twitter_api_search_statuses_when_it_return_200(self):
        tag = '#xpto'
        count = 1
        querystring = urllib.parse.urlencode({'q': tag, 'count': count})

        with open('/app/test/fixtures/twitterapi.json') as file_:
            twitterapi_json_return = file_.read()

        httpretty.register_uri(
            httpretty.GET,
            'https://api.twitter.com/1.1/search/tweets.json?%s' % querystring,
            body=twitterapi_json_return,
            status=200
        )

        self.assertEqual(
            self.twitter_client.search_statuses(tag, count),
            json.loads(twitterapi_json_return)['statuses']
        )

    @httpretty.activate
    def test_twitter_api_search_statuses_when_it_not_return_200(self):
        tag = '#xpto2'
        count = 1
        querystring = urllib.parse.urlencode({'q': tag, 'count': count})

        httpretty.register_uri(
            httpretty.GET,
            'https://api.twitter.com/1.1/search/tweets.json?%s' % querystring,
            body='{"errors":[{"code":89,"message":"Invalid or expired token."}]}',
            status=401
        )

        self.assertRaises(HTTPError,
                          self.twitter_client.search_statuses,
                          tag, count)

    @httpretty.activate
    def test_generate_bearer_token_when_it_return_200(self):
        httpretty.reset()

        httpretty.register_uri(
            httpretty.POST,
            'https://api.twitter.com/oauth2/token',
            body='{"token_type":"bearer","access_token": "AAAABBB"}',           
            status=200
        )

        self.assertEqual(
            self.twitter_client.generate_bearer_token(self.api_key, self.api_secret_key),
            'AAAABBB'
        )
  
    @httpretty.activate
    def test_generate_bearer_token_when_it_not_return_200(self):
        httpretty.reset()

        httpretty.register_uri(
            httpretty.POST,
            'https://api.twitter.com/oauth2/token',
            body='{"errors":[{"code":99,"message":"Unable to verify your credentials","label":"authenticity_token_error"}]}',
            status=403
        )

        self.assertRaises(HTTPError,
                          self.twitter_client.generate_bearer_token,
                          self.api_key, 
                          self.api_secret_key
        )
    
