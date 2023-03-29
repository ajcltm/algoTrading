import unittest
import numpy as np
from datetime import datetime
from services import service
from adapters import repository
from entrypoints import api
import config


class Broker(unittest.TestCase):

    def setUp(self) -> None:
        timer = service.FakeTimer()
        self.repo = repository.CsvTransactionRepository(file_path=config.file_path)
        order_api = api.FakeOrderApi(timer=timer, price_api=api.FakePriceApi())
        self.broker = service.BackTestingBroker(timer=timer, repo=self.repo, orderApi=order_api)

    def test_limit_order(self):

        pf_name = 'test_pf'
        funding_scale = 7_000_000
        ticker = ['AMZN', 'APPL']
        order_price = [10_000, 20_000]
        order_quantity = [500, 100]

        self.broker.deposit_or_withdrawal(pf_name=pf_name, amounts=[funding_scale], funding_yn='y')
        self.broker.limit_order(pf_name=pf_name, ticker=ticker, order_price=order_price, order_quantity=order_quantity)

        assert ticker == [i.ticker for i in next(self.repo.get_orderLine())]
        assert order_price == [i.order_price for i in next(self.repo.get_orderLine())]
        assert ticker == [i.ticker for i in next(self.repo.get_asset_transaction())]
        assert order_price == [i.trsc_price for i in next(self.repo.get_asset_transaction())]

    def test_marker_order(self):

        pf_name = 'test_pf'
        funding_scale = 7_000_000
        ticker = ['AMZN', 'APPL']
        order_quantity = [500, 100]


        self.broker.deposit_or_withdrawal(pf_name=pf_name, amounts=[funding_scale], funding_yn='y')
        self.broker.market_order(pf_name=pf_name, ticker=ticker, order_quantity=order_quantity)

        assert ticker == [i.ticker for i in next(self.repo.get_orderLine())]
        assert ticker == [i.ticker for i in next(self.repo.get_asset_transaction())]


if __name__ == '__main__':
    unittest.main()