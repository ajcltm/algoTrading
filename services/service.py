import abc
from typing import List, Callable
from datetime import datetime
from domain import models
from adapters import repository
from entrypoints import api
import utils

class ITimer(abc.ABC):

    @abc.abstractmethod
    def now(self):
        pass

class FakeTimer(ITimer):

    def __init__(self):
        self.current_time = datetime(1923, 8, 29)

    def now(self):
        return self.current_time

    def update(self, time:datetime):
        self.current_time = time

class RealTimer(ITimer):

    def now(self):
        return datetime.now()

class IBroker(abc.ABC):

    def __init__(self, repository:repository.ITransactionRepository):
        pass

    @abc.abstractmethod
    def handle_deal_signal(self):
        pass

    @abc.abstractmethod
    def deposit_or_withdrawal(self):
        pass

    @abc.abstractmethod
    def limit_order(self):
        pass


class BackTestingBroker(IBroker):

    def __init__(self, timer:ITimer, repo:repository.ITransactionRepository, orderApi:api.IOrderApi):
        self.timer = timer
        self.repo = repo
        self.order_api = orderApi
        self.order_api.connect(self.handle_deal_signal)

    def handle_deal_signal(self, sender:str, asset_transaction:models.AssetTransaction):
        self.repo.add_asset_transaction(asset_transaction=asset_transaction)

    def deposit_or_withdrawal(self, pf_name:str, amounts:List[int], funding_yn:str='n'):
        self.repo.add_cash_transaction([models.CashTransaction(cash_trsc_id=utils.create_id(), pf_name=pf_name, cash_trsc_time=self.timer.now(), funding_yn=funding_yn, amounts=v) for v in amounts])

    def limit_order(self, pf_name:str, ticker:List[str], order_price:List[float], order_quantity:List[float]):
        orderLine = [models.OrderLine(order_id=utils.create_id(), pf_name=pf_name, order_type='limit_order', order_time=self.timer.now(), ticker=v, order_price=order_price[idx], order_quantity=order_quantity[idx], fee=self.calculate_fee(trading_scale=order_price[idx]*order_quantity[idx])) for idx, v in enumerate(ticker)]
        self.repo.add_orderLine(orderLine=orderLine)
        self.deposit_or_withdrawal(pf_name=pf_name, amounts=[-1*(v*order_quantity[idx]+orderLine[idx].fee) for idx, v in enumerate(order_price)])
        self.order_api.send(orderLine)

    def calculate_fee(self, trading_scale:float):
        brokage_fee_rate = .00015
        if trading_scale<0:
            tax_fee_rate = .0025
        else :
            tax_fee_rate = .0015
        return trading_scale*(brokage_fee_rate + tax_fee_rate)
