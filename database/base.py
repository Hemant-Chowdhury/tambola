import sqlite3
from abc import ABCMeta, abstractmethod

DATABASE = 'tambola.db'


class Table(metaclass=ABCMeta):
    """docstring for table"""
    __INSTANCE = None

    def __init__(self, table_name):
        self.table_name = table_name
        self.connection = sqlite3.connect(DATABASE)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor_obj = self.connection.cursor()
        self.create_table()

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls._create_instance()
        return cls.__INSTANCE

    @classmethod
    @abstractmethod
    def _create_instance(cls):
        ...

    @abstractmethod
    def create_table(self, *args, **kwargs):
        ...

    @abstractmethod
    def insert(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...

    @abstractmethod
    def fetch_all(self):
        ...
