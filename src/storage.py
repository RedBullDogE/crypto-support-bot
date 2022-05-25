import os

from rethinkdb import RethinkDB
from functools import wraps

from helpers.exceptions import NoAdmins

DB_HOST = os.getenv("RETHINKDB_HOST", "localhost")
DB_PORT = os.getenv("RETHINKDB_PORT", 28015)
DB_USER = os.getenv("RETHINKDB_USERNAME", "admin")
DB_PASS = os.getenv("RETHINKDB_PASSWORD", "")
DB_NAME = os.getenv("RETHINKDB_NAME", "test")


def control_connection(func):
    """
    Decorator for convenient management of the DB connection
    """

    @wraps(func)
    def wrapper(self, *args, **kw):
        conn = self.r.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        ).repl()
        try:
            res = func(self, *args, **kw)
        finally:
            conn.close()
        return res

    return wrapper


def wrap_class_methods(function_decorator):
    """
    Decorator-function for classes. Wraps all methods of a class
    except those that start with underscore
    """

    def decorator(cls):
        for name, obj in vars(cls).items():
            if callable(obj) and not name.startswith("_"):
                setattr(cls, name, function_decorator(obj))
        return cls

    return decorator


@wrap_class_methods(control_connection)
class Storage:

    admin_table = "admins"
    user_support_table = "user_support"
    message_table = "user_messages"

    def __init__(self) -> None:
        self.r = RethinkDB()
        with self.r.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        ) as conn:
            if not self.r.table_list().contains(self.user_support_table).run(conn):
                self.r.db(DB_NAME).table_create(
                    self.user_support_table, primary_key="user_id"
                ).run(conn)

            if not self.r.table_list().contains(self.admin_table).run(conn):
                self.r.db(DB_NAME).table_create(
                    self.admin_table, primary_key="admin_id"
                ).run(conn)

            if not self.r.table_list().contains(self.message_table).run(conn):
                self.r.db(DB_NAME).table_create(
                    self.message_table, primary_key="id"
                ).run(conn)

    def add_admin(self, user_id: int):
        elem = self.r.table(self.admin_table).get(user_id).run()

        # update if such admin already exists
        if elem:
            return False

        new = {"admin_id": user_id, "users": 0, "active": False}
        res = self.r.table(self.admin_table).insert(new).run()

        return res["inserted"] == 1

    def admin_mode(self, user_id, state):
        elem = self.r.table(self.admin_table).get(user_id).run()

        # exit if there is no such admin
        if not elem:
            return False

        res = (
            self.r.table(self.admin_table).get(user_id).update({"active": state}).run()
        )
        return res["replaced"] == 1

    def is_admin(self, user_id: int):
        return self.r.table(self.admin_table).get(user_id).run() is not None

    def is_admin_active(self, user_id):
        return self.r.table(self.admin_table).get(user_id)["active"].run()

    def _get_free_admin(self):
        admin = (
            self.r.table(self.admin_table)
            .filter(self.r.row["active"])
            .order_by("users")
            .limit(1)["admin_id"]
            .run()
        )
        if not admin:
            raise NoAdmins

        return admin[0]

    def get_user_admin(self, user_id):
        return self.r.table(self.user_support_table).get(user_id)["admin_id"].run()

    def add_target_user(self, admin_id, message_id, user_id):
        data = {
            "admin_id": admin_id,
            "message_id": message_id,
            "user_id": user_id,
        }
        self.r.table(self.message_table).insert(data).run()

    def get_target_user(self, admin_id, message_id):
        res = (
            self.r.table(self.message_table)
            .filter(
                lambda row: row["admin_id"] == admin_id
                and row["message_id"] == message_id
            )
            .limit(1)["user_id"]
            .run()
        )

        if not res:
            return None

        return list(res)[0]

    def remove_target_user(self, user_id):
        res = (
            self.r.table(self.message_table)
            .filter(self.r.row["user_id"] == user_id)
            .delete()
            .run()
        )

        return res["deleted"]

    def add_user_support(self, user_id):

        # get free admin
        admin_id = self._get_free_admin()

        # prepare data to insert
        data = {
            "user_id": user_id,
            "admin_id": admin_id,
        }

        # insert new record
        res = self.r.table(self.user_support_table).insert(data).run()

        # increase counter
        self.r.table(self.admin_table).get(admin_id).update(
            {"users": self.r.row["users"] + 1}
        ).run()

        return admin_id

    def remove_user_support(self, user_id):
        # remove record
        record = self.r.table(self.user_support_table).get(user_id).run()

        if not record:
            return False

        res = self.r.table(self.user_support_table).get(user_id).delete().run()

        # decrease counter
        self.r.table(self.admin_table).get(record["admin_id"]).update(
            {"users": self.r.row["users"] - 1}
        ).run()

        return res["deleted"] == 1


if __name__ == "__main__":
    s = Storage()

    s.add_admin(69526339)
