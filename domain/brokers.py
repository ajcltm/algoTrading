import abc
from typing import List, Dict
from domain import models, timers
from adapters import repository
from entrypoints import api
from utils import utils

class Broker:

    def __init__(self, timer:timers.ITimer, repo:repository.ITransactionRepository, orderApi:api.IOrderApi):
        self.timer = timer
        self.repo = repo
        self.order_api = orderApi
        self.order_api.connect(self.handle_deal_signal)

    def handle_deal_signal(self, sender:str, asset_transaction_data:List[Dict]):
        asset_transaction = [models.AssetTransaction(**{**i, **{"fee":self.calculate_fee(i['trsc_price']*i['trsc_quantity'])}}) for i in asset_transaction_data]
        self.repo.add_asset_transaction(asset_transaction=asset_transaction)
        self.deposit_or_withdrawal(pf_name=asset_transaction[0].pf_name, amounts=[i.fee for i in asset_transaction])

    def deposit_or_withdrawal(self, pf_name:str, amounts:List[int], funding_yn:str='n'):
        self.repo.add_cash_transaction([models.CashTransaction(cash_trsc_id=utils.utils.create_id(), pf_name=pf_name, cash_trsc_time=self.timer.now(), funding_yn=funding_yn, amounts=v) for v in amounts])

    def limit_order(self, pf_name:str, ticker:List[str], order_price:List[float], order_scale:List[float]):
        orderLine = [models.OrderLine(order_id=utils.utils.create_id(), pf_name=pf_name, order_type='limit_order', order_time=self.timer.now(), ticker=v, order_price=order_price[idx], order_quantity=order_scale[idx]/order_price[idx], order_scale=order_scale[idx]) for idx, v in enumerate(ticker)]
        self.repo.add_orderLine(orderLine=orderLine)
        self.order_api.send(orderLine)

    def market_order(self, pf_name:str, ticker:List[str], order_scale:List[float]):
        orderLine = [models.OrderLine(order_id=utils.utils.create_id(), pf_name=pf_name, order_type='market_order', order_time=self.timer.now(), ticker=v, order_price=None, order_quantity=None, order_scale=order_scale[idx]) for idx, v in enumerate(ticker)]
        self.repo.add_orderLine(orderLine=orderLine)
        self.order_api.send(orderLine)

    def calculate_fee(self, trading_scale:float):
        brokage_fee_rate = .00015
        if trading_scale<0:
            tax_fee_rate = .0025
        else :
            tax_fee_rate = .0015
        return trading_scale*(brokage_fee_rate + tax_fee_rate)