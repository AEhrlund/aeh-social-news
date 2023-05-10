import os
from twitter import twitter_api
from lib import database


def get_current_following():
    files = os.listdir("data")
    following = []
    for file in files:
        user_id = file[:-5]
        if user_id.isnumeric():
            following.append(int(user_id))
    return following


def remove_following(users, db):
    for user_id in users:
        print(f"Removing user {user_id}")
        db.remove(user_id)
        os.remove(f"data/{user_id}.json")       


def update_following():
    removed_following = get_current_following()
    db = database.Database(database.Database.BackendFile("twitter_following"))
    twitter = twitter_api.TwitterAPI(twitter_api.TwitterAPI.get_client())
    following = twitter.get_following(twitter.get_my_user_id())
    for user in following:
        user_id = user["id"]
        if user_id in removed_following:
            removed_following.remove(user_id)
        user_data = db.get_user_data(user_id)
        if not user_data:
            name = user["name"]
            print(f"Adding new user: {name}")
            user_data = {
                "limit": 70,
                "name": name,
                "username": user["username"],
            }
            db.update_user_data(user_id, user_data)
    remove_following(removed_following, db)

if __name__ == "__main__":
    update_following()
