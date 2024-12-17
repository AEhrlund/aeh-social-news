import datetime
import tweepy  # type:ignore
import pytz  # type:ignore
import lib.secret

class TwitterAPI:
    def __init__(self, client: tweepy.Client) -> None:
        self._utc = pytz.UTC
        self._client: tweepy.Client = client

    @staticmethod
    def get_client() -> tweepy.Client:
        twitter_secret = lib.secret.get_secret()
        print(twitter_secret)
        return tweepy.Client(bearer_token=twitter_secret["bearer_token"])

    def get_my_user_id(self) -> int:
        data, _, _, _ = self._client.get_me()
        return data.id

    def get_following(self, user_id: int) -> list[dict]:
        data, _, _, _ = self._client.get_users_following(user_id)
        following = []
        for user in data:
            following.append({"id": user.id, "name": user.name, "username": user.username})
        return following

    def get_tweets(self, user_id: int, start_time: datetime.datetime, end_time: datetime.datetime) -> list[dict]:
        start_time_ = datetime.datetime(
            year=start_time.year,
            month=start_time.month,
            day=start_time.day,
            hour=0,
            minute=0,
        )
        end_time_ = datetime.datetime(
            year=end_time.year,
            month=end_time.month,
            day=end_time.day,
            hour=23,
            minute=59,
        )
        tweets_out = []
        if end_time_.date() > start_time_.date():
            tweet_fields = [
                "created_at",
                "source",
                "referenced_tweets",
                "public_metrics",
                "in_reply_to_user_id",
                "conversation_id",
                "attachments",
            ]
            tweets, _, _, meta = self._client.get_users_tweets(
                user_id,
                exclude="replies",
                start_time=start_time_,
                end_time=end_time_,
                max_results=100,
                tweet_fields=tweet_fields,
            )
            while "next_token" in meta:
                more_tweets, _, _, meta = self._client.get_users_tweets(
                    user_id,
                    exclude="replies",
                    start_time=start_time_,
                    end_time=end_time_,
                    max_results=100,
                    tweet_fields=tweet_fields,
                    pagination_token=meta["next_token"],
                )
                if more_tweets:
                    tweets += more_tweets
            if not tweets:
                tweets = []
            for tweet in tweets:
                tweets_out.append(
                    {
                        "tweet_id": tweet.id,
                        "value": self._calculate_value(tweet.public_metrics),
                        "date": tweet.created_at.isoformat(),
                        "read": False,
                    }
                )
        return tweets_out

    def _calculate_value(self, public_metrics: dict) -> int:
        value = (
            (public_metrics["retweet_count"] * 10)
            + (public_metrics["reply_count"] * 2)
            + (public_metrics["like_count"] * 1)
            + (public_metrics["quote_count"] * 4)
            + (public_metrics["impression_count"] * 1)
        )
        return value

    # def get_tweets(self, user_id, end_date, tweets):
    #   if user_id not in self._json_data.keys():
    #     self._json_data[user_id] = { "tweets": [] }
    #   self._json_data[user_id]["end_date"] = end_date.strftime("%Y-%m-%d")
    #   self._json_data[user_id]["tweets"] = self._json_data[user_id]["tweets"] + tweets

    # def get_updates(self, user_id, start_time, end_time):
    #   return self.get_tweets(user_id, start_time, end_time)

    # def get_end_date(self, user: str) -> datetime.datetime:
    #   user_data = self.get_user(user)
    #   if user_data:
    #     return datetime.datetime.strptime(user_data["end_date"], "%Y-%m-%d")
    #   return None

    # START_WEEKS = datetime.timedelta(weeks=10)
    #   return datetime.datetime.now() - self.START_WEEKS


#  + datetime.timedelta(days=1)
