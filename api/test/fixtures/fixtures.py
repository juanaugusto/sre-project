from bson import ObjectId


def get_tweets():
    return [
        {
            '_id': ObjectId('37c3d8106374d8dc40973f6d'),
            'tweet_hashtag': '#B',
            'tweet_id': 1,
            'tweet_text': 'Text1',
            'tweet_hour_created_at': 23,
            'tweet_lang': 'en'
        },
        {
            '_id': ObjectId('33e1b43f93df3a541f73ac04'),
            'tweet_hashtag': '#B',
            'tweet_id': 2,
            'tweet_text': 'Text2',
            'tweet_hour_created_at': 2,
            'tweet_lang': 'pt'
        },
        {
            '_id': ObjectId('0ff641ae5daf127d5052f29e'),
            'tweet_hashtag': '#C',
            'tweet_id': 3,
            'tweet_text': 'Text3',
            'tweet_hour_created_at': 4,
            'tweet_lang': 'fr'
        },
        {
            '_id': ObjectId('33f350eabb52ad9cf63b9e8c'),
            'tweet_hashtag': '#D',
            'tweet_id': 4,
            'tweet_text': 'Text4',
            'tweet_hour_created_at': 11,
            'tweet_lang': 'en'
        },
        {
            '_id': ObjectId('822e777fb8f4e0205c71c678'),
            'tweet_hashtag': '#D',
            'tweet_id': 5,
            'tweet_text': 'Text5',
            'tweet_hour_created_at': 7,
            'tweet_lang': 'en'
        },
        {
            '_id': ObjectId('a1ee8ca9b8ac3d4e738c0790'),
            'tweet_hashtag': '#E',
            'tweet_id': 6,
            'tweet_text': 'Text6',
            'tweet_hour_created_at': 5,
            'tweet_lang': 'it'
        },
        {
            '_id': ObjectId('7952a85a8a14b49d5c58f55a'),
            'tweet_hashtag': '#A',
            'tweet_id': 7,
            'tweet_text': 'Text7',
            'tweet_hour_created_at': 5,
            'tweet_lang': 'es'
        },
        {
            '_id': ObjectId('752b3e745f3ed26f0d01f076'),
            'tweet_hashtag': '#A',
            'tweet_id': 8,
            'tweet_text': 'Text8',
            'tweet_hour_created_at': 5,
            'tweet_lang': 'it'
        },
        {
            '_id': ObjectId('0f679e723f07940785d770f5'),
            'tweet_hashtag': '#A',
            'tweet_id': 9,
            'tweet_text': 'Text9',
            'tweet_hour_created_at': 3,
            'tweet_lang': 'pt'
        },
        {
            '_id': ObjectId('83506615e486d2f4b3c81fb7'),
            'tweet_hashtag': '#G',
            'tweet_id': 10,
            'tweet_text': 'Text10',
            'tweet_hour_created_at': 20,
            'tweet_lang': 'it'
        }
    ]


def get_users():
    return [
        {
            '_id': ObjectId('aca2ff5cd3e22177d97e1dc1'),
            'user_id': 10,
            'user_name': 'Test1',
            'user_followers_count': 5,
            'user_location': 'France',
            'tweets': [ObjectId('37c3d8106374d8dc40973f6d'), ObjectId('33e1b43f93df3a541f73ac04'), ObjectId('0ff641ae5daf127d5052f29e'), ObjectId('33f350eabb52ad9cf63b9e8c'), ObjectId('822e777fb8f4e0205c71c678')]
        },
        {
            '_id': ObjectId('ddf7ca2c0a3a25f53b99b340'),
            'user_id': 11,
            'user_name': 'Test2',
            'user_followers_count': 999,
            'user_location': 'US',
            'tweets': [ObjectId('a1ee8ca9b8ac3d4e738c0790')]
        },
        {
            '_id': ObjectId('9a5c6269350daabeb53f377f'),
            'user_id': 12,
            'user_name': 'Test3',
            'user_followers_count': 50,
            'user_location': 'BR',
            'tweets': [ObjectId('7952a85a8a14b49d5c58f55a')]
        },
        {
            '_id': ObjectId('10cf2276a2b5a06c423c5f26'),
            'user_id': 13,
            'user_name': 'Test4',
            'user_followers_count': 99,
            'user_location': 'FR',
            'tweets': [ObjectId('752b3e745f3ed26f0d01f076')]
        },
        {
            '_id': ObjectId('4e30693dd1d1ac2870f27c2d'),
            'user_id': 14,
            'user_name': 'Test5',
            'user_followers_count': 700,
            'user_location': 'ES',
            'tweets': [ObjectId('0f679e723f07940785d770f5')]
        },
        {
            '_id': ObjectId('99236f34e2d977b6687bff79'),
            'user_id': 15,
            'user_name': 'Test6',
            'user_followers_count': 2,
            'user_location': 'BR',
            'tweets': [ObjectId('83506615e486d2f4b3c81fb7')]
        }
    ]
