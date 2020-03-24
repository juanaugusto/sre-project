import base64
import requests
import urllib.parse


class TwitterAPI:
    """A Client for TwitterAPI usage."""

    def __init__(self, api_key, api_secret_key):
        self.base_url = 'https://api.twitter.com'
        self.bearer_token = self.generate_bearer_token(api_key, api_secret_key)

    def generate_bearer_token(self, api_key, api_secret_key):
        """Takes the api_key and api_secret_key and based 
           in them, generate the Bearer Token using Twitter API.
        """
        url = '%s/oauth2/token' % self.base_url

        api_key = urllib.parse.quote(api_key)
        api_secret_key = urllib.parse.quote(api_secret_key)

        bearer_token_credentials = '%s:%s' % (api_key, api_secret_key)
        bearer_token_credentials_bytes = bearer_token_credentials.encode('ascii')
        base64_bearer_token_credentials_bytes = base64.b64encode(bearer_token_credentials_bytes)
        base64_bearer_token_credentials_message = base64_bearer_token_credentials_bytes.decode('ascii')

        result = requests.post(url,
                               headers={'Authorization':
                                        'Basic %s' % base64_bearer_token_credentials_message,
                                        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8.'},
                               data='grant_type=client_credentials')
        
        result.raise_for_status()

        return result.json()['access_token']

    def search_statuses(self, tag, count):
        """Search statuses by tag and limits the amount of results 
           the Twitter API will return with count parameter.
        """
        querystring = urllib.parse.urlencode({'q': tag, 'count': count})
        url = '%s/1.1/search/tweets.json?%s' % (self.base_url, querystring)
        
        result = requests.get(url, 
                              timeout=2, 
                              headers={'Authorization': 
                                       'Bearer %s' % self.bearer_token})

        result.raise_for_status()

        return result.json()['statuses']
