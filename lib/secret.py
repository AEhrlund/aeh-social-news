import os
import json
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_FILE = "secret/salt"
SECRET_FILE = "secret/secret"

def _get_salt():
  if os.path.isfile(SALT_FILE):
    with open(SALT_FILE, "rb") as file:
      salt = file.read()
  else:
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as file:
      file.write(salt)
  return salt


def _get_fernet():
  salt = _get_salt()
  kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
  key = base64.urlsafe_b64encode(kdf.derive(getpass.getpass().encode()))
  return Fernet(key)


blaj = _get_fernet()

def _decrypt_json(enc_data):
  json_str = blaj.decrypt(enc_data).decode()
  return json.loads(json_str)


def _encrypt_json(json_data):
  json_str = json.dumps(json_data)
  return blaj.encrypt(json_str.encode())


def dump_secret(user_secret):
  enc = _encrypt_json(user_secret)
  with open(SECRET_FILE, "wb") as f:
    f.write(enc)


def get_secret():
  with open(SECRET_FILE, "rb") as f:
    enc = f.read()
  return _decrypt_json(enc)
