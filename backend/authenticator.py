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
        if not validate_params(req.params, 'admin_id', 'password'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = "Bad parameters."
            return

        admin_id = req.params['admin_id']
        password = req.params['password']
        token = self._create_token(admin_id=admin_id, password=password)
        if not token:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = "Invalid admin_id or password."

        resp.status = falcon.HTTP_OK
        resp.body = token

    # Hashing algorithms from https://www.pythoncentral.io/hashing-strings-with-python/

    def _create_token(self, admin_id: str, password: str):
        user = self.db.get_admin(admin_id)
        if not check_password(user['password'], password):
            return None
        self.db.update_user_access(admin_id)
        cred = {
            'admin_id': admin_id,
            'password': hash_password(password),
            'last_access_expire': uptime
        }
        return jwt.encode(cred, secret_key, algorithm='HS256')


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def validate_token_expire(manager: DatabaseManager, token: str):
    try:
        cred = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return None

    admin_id = cred['admin_id']
    last_access_expire = cred['last_access_expire']
    if not manager.validate_user_expire(admin_id, last_access_expire):
        return None

    return admin_id