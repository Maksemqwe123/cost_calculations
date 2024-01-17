import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class Postgres:
    def __init__(self):
        self.connection = psycopg2.connect(host=os.getenv('HOST'), user=os.getenv('USER'),
                                           password=os.getenv('PASSWORD'), database=os.getenv('DB_NAME'))
        self.cursor = self.connection.cursor()

        self._create_table_registrations_user()
        self._create_main_table()

    def _create_table_registrations_user(self):
        sql_create = """CREATE TABLE IF NOT EXISTS user_registration (
        user_id BIGINT UNIQUE,
        user_name VARCHAR(128),
        login VARCHAR(6000),
        password VARCHAR(6000),
        date_registration TIMESTAMP
        )"""

        with self.connection:
            self.cursor.execute(sql_create)

    def _create_main_table(self):
        sql_create = """CREATE TABLE IF NOT EXISTS users_expenses (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        user_name VARCHAR(128),
        company_name VARCHAR(256),
        category_name VARCHAR(512),
        price FLOAT8,
        dttm TIMESTAMP
        )"""

        with self.connection:
            self.cursor.execute(sql_create)

    def insert_table_registrations_user(self, user_id, user_name, login, password, date_registration):
        sql_insert = 'INSERT INTO user_registration (user_id, user_name, login, password, date_registration) VALUES ('
        sql_insert = sql_insert + user_id + ",'" + user_name + "','" + login + "','" + password + "','" + date_registration + "');"

        with self.connection:
            self.cursor.execute(sql_insert)

    def insert_main_table(self, user_id, user_name, company_name, category_name, price, last_activity):
        sql_insert = 'INSERT INTO users_expenses (user_id, user_name, company_name, category_name, price, dttm)'
        sql_insert = sql_insert + "VALUES ('" + user_id + "', '" + user_name + "', '" + company_name + "', '" + category_name
        sql_insert = sql_insert + "', '" + price + "', '" + last_activity + "');"

        with self.connection:
            self.cursor.execute(sql_insert)

    def select_table_registrations_user(self, user_id):
        sql_select = f'SELECT login, password FROM user_registration WHERE user_id = {user_id}'

        with self.connection:
            self.cursor.execute(sql_select)
        return self.cursor.fetchall()

    def check_login_user(self, login):
        sql_select = f"SELECT user_id FROM user_registration WHERE login = '{login}'"

        with self.connection:
            self.cursor.execute(sql_select)
        return self.cursor.fetchall()

    def select_main_table(self, user_id):
        sql_select = f'SELECT user_id FROM users_expenses WHERE user_id = {user_id}'

        with self.connection:
            self.cursor.execute(sql_select)
        return self.cursor.fetchall()
