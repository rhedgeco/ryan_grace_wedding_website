import random
import string

from datetime import datetime

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase

TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
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
        print(admin_id)

    def get_admin_from_add_code(self, add_code: str):
        return self.db.fetchone_query(f"SELECT * FROM admins WHERE add_code='{add_code}'")

    def reset_admin_add_code(self, admin_id: str):
        add_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                           for _ in range(ADD_CODE_LENGTH))
        self.db.send_query(f"UPDATE admins SET add_code = '{add_code}' WHERE admin_id = '{admin_id}'")

    def update_user_access(self, admin_id: str):
        self.db.send_query(f"UPDATE admins SET last_access = '{datetime.now().strftime(TIME_FORMAT)}' "
                           f"WHERE admin_id = '{admin_id}'")

    def validate_user_expire(self, admin_id: str, expire_time):
        user = self.get_admin(admin_id)
        last_access = datetime.strptime(user['last_access'], TIME_FORMAT)
        return last_access + expire_time > datetime.now()
