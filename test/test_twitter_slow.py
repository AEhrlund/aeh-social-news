import os
import sys
import datetime

sys.path.insert(0, f"{os.path.dirname(os.path.realpath(__file__))}/..")
from twitter import twitter_api  # pylint: disable=wrong-import-position


def test_get_tweets():
    twitter = twitter_api.TwitterAPI(twitter_api.TwitterAPI.get_client())
    end_time = datetime.datetime(year=2023, month=2, day=28)
    start_time = end_time - datetime.timedelta(days=20)
    user = 1351906066519490562
    tweets = twitter.get_tweets(user, start_time, end_time)
    assert len(tweets) == 192
