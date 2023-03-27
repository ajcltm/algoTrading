import unittest
import numpy as np
from datetime import datetime
from services import service
from adapters import repository
from entrypoints import api
import config


class Basic(unittest.TestCase):

    def test_basic_asset_transaction(self):

        pf_name = 'test_pf'
        funding_scale = 7_000_000
        ticker = ['AMZN', 'APPL']
        order_price = [10_000, 20_000]
        order_quantity = [500, 100]

        timer = service.FakeTimer()
        repo = repository.CsvTransactionRepository(file_path=config.file_path)
        order_api = api.FakeOrderApi(timer=timer)
        broker = service.BackTestingBroker(timer=timer, repo=repo, orderApi=order_api)

        broker.deposit_or_withdrawal(pf_name=pf_name, amounts=[funding_scale], funding_yn='y')
        broker.limit_order(pf_name=pf_name, ticker=ticker, order_price=order_price, order_quantity=order_quantity)

        timer.update(datetime(2023, 3, 28))

        broker.deposit_or_withdrawal(pf_name=pf_name, amounts=[funding_scale], funding_yn='y')
        broker.limit_order(pf_name=pf_name, ticker=ticker, order_price=order_price, order_quantity=order_quantity)

        assert order_price + order_price == [i.order_price for i in next(repo.get_orderLine())]
        assert order_price + order_price == [i.trsc_price for i in next(repo.get_asset_transaction())]
        print(np.sum([i.amounts for i in next(repo.get_cash_transaction())]))
        repo.commit()



if __name__ == '__main__':
    unittest.main()