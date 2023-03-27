import abc
from typing import List
from blinker import signal
from domain import models
from services import service
import utils

class IOrderApi(abc.ABC):

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def send(self):
        pass

class FakeOrderApi(IOrderApi):

    def __init__(self, timer) -> None:
        self.timer = timer
        self.signal = signal('fakeOrderApi')
        self.signal.connect(self.handle_deal_data)
        self.callback_func = None

    def connect(self, callback_func):
        self.callback_func = callback_func
    
    def send(self, orderLine:List[models.OrderLine]):
        if orderLine[0].order_type == 'limit_order':
            self.signal.send('fake_system', asset_transaction=[models.AssetTransaction(asset_trsc_id=utils.create_id(), pf_name=orderLine[idx].pf_name, order_id=orderLine[idx].order_id, asset_trsc_time=self.timer.now(), ticker=orderLine[idx].ticker, trsc_price=orderLine[idx].order_price, trsc_quantity=orderLine[idx].order_quantity) for idx, v in enumerate(orderLine)])

    def handle_deal_data(self, sender, asset_transaction:List[models.AssetTransaction]):
        self.callback_func(sender, asset_transaction)
