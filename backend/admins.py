import falcon
import json

from backend.database_manager import SqliteDatabase, DatabaseManager
from backend.authenticator import hash_password, validate_token_expire, TokenValidationType
from backend.api_utils import validate_params


class Admins:

    def __init__(self, database: SqliteDatabase):
        self.db = DatabaseManager(database)

    def on_get(self, req, resp):
        if not validate_params(req.params, 'authToken'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Bad parameters.'
            return

        token = req.params['authToken']
        user = validate_token_expire(self.db, token)

        if user == TokenValidationType.BAD_TOKEN:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = 'Bad Token.'
            return

        if user == TokenValidationType.EXPIRED:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = 'Login expired.'
            return

        resp.status = falcon.HTTP_OK
        resp.body = user

    def on_post(self, req, resp):
        if not validate_params(req.params, 'email', 'admin_id', 'password', 'add_code'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Bad parameters.'
            return

        admin_id = req.params['admin_id']
        if self.db.get_admin(admin_id) != 'null':
            resp.status = falcon.HTTP_CONFLICT
            resp.body = 'Admin ID already exists.'
            return

        add_code = req.params['add_code']
        adding_admin = self.db.get_admin_from_add_code(add_code)
        if adding_admin == 'null':
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = 'Invalid add code.'
            return

        self.db.reset_admin_add_code(adding_admin['admin_id'])

        email = req.params['email']
        password = hash_password(req.params['password'])
        self.db.create_admin(email, admin_id, password)
