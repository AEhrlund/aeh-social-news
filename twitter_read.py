from lib import database


def get_tweet_url(tweet_id):
    return f"https://twitter.com/twitter/statuses/{tweet_id}"


def get_user_url(user_id):
    return f"https://twitter.com/intent/user?user_id={user_id}"


def get_value_limit(user_id, limit):
    db = database.Database(database.Database.BackendFile(user_id))
    user_tweets = db.get_user_data(user_id)
    num = len(user_tweets)
    if num > 0:
        index = num -1
        tot_values = 0
        while index >= 0:
            value = user_tweets[index]['value']
            tot_values += value
            index -= 1
        return int((tot_values / num) * (limit/100))
    return 0


def get_tweets(user_id, min_value, num):
    db = database.Database(database.Database.BackendFile(user_id))
    user_tweets = db.get_user_data(user_id)
    index = len(user_tweets) - 1
    tweets = []
    while index >= 0 and len(tweets) < num:
        index -= 1
        tweet = user_tweets[index]
        if tweet['read'] == False and tweet['value'] >= min_value:
            print(f"    +++++ Reading tweet {tweet}")
            tweets.append(tweet)
        elif tweet['read'] == False:
            print(f"    ----- Skipping {tweet}")
        user_tweets[index]['read'] = True
    db.update_user_data(user_id, user_tweets)
    return tweets


def create_web_page(tweets):   
    with open('tweets.html', 'w') as f:
        f.write('<html>\n<head>\n<body>\n')
        for tweet in tweets:
            f.write('    <blockquote class="twitter-tweet">\n')
            f.write(f'        <a href="https://twitter.com/x/status/{tweet["tweet_id"]}"></a>\n')
            f.write('    </blockquote>\n')
            f.write('    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n')
        f.write('</body>\n</head>\n</html>\n')


def get_tweets_to_read():
    following = database.Database(database.Database.BackendFile("twitter_following"))
    tweets = []
    num_limit = 20
    for user_id in following:
        user = following.get_user(user_id)
        print(user)
        limit = user['limit']
        min_value = get_value_limit(user_id, limit)
        tweets += get_tweets(user_id, min_value, 4)
        if len(tweets) > num_limit:
            return tweets
    print(f"{len(tweets)} tweets to read!")
    return tweets


tweets = get_tweets_to_read()
create_web_page(tweets)
