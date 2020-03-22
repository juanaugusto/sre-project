import httpretty
import json
import unittest
import urllib.parse
from ..clients.twitterapi import TwitterAPI
from unittest.mock import MagicMock
from requests.exceptions import HTTPError
from requests.exceptions import ConnectTimeout


class TestTwitterAPI(unittest.TestCase):
    def setUp(self):
        self.bearer_token = 'AAAAA'
        self.twitter_client = TwitterAPI(self.bearer_token)

    @httpretty.activate
    def test_twitter_api_when_it_return_200(self):
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
            self.twitter_client.search_tweets(tag, count),
            json.loads(twitterapi_json_return)['statuses']
        )

    @httpretty.activate
    def test_twitter_api_when_it_not_return_200(self):
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
                          self.twitter_client.search_tweets,
                          tag, count)
    

if __name__ == '__main__':
    unittest.main()