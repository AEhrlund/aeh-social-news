import os
import sys

sys.path.insert(0, f"{os.path.dirname(os.path.realpath(__file__))}/..")
from lib import database  # pylint: disable=wrong-import-position


def test_missing_user():
    test_db = database.Database(database.Database.Backend({}))
    user = "123"
    user_data = test_db.get_user_data(user)
    assert user_data is None


def test_get_user():
    user = 123
    user_data = {
        "hej": "blaj",
    }
    json_data = {str(user): user_data}
    test_db = database.Database(database.Database.Backend(json_data))
    for asd in test_db:
        print(asd)
    user_data_got = test_db.get_user_data(user)
    assert user_data_got == user_data


def test_update_user():
    user = 123
    user_data = {
        "hej": "blaj",
    }
    json_data = {str(user): user_data}
    test_db = database.Database(database.Database.Backend(json_data))
    user_data_got = test_db.get_user_data(user)
    assert user_data_got == user_data
    user_data = {
        "hej": "xxxx",
    }
    test_db.update_user_data(user, user_data)
    user_data_got = test_db.get_user_data(user)
    assert user_data_got == user_data
