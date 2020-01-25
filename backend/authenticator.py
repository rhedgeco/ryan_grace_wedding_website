import base64

import falcon
import jwt
import hashlib
import uuid

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase
from backend.database_manager import DatabaseManager
from backend.api_utils import validate_params
from enum import Enum

secret_key = 'DoPe_WeDdInG_kEy'
uptime = 5


class TokenValidationType(Enum):
    ACCEPTED = 0
    EXPIRED = 1
    BAD_TOKEN = 2


class Auth:

    def __init__(self, database: SqliteDatabase):
        self.db = DatabaseManager(database)

    def on_get(self, req, resp):
        admin_id, password = get_auth_username_password(req.auth)
        if admin_id == '' or password == '':
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Username and Password not supplied.'
            return

        token = self._create_token(admin_id, password)
        if not token:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = "Invalid Admin ID or password."
            return

        resp.status = falcon.HTTP_OK
        resp.body = token

    # Hashing algorithms from https://www.pythoncentral.io/hashing-strings-with-python/

    def _create_token(self, admin_id: str, password: str):
        user = self.db.get_admin(admin_id)
        if not user:
            return None
        if not check_password(user['password'], password):
            return None
        return self.db.start_session(admin_id)


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def get_auth_username_password(auth):
    if not auth:
        return '', ''
    auth_parts = auth.split(" ")
    if len(auth_parts) < 2:
        return '', ''
    auth_type, token = auth_parts
    if auth_type != "Basic":
        return '', ''
    token = base64.b64decode(token).decode("utf-8")

    token_parts = token.split(":")
    if len(token_parts) < 2:
        return '', ''
    return token_parts
