import unittest
from domain import models
from services import service
from adapters import repository
import config
import utils

class FakeTransactionRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.timer = service.FakeTimer()

        self.cash_id_1 = utils.create_id()
        self.asset_id_1 = utils.create_id()
        self.order_id_1 = utils.create_id()
        
        self.cash_trsc_1 = models.CashTransaction(cash_trsc_id=self.cash_id_1, pf_name='test_repo', cash_trsc_time=self.timer.now(), funding_yn='y', amounts=5000)
        self.asset_trsc_1 = models.AssetTransaction(asset_trsc_id=self.asset_id_1, pf_name='test_repo', order_id='1234', asset_trsc_time=self.timer.now(), ticker='AMZN', trsc_price=100, trsc_quantity=50, fee=5)
        self.orderLine_1 = models.OrderLine(order_id=self.order_id_1, pf_name='test_repo', order_type='limit_order', order_time=self.timer.now(), ticker='AMZN', order_price=200, order_quantity=10)

        self.cash_id_2 = utils.create_id()
        self.asset_id_2 = utils.create_id()
        self.order_id_2 = utils.create_id()
        
        self.cash_trsc_2 = models.CashTransaction(cash_trsc_id=self.cash_id_2, pf_name='test_repo', cash_trsc_time=self.timer.now(), funding_yn='y', amounts=5000)
        self.asset_trsc_2 = models.AssetTransaction(asset_trsc_id=self.asset_id_2, pf_name='test_repo', order_id='1234', asset_trsc_time=self.timer.now(), ticker='AMZN', trsc_price=100, trsc_quantity=50, fee=5)
        self.orderLine_2 = models.OrderLine(order_id=self.order_id_2, pf_name='test_repo', order_type='limit_order', order_time=self.timer.now(), ticker='AMZN', order_price=200, order_quantity=10)

        self.cash_id_3 = utils.create_id()
        self.asset_id_3 = utils.create_id()
        self.order_id_3 = utils.create_id()
        
        self.cash_trsc_3 = models.CashTransaction(cash_trsc_id=self.cash_id_3, pf_name='test_repo', cash_trsc_time=self.timer.now(), funding_yn='y', amounts=5000)
        self.asset_trsc_3 = models.AssetTransaction(asset_trsc_id=self.asset_id_3, pf_name='test_repo', order_id='1234', asset_trsc_time=self.timer.now(), ticker='AMZN', trsc_price=100, trsc_quantity=50, fee=5)
        self.orderLine_3 = models.OrderLine(order_id=self.order_id_3, pf_name='test_repo', order_type='limit_order', order_time=self.timer.now(), ticker='AMZN', order_price=200, order_quantity=10)

        self.cash_id_4 = utils.create_id()
        self.asset_id_4 = utils.create_id()
        self.order_id_4 = utils.create_id()
        
        self.cash_trsc_4 = models.CashTransaction(cash_trsc_id=self.cash_id_4, pf_name='test_repo', cash_trsc_time=self.timer.now(), funding_yn='y', amounts=5000)
        self.asset_trsc_4 = models.AssetTransaction(asset_trsc_id=self.asset_id_4, pf_name='test_repo', order_id='1234', asset_trsc_time=self.timer.now(), ticker='AMZN', trsc_price=100, trsc_quantity=50, fee=5)
        self.orderLine_4 = models.OrderLine(order_id=self.order_id_4, pf_name='test_repo', order_type='limit_order', order_time=self.timer.now(), ticker='AMZN', order_price=200, order_quantity=10)

    def test_repo(self):
        repo = repository.CsvTransactionRepository(file_path=config.file_path)

        repo.add_cash_transaction(cash_transaction=[self.cash_trsc_1])
        repo.add_asset_transaction(asset_transaction=[self.asset_trsc_1])
        repo.add_orderLine(orderLine=[self.orderLine_1])

        repo.commit()

        assert next(repo.get_cash_transaction())[0].cash_trsc_id == self.cash_id_1
        assert next(repo.get_asset_transaction())[0].asset_trsc_id == self.asset_id_1
        assert next(repo.get_orderLine())[0].order_id == self.order_id_1

        repo.add_cash_transaction(cash_transaction=[self.cash_trsc_2])
        repo.add_asset_transaction(asset_transaction=[self.asset_trsc_2])
        repo.add_orderLine(orderLine=[self.orderLine_2])

        assert next(repo.get_cash_transaction())[-1].cash_trsc_id == self.cash_id_1
        assert next(repo.get_asset_transaction())[-1].asset_trsc_id == self.asset_id_1
        assert next(repo.get_orderLine())[-1].order_id == self.order_id_1

        repo.commit()

        assert next(repo.get_cash_transaction())[-1].cash_trsc_id == self.cash_id_2
        assert next(repo.get_asset_transaction())[-1].asset_trsc_id == self.asset_id_2
        assert next(repo.get_orderLine())[-1].order_id == self.order_id_2

        repo.add_cash_transaction(cash_transaction=[self.cash_trsc_3])
        repo.add_asset_transaction(asset_transaction=[self.asset_trsc_3])
        repo.add_orderLine(orderLine=[self.orderLine_3])

        repo.add_cash_transaction(cash_transaction=[self.cash_trsc_4])
        repo.add_asset_transaction(asset_transaction=[self.asset_trsc_4])
        repo.add_orderLine(orderLine=[self.orderLine_4])

        repo.roll_back()

        assert next(repo.get_cash_transaction())[-1].cash_trsc_id == self.cash_id_2
        assert next(repo.get_asset_transaction())[-1].asset_trsc_id == self.asset_id_2
        assert next(repo.get_orderLine())[-1].order_id == self.order_id_2

        repo.add_cash_transaction(cash_transaction=[self.cash_trsc_4, self.cash_trsc_3])
        repo.add_asset_transaction(asset_transaction=[self.asset_trsc_4, self.asset_trsc_3])
        repo.add_orderLine(orderLine=[self.orderLine_4, self.orderLine_3])

        repo.commit()

        assert next(repo.get_cash_transaction())[-1].cash_trsc_id == self.cash_id_3
        assert next(repo.get_asset_transaction())[-1].asset_trsc_id == self.asset_id_3
        assert next(repo.get_orderLine())[-1].order_id == self.order_id_3

if __name__ == '__main__':
    unittest.main()

