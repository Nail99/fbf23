import sqlite3 as sql


class Database:
    def __init__(self, db_file):
        self.connection = sql.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_member(self, member_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO members ('member_id') VALUES (?)", (member_id,))

    def member_telegram(self, member_id, telegram):
        with self.connection:
            return self.cursor.execute("UPDATE members SET telegram = ? WHERE member_id = ?", (telegram, member_id,))

    def member_exists(self, member_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,)).fetchall()
            return bool(len(result))

    def set_name(self, member_id, name):
        with self.connection:
            self.cursor.execute("UPDATE members SET name = ? WHERE member_id = ?", (name, member_id),)
            self.connection.commit()

    def set_phone(self, member_id, phone):
        with self.connection:
            self.cursor.execute("UPDATE members SET phone = ? WHERE member_id = ?", (phone, member_id),)
            self.connection.commit()

    def set_city(self, member_id, city):
        with self.connection:
            self.cursor.execute("UPDATE members SET city = ? WHERE member_id = ?", (city, member_id),)
            self.connection.commit()

    def set_pass(self, member_id, pass1):
        with self.connection:
            self.cursor.execute("UPDATE members SET pass = ? WHERE member_id = ?", (pass1, member_id),)
            self.connection.commit()
