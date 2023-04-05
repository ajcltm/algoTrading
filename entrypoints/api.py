import abc
from typing import List
from datetime import datetime
from blinker import signal
from domain import models, timers
from utils import utils

class IOrderApi(abc.ABC):

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def send(self):
        pass


class FakeOrderApi(IOrderApi):

    def __init__(self, timer, price_api) -> None:
        self.timer = timer
        self.price_api = price_api
        self.signal = signal('fakeOrderApi')
        self.signal.connect(self.handle_deal_data)
        self.callback_func = None

    def connect(self, callback_func):
        self.callback_func = callback_func
    
    def send(self, orderLine:List[models.OrderLine]):
        if orderLine[0].order_type == 'limit_order':
            self.signal.send('fake_system', data=[{'asset_trsc_id':utils.utils.create_id(), 'pf_name':orderLine[idx].pf_name, 'order_id':orderLine[idx].order_id, 'asset_trsc_time':self.timer.now(), 'ticker':orderLine[idx].ticker, 'trsc_price':orderLine[idx].order_price, 'trsc_quantity':orderLine[idx].order_quantity} for idx, v in enumerate(orderLine)])
        if orderLine[0].order_type == 'market_order':
            self.signal.send('fake_system', data=[{'asset_trsc_id':utils.utils.create_id(), 'pf_name':orderLine[idx].pf_name, 'order_id':orderLine[idx].order_id, 'asset_trsc_time':self.timer.now(), 'ticker':orderLine[idx].ticker, 'trsc_price':self.price_api.get_price_by_date_ticker(date=self.timer.now(), ticker=orderLine[idx].ticker), 'trsc_quantity':orderLine[idx].order_quantity} for idx, v in enumerate(orderLine)])

    def handle_deal_data(self, sender, data):
        self.callback_func(sender, data)


class IPriceApi(abc.ABC):

    @abc.abstractmethod
    def get_price_by_date_ticker(self, date:datetime, ticker:str):
        pass

class FakePriceApi(IPriceApi):
    
    dataset = {datetime(1923, 8, 29):{'AMZN': 1100, 'APPL': 4500}}

    def get_price_by_date_ticker(self, date: datetime, ticker: str):
        return self.dataset.get(date).get(ticker)