import datetime
from lib import database
from twitter import twitter_api

def twitter_update():
    following = database.Database(database.Database.BackendFile("twitter_following"))
    twitter = twitter_api.TwitterAPI(twitter_api.TwitterAPI.get_client())
    start_time_new_user = datetime.datetime.now() - datetime.timedelta(days=120)
    end_time = datetime.datetime.now() - datetime.timedelta(days=10)
    for user in following:
        user_data = following.get_user_data(user)
        db = database.Database(database.Database.BackendFile(user))
        user_tweets = db.get_user_data(user)
        if not user_tweets:
            print(f"Update new user: {user_data['name']}")
            start_time = start_time_new_user
            user_tweets = []
        else:
            print(f"Update user: {user_data['name']}")
            start_time = datetime.datetime.fromisoformat(user_tweets[0]["date"])
            start_time += datetime.timedelta(days=1)
        new_tweets = twitter.get_tweets(user, start_time, end_time)
        print(f"   adding {len(new_tweets)} tweets")
        user_tweets = new_tweets + user_tweets
        db.update_user_data(user, user_tweets)

if __name__ == "__main__":
    twitter_update()
