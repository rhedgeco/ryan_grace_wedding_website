import falcon
import json

from backend.database_manager import SqliteDatabase, DatabaseManager
from backend.authenticator import hash_password, get_auth_username_password
from backend.api_utils import validate_params


class Admins:

    def __init__(self, database: SqliteDatabase):
        self.db = DatabaseManager(database)

    def on_get(self, req, resp):
        if not validate_params(req.params, 'token'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Bad parameters.'
            return

        token = req.params['token']
        admin_id = self.db.validate_session(token)
        if not admin_id:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = 'Login Expired.'
            return

        resp.body = admin_id

    def on_post(self, req, resp):
        if not validate_params(req.params, 'add_code'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Bad parameters.'
            return

        admin_id, password = get_auth_username_password(req.auth)
        if not admin_id or not password:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Username and Password not supplied.'
            return

        if self.db.get_admin(admin_id):
            resp.status = falcon.HTTP_CONFLICT
            resp.body = 'Admin ID already exists.'
            return

        add_code = req.params['add_code']
        adding_admin = self.db.get_admin_from_add_code(add_code)
        if not adding_admin:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = 'Invalid add code.'
            return

        self.db.reset_admin_add_code(adding_admin['admin_id'])

        password = hash_password(password)
        self.db.create_admin(admin_id, password)
