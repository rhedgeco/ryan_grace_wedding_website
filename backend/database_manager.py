import random
import string
import uuid
import datetime

from datetime import datetime as dt

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase

TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
TIME_EXPIRE = 600
ADD_CODE_LENGTH = 8


class DatabaseManager:

    def __init__(self, database: SqliteDatabase):
        self.db = database

    def get_admin(self, admin_id: str):
        return self.db.fetchone_query(f"SELECT * FROM admins WHERE admin_id='{admin_id}'")

    def create_admin(self, admin_id: str, password: str):
        self.db.send_query(f"INSERT INTO admins(admin_id, password) "
                           f"VALUES ('{admin_id}', '{password}')")
        self.reset_admin_add_code(admin_id)

    def get_admin_from_add_code(self, add_code: str):
        return self.db.fetchone_query(f"SELECT * FROM admins WHERE add_code='{add_code}'")

    def reset_admin_add_code(self, admin_id: str):
        add_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                           for _ in range(ADD_CODE_LENGTH))
        self.db.send_query(f"UPDATE admins SET add_code = '{add_code}' WHERE admin_id = '{admin_id}'")

    def update_user_access(self, admin_id: str):
        self.db.send_query(f"UPDATE admins SET access_expire = '{(dt.now()).strftime(TIME_FORMAT)}' "
                           f"WHERE admin_id = '{admin_id}'")

    def start_session(self, admin_id: str):
        token = uuid.uuid4().hex
        self.db.send_query(f"REPLACE INTO sessions(token, admin_id, expire) "
                           f"VALUES ('{token}', '{admin_id}', "
                           f"'{(dt.now() + datetime.timedelta(0,TIME_EXPIRE)).strftime(TIME_FORMAT)}')")
        return token

    def validate_session(self, token: str):
        session = self.db.fetchone_query(f"SELECT * FROM sessions WHERE token = '{token}'")
        if not session:
            return None
        time = dt.strptime(session['expire'], TIME_FORMAT)
        if time < dt.now():
            return None
        else:
            return session['admin_id']
