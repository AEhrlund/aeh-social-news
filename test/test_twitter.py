import os
import sys
import datetime

sys.path.insert(0, f"{os.path.dirname(os.path.realpath(__file__))}/..")
from twitter import twitter_api  # pylint: disable=wrong-import-position


class MockUser:  # pylint: disable=too-few-public-methods
    id = None
    name = None
    username = None

    def __init__(self, user_id, name, username):
        self.id = user_id  # pylint: disable=invalid-name
        self.name = name
        self.username = username


class MockTweet:  # pylint: disable=too-few-public-methods
    id = None
    text = None
    created_at = None
    public_metrics = None

    def __init__(self, tweet_id, text, created_at, public_metrics):
        self.id = tweet_id  # pylint: disable=invalid-name
        self.text = text
        self.created_at = created_at
        self.public_metrics = public_metrics


class MockClientSimple:
    def get_me(self):
        return (MockUser(123, "name", "username"), None, None, None)

    def get_users_following(self, user_id):  # pylint: disable=unused-argument
        return ([MockUser(123, "name", "username")], None, None, None)

    def get_users_tweets(
        self, user_id, exclude, start_time, end_time, max_results, tweet_fields
    ):  # pylint: disable=unused-argument,too-many-arguments
        return ([], None, None, {})


class MockClient:  # pylint: disable=too-few-public-methods
    mock_tweets: list = []

    def __init__(self):
        now = datetime.datetime.now()
        public_metrics = {
            "retweet_count": 3,
            "reply_count": 30,
            "like_count": 300,
            "quote_count": 3000,
            "impression_count": 30000,
        }
        self.mock_tweets.append(MockTweet(1, "text 1", now, public_metrics))
        self.mock_tweets.append(MockTweet(2, "text 2", now - datetime.timedelta(days=1), public_metrics))
        self.mock_tweets.append(MockTweet(3, "text 3", now - datetime.timedelta(days=2), public_metrics))

    def get_users_tweets(
        self, user_id, exclude, start_time, end_time, max_results, tweet_fields
    ):  # pylint: disable=unused-argument,too-many-arguments
        tweets = []
        for tweet in self.mock_tweets:
            if tweet.created_at >= start_time and tweet.created_at <= end_time:
                tweets.append(tweet)
        return (tweets, None, None, {})


def test_get_my_user_id():
    twitter = twitter_api.TwitterAPI(MockClientSimple())
    user_id = twitter.get_my_user_id()
    assert user_id == 123


def test_get_following():
    twitter = twitter_api.TwitterAPI(MockClientSimple())
    following = twitter.get_following(123)
    assert len(following) == 1
    assert following[0]["id"] == 123
    assert following[0]["name"] == "name"
    assert following[0]["username"] == "username"


def test_get_tweets():
    twitter = twitter_api.TwitterAPI(MockClient())
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=1)
    tweets = twitter.get_tweets(1, start_time, end_time)
    assert len(tweets) == 2


def test_get_tweets_no_tweets():
    twitter = twitter_api.TwitterAPI(MockClient())
    end_time = datetime.datetime.now() - datetime.timedelta(days=3)
    start_time = end_time - datetime.timedelta(days=1)
    tweets = twitter.get_tweets(1, start_time, end_time)
    assert len(tweets) == 0
