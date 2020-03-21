import requests
import urllib.parse


class TwitterAPI:

    def __init__(self, bearer_token):
        self.base_url = 'https://api.twitter.com/1.1'
        self.bearer_token = bearer_token

    def search_tweets(self, tag):
        querystring = urllib.parse.urlencode({'q': tag})
        search_path = '/search/tweets.json?%s' % querystring
        url = '%s%s' % (self.base_url, search_path)
        
        result = requests.get(url, 
                              timeout=2, 
                              headers={'Authorization': 
                                       'Bearer %s' % self.bearer_token})

        result.raise_for_status()

        return result.json()['statuses']
