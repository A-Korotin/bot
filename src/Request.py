import datetime
from enum import Enum
from typing import Tuple, Dict
from abc import ABC, abstractmethod
import time
from decimal import Decimal


def gen_timestamp() -> int:
    return int(time.time() * 1000)


class RequestType(Enum):
    ABC = 0
    SELL = 1,
    BUY = 2,
    PRICE_UPDATE = 3,
    WALLET_UPDATE = 4


class Request(ABC):

    _type = RequestType.ABC

    @abstractmethod
    def compose(self):
        raise RuntimeError

    @abstractmethod
    def get_log_info(self):
        raise RuntimeError


class SellOrder(Request):
    def __init__(self, asset: str, price: Decimal, quantity: Decimal):
        self._method = "POST"
        self._signed = True
        self._type = RequestType.SELL
        self.__asset = asset
        self.__price = price
        self.__quantity = quantity

    def compose(self):
        url: str = "api/v3/order"
        params: str = f"symbol={self.__asset}" \
                      f"&side=SELL" \
                      f"&type=LIMIT_MAKER" \
                      f"&quantity={self.__quantity}" \
                      f"&price={self.__price}" \
                      f"&timestamp={gen_timestamp()}" \
                      f"&recvWindow=15000"

        return self._method, self._signed, url, params

    def get_log_info(self) -> Tuple[str, Dict[str, str]]:
        return "requests", {"type": str(self._type).split('.')[-1],
                            "time": datetime.datetime.now().isoformat()}


class BuyOrder(Request):
    def __init__(self, asset: str, price: Decimal, quantity: Decimal):
        self._method = "POST"
        self._signed = True
        self._type = RequestType.BUY
        self.__asset = asset
        self.__price = price
        self.__quantity = quantity

    def compose(self) -> Tuple[str, bool, str, str]:
        url: str = "api/v3/order"
        params: str = f"symbol={self.__asset}" \
                      f"&side=BUY" \
                      f"&type=LIMIT_MAKER" \
                      f"&quantity={self.__quantity}" \
                      f"&price={self.__price}" \
                      f"&timestamp={gen_timestamp()}" \
                      f"&recvWindow=15000"

        return self._method, self._signed, url, params

    def get_log_info(self) -> Tuple[str, Dict[str, str]]:
        return "requests", {"type": str(self._type).split('.')[-1],
                            "time": datetime.datetime.now().isoformat()}


class PriceUpdate(Request):
    def __init__(self, asset: str) -> None:
        self._method = "GET"
        self._signed: bool = False
        self._type = RequestType.PRICE_UPDATE
        self.__asset = asset

    def compose(self) -> Tuple[str, bool, str, str]:
        url: str = "api/v3/ticker/price"
        params = f"symbol={self.__asset}"
        return self._method, self._signed, url, params

    def get_log_info(self) -> Tuple[str, Dict[str, str]]:
        return "requests", {"type": str(self._type).split('.')[-1],
                            "time": datetime.datetime.now().isoformat()}


class WalletUpdate(Request):
    def __init__(self) -> None:
        self._method = "GET"
        self._signed: bool = True
        self._type = RequestType.WALLET_UPDATE

    def compose(self) -> Tuple[str, bool, str, str]:
        url: str = "api/v3/account"
        params = f"timestamp={gen_timestamp()}"
        return self._method, self._signed, url, params

    def get_log_info(self) -> Tuple[str, Dict[str, str]]:
        return "requests", {"type": f"{str(self._type).split('.')[-1]}",
                            "time": f"{datetime.datetime.now().isoformat()}"}
