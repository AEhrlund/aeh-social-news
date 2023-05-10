import lib.secret


def get_secret():
    return lib.secret.get_secret()


def write_new_secret():
    secret = {
        "bearer_token": "",
        "consumer_key": "",
        "consumer_secret": "",
        "access_token": "",
        "access_token_secret": "",
    }
    lib.secret.dump_secret(secret)


if __name__ == "__main__":
    if False:
        write_new_secret()
    else:
        secret = get_secret()
        print(secret)
    