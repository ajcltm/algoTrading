import unittest
import numpy as np
from services import services
from adapters import repository
import config


class Basic(unittest.TestCase):

    def test_basic_asset_transaction(self):

        pf_name = 'test_pf'
        funding_scale = 7_000_000
        ticker = ['AMZN', 'APPL']
        order_price = [10_000, 20_000]
        order_quantity = [500, 100]

        repo = repository.CsvTransactionRepository(file_path=config.file_path)
        broker = services.BackTestingBroker(repo=repo)

        broker.deposit_or_withdrawal(pf_name=pf_name, amounts=[funding_scale], funding_yn='y')
        broker.limit_order(pf_name=pf_name, ticker=ticker, order_price=order_price, order_quantity=order_quantity)

        assert order_price == [i.order_price for i in next(repo.get_orderLine())]
        assert order_price == [i.trsc_price for i in next(repo.get_asset_transaction())]
        print(np.sum([i.amounts for i in next(repo.get_cash_transaction())]))


if __name__ == '__main__':
    unittest.main()