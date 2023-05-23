from lib import database


def get_tweet_url(tweet_id):
    return f"https://twitter.com/twitter/statuses/{tweet_id}"


def get_user_url(user_id):
    return f"https://twitter.com/intent/user?user_id={user_id}"


def get_highest_value(user_id):
    db = database.Database(database.Database.BackendFile(user_id))
    user_tweets = db.get_user_data(user_id)
    if user_tweets:
        values = [tweet["value"] for tweet in user_tweets]

        highest_value = max(values)
        print(highest_value)
        values.remove(highest_value)

        highest_value = max(values)
        print(highest_value)
        values.remove(highest_value)

        highest_value = max(values)
        print(highest_value)
        values.remove(highest_value)

        return max(values)
    return 0


def get_value_limit(user_id, limit):
    highest_value = get_highest_value(user_id)
    value_limit = int(highest_value * (limit/100))
    print(f"{highest_value} => {value_limit}")
    return value_limit


def get_tweets(user_id, min_value, num):
    db = database.Database(database.Database.BackendFile(user_id))
    tweets = []
    user_tweets = db.get_user_data(user_id)
    if user_tweets:
        for index in range(len(user_tweets) - 1,-1,-1):
            value = user_tweets[index]['value']
            if user_tweets[index]['read'] == False and value >= min_value:
                user_tweets[index]['read'] = True
                print(f"    +++++ {value} Reading tweet {user_tweets[index]}")
                tweets.append(user_tweets[index])
                if len(tweets) == num:
                    break
            elif user_tweets[index]['read'] == False:
                user_tweets[index]['read'] = True
                print(f"    ----- {value} Skipping {user_tweets[index]}")
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
