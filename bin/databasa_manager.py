import os
import sqlite3


# Класс для работы с базой данных
class DatabaseManager:
    # Конструктор класса
    def __init__(self):
        self.db_connection = None
        if not os.path.isfile('data/data.db'):
            self.create_tables()

    # Функция для выполнения запросов
    def execute_query(self, query, params=None):
        self.db_connection = sqlite3.connect('data/data.db')
        cursor = self.db_connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.db_connection.commit()
        result = cursor.fetchall()
        self.db_connection.close()
        return result

    # Функция для создания таблиц
    def create_tables(self):
        query = '''CREATE TABLE IF NOT EXISTS settings
                   (id INTEGER PRIMARY KEY, name TEXT, value TEXT)'''
        self.execute_query(query)

        query = '''CREATE TABLE IF NOT EXISTS saves
                   (id INTEGER PRIMARY KEY, 
                   level TEXT, 
                   win INTEGER, 
                   lose INTEGER, 
                   kill INTEGER, 
                   coins INTEGER)'''
        self.execute_query(query)

    # Функция для вывода всех записей с указанной таблицы
    def select_all(self, table):
        query = f"SELECT * FROM {table}"
        return self.execute_query(query)

    # Функция для получения записи по id
    def select_by_id(self, table, id):
        query = f"SELECT * FROM {table} WHERE id=?"
        return self.execute_query(query, (id,))

    # Функция для получения записи по определенному значению в колонке
    def select_by_col(self, table, name_col, col):
        query = f"SELECT * FROM {table} WHERE {name_col}='{col}'"
        return self.execute_query(query)

    # Функция создания новой записи, таблицы сохранений
    def insert_save(self, data):
        query = f"""INSERT INTO saves (level, win, lose, kill, coins) 
        VALUES ('{data['level']}', {1 if data['win'] else 0}, {0 if data['win'] else 1}, 
        {data['kill']}, {data['coins']})"""
        self.execute_query(query)

    # Функция вставки новой записи, таблицы настроек
    def insert_settings(self, data):
        for key, value in data.items():
            query = f"INSERT INTO settings (name, value) VALUES ('{key}', '{value}')"
            self.execute_query(query)

    # Функция для обновления настроек
    def update_settings(self, data):
        for key, value in data.items():
            if self.select_by_col('settings', 'name', key):
                query = f"UPDATE settings SET value='{value}' WHERE name='{key}'"
                self.execute_query(query)
            else:
                data = {
                    key: value
                }
                self.insert_settings(data)

    # Функция для обновления сохранения
    def update_save(self, data):
        query = f"""UPDATE saves SET win={data['win']}, lose={data['lose']}, 
        kill={data['kill']}, coins={data['coins']} WHERE level='{data['level']}'"""
        self.execute_query(query)

    # Функция для удаления записи по id
    def delete(self, table, id):
        query = f"DELETE FROM {table} WHERE id=?"
        self.execute_query(query, (id,))

    # Функция для удаления всех записей из таблицы
    def delete_all(self, table):
        query = f"DELETE FROM {table}"
        self.execute_query(query)
