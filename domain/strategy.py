import abc
import numpy as np
from domain import timers, brokers
from entrypoints import api
from utils import calculation

class IStrategy(abc.ABC):

    def __init__(self, pf_name:str, timer:timers.ITimer, broker:brokers.Broker, priceApi:api.IPriceApi):
        self.pf_name = pf_name
        self.timer = timer
        self.broker = broker
        self.priceApi = priceApi
        self.position = False

    def operate(self, **sys_data):
        pass

class CompositeStrategy:

    def __init__(self):

        self.strategies = []

    def operate(self, **sys_data):
        self.strategies.operate()

    def add(self, strategy:IStrategy):
        self.strategies.append(strategy)

class GoldenCrossStrategy(IStrategy):

    def __init__(self, short_window, long_window, trading_scale):
        self.short_window = short_window
        self.long_window = long_window
        self.trading_scale
        self.price_container = []

    def operate(self, **sys_data):
        self.price_container.append(sys_data.get('price'))
        self.price_container = self.price_container[-self.long_window-1:]
        if calculation.golden_cross_signal(self.price_container, short_window=self.short_window, long_window=self.long_window)=='buy' and self.position == False:
            self.broker.market_order(pf_name=self.pf_name, ticker=[sys_data.get('ticker')], order_scale=self.trading_scale)
        if calculation.golden_cross_signal(self.price_container, short_window=self.short_window, long_window=self.long_window)=='sell' and self.position == True:
            self.broker.market_order(pf_name=self.pf_name, ticker=[sys_data.get('ticker')], order_scale=-self.trading_scale)
