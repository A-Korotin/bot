from DatabaseManager import DatabaseManager
from Request import *
from Logger import Logger
from typing import List, Tuple
import requests
import hashlib
import hmac


class APIHandler:

    @staticmethod
    def __read_keys(file_path: str) -> Tuple[str, bytes]:
        with open(file_path, 'r') as file:
            values = file.readline().split()
            return values[0], values[1].encode("utf-8")

    def __generate_signature(self, params: str) -> str:
        return hmac.new(self.__secret_key, params.encode('utf-8'), hashlib.sha256).hexdigest()

    def __init_properties(self):
        db_manager = DatabaseManager("../res/dbs/logging.db")
        db_manager.create_table("requests", {
                                             "id": "integer primary key",
                                             "type": "text not null",
                                             "time": "text not null"
                                            })

        db_manager.create_table("prices", {"id": "integer primary key",
                                           "asset": "text not null",
                                           "price": "decimal not null",
                                           "time": "text not null"})

        self.__logger = Logger(db_manager)
        self.__servers = ["https://api.binance.com", "https://api1.binance.com",
                          "https://api2.binance.com", "https://api3.binance.com"]
        self.__methods: dict = {"POST": requests.post,
                                "GET": requests.get}

    def __init__(self, api_key: str = None, secret_key: str = None, file_path: str = None, **kwargs):
        if file_path is None:
            self.__api_key, self.__secret_key = api_key, secret_key
        else:
            self.__api_key, self.__secret_key = self.__read_keys(file_path)
        if self.__api_key is None or self.__secret_key is None:
            raise RuntimeError("No keys found")
        self.__init_properties()

    def send_request(self, order: Request) -> dict:
        method, signed, url, params = order.compose()
        api_response: requests.Response
        for server in self.__servers:
            if signed:
                api_response = self.__methods[method](f"{server}/{url}?{params}"
                                                      f"&signature={self.__generate_signature(params)}",
                                                      headers={'X-MBX-APIKEY': self.__api_key})
            else:
                api_response = self.__methods[method](f"{server}/{url}?{params}",
                                                      headers={'X-MBX-APIKEY': self.__api_key})

            if "code" not in api_response.json().keys():
                break

        return api_response.json()

