from DatabaseManager import DatabaseManager
from Request import *


class Logger:
    def __init__(self, manager: DatabaseManager):
        self.__manager = manager

    def log_request(self, request: Request):
        table, body = request.get_log_info()
        self.__manager.insert(table, body)

