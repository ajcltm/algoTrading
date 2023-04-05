import unittest
from domain import brokers, timers
from adapters import repository
from entrypoints import api

class Broker(unittest.TestCase):

    def setUp(self) -> None:
        timer = timers.FakeTimer()
        self.repo = repository.FakeTransactionRepository()
        order_api = api.FakeOrderApi(timer=timer, price_api=api.FakePriceApi())
        self.broker = brokers.Broker(timer=timer, repo=self.repo, orderApi=order_api)

    def test_limit_order(self):

        pf_name = 'test_pf'
        funding_scale = 7_000_000
        ticker = ['AMZN', 'APPL']
        order_price = [10_000, 20_000]
        order_scale = [50_000, 100_000]

        self.broker.deposit_or_withdrawal(pf_name=pf_name, amounts=[funding_scale], funding_yn='y')
        self.broker.limit_order(pf_name=pf_name, ticker=ticker, order_price=order_price, order_scale=order_scale)

        self.repo.commit()

        assert ticker == [i.ticker for i in next(self.repo.get_orderLine())]
        assert order_price == [i.order_price for i in next(self.repo.get_orderLine())]
        assert ticker == [i.ticker for i in next(self.repo.get_asset_transaction())]
        assert order_price == [i.trsc_price for i in next(self.repo.get_asset_transaction())]


    def test_market_order(self):

        pf_name = 'test_pf'
        funding_scale = 7_000_000
        ticker = ['AMZN', 'APPL']
        order_scale = [50_000, 100_000]

        self.broker.deposit_or_withdrawal(pf_name=pf_name, amounts=[funding_scale], funding_yn='y')
        self.broker.market_order(pf_name=pf_name, ticker=ticker, order_scale=order_scale)

        self.repo.commit()

        assert ticker == [i.ticker for i in next(self.repo.get_orderLine())]
        assert ticker == [i.ticker for i in next(self.repo.get_asset_transaction())]


if __name__ == '__main__':
    unittest.main()