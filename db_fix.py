from lib import database

following = database.Database(database.Database.BackendFile("twitter_following"))
tweets = []
num_limit = 20
for user_id in following:
    db = database.Database(database.Database.BackendFile(user_id))
    user_tweets = db.get_user_data(user_id)
    for tweet in user_tweets:
        tweet['read'] = True
    db.update_user_data(user_id, user_tweets)
