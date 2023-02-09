import base64
import hashlib
import hmac

from dao.user import UserDAO
from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_user_by_id(self, uid):
        return self.dao.get_user_by_id(uid)

    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)

        return base64.b32encode(hash_digest)

    def compare_password(self, hash_pass, password):
        decode_digest = base64.b32decode(hash_pass)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)

        return hmac.compare_digest(decode_digest, hash_digest)

    def create(self, user_data):
        user_data['password'] = self.get_hash(user_data['password'])
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data['password'] = self.get_hash(user_data['password'])

        return self.dao.update(user_data)

    def delete(self, uid):
        self.dao.delete(uid)
