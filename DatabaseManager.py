import sqlite3
from typing import Dict, Iterable


class DatabaseManager:
    def __init__(self, filepath: str) -> None:
        self.__filePath = filepath
        self.__connection = sqlite3.connect(filepath)

    def __execute(self, request: str, params: Iterable = None, size: int = None):
        cursor = self.__connection.cursor()
        if params is None:
            cursor.execute(request)
        else:
            cursor.execute(request, params)
        result = cursor.fetchall() if size is None else cursor.fetchmany(size)
        self.__connection.commit()
        cursor.close()
        return result

    def create_table(self, name: str, layout: Dict[str, str] = None) -> None:
        request: str = \
            f"CREATE TABLE IF NOT EXISTS {name} "
        if layout is not None:
            request += "(" + ", ".join([f'{key} = {value}' for key, value in layout.items()]) + ")"
        self.__execute(request)

    def insert(self, table_name: str, values: dict) -> None:
        request: str = \
            f"INSERT INTO {table_name} ({', '.join(values.keys())}) VALUES({', '.join('?' * len(values))})"
        self.__execute(request, list(values.values()))

    def select(self, table_name: str, columns: Iterable = None, criteria: dict = None,
               order: Dict = None, size: int = None):
        request: str = \
            f"SELECT {'*' if columns is None else ', '.join(columns)} FROM {table_name} "

        if criteria is not None:
            request += "WHERE " + ", ".join([f"{key} = ?" for key in criteria.keys()])

        if order is not None:
            request += "ORDER BY " + ", ".join([f"{key} {value}" for key, value in order.items()])
        return self.__execute(request, size=size) if criteria is None else \
            self.__execute(request, list(criteria.values()), size=size)

    def update(self, table_name: str, content: dict, criteria: dict):
        request: str = \
            f"UPDATE {table_name} SET {', '.join([f'{key} = {value}' for key, value in content.items()])} " \
            f"WHERE {', '.join([f'{key} = {value}' for key, value in criteria.items()])}"
        self.__execute(request)

    def delete(self, table_name: str, criteria: dict):
        request: str = \
            f"DELETE FROM {table_name} WHERE {', '.join([f'{key} = {value}' for key, value in criteria.items()])}"
        self.__execute(request)
