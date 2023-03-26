import abc
from domain import models
from typing import Generator, List
from pathlib import Path
import pandas as pd

class ITransactionRepository(abc.ABC):

    @abc.abstractmethod
    def add_cash_transaction(self, cash_transaction:List[models.CashTransaction])->None:
        pass

    @abc.abstractmethod
    def add_asset_transaction(self, asset_transaction:List[models.AssetTransaction])->None: pass

    @abc.abstractmethod
    def add_orderLine(self, orderLine:List[models.OrderLine])->None:
        pass

    @abc.abstractmethod
    def get_cash_transaction(self, pf_name:List[str], funding_yn:str)->Generator[models.CashTransaction, None, None]:
        pass

    @abc.abstractmethod
    def get_asset_transaction(self, pf_name:List[str], ticker:List[str])->Generator[models.AssetTransaction, None, None]:
        pass

    @abc.abstractmethod
    def get_orderLine(self, pf_name:List[str], ticker:List[str])->Generator[models.OrderLine, None, None]:
        pass


class CsvTransactionRepository(ITransactionRepository):

    def __init__(self, file_path:Path):
        self.cash_transaction_file_path = file_path.joinpath('cash_transaction.csv')
        self.asset_transaction_file_path = file_path.joinpath('asset_transaction.csv')
        self.orderLine_file_path = file_path.joinpath('orderLine.csv')

    def add_cash_transaction(self, cash_transaction:List[models.CashTransaction])->None:
        new_df = pd.DataFrame([i.__dict__ for i in cash_transaction])
        if self.cash_transaction_file_path.exists():
            df = pd.read_csv(self.cash_transaction_file_path)
            df = pd.concat([df, new_df], ignore_index=True)
        else :
            df = new_df
        df.to_csv(self.cash_transaction_file_path, index=False)
        new_df = None
        df = None

    def add_asset_transaction(self, asset_transaction:List[models.AssetTransaction])->None:
        new_df = pd.DataFrame([i.__dict__ for i in asset_transaction])
        if self.asset_transaction_file_path.exists():
            df = pd.read_csv(self.asset_transaction_file_path)
            df = pd.concat([df, new_df], ignore_index=True)
        else :
            df = new_df
        df.to_csv(self.asset_transaction_file_path, index=False)
        new_df = None
        df = None

    def add_orderLine(self, orderLine:List[models.OrderLine])->None:
        new_df = pd.DataFrame([i.__dict__ for i in orderLine])
        if self.orderLine_file_path.exists():
            df = pd.read_csv(self.orderLine_file_path)
            df = pd.concat([df, new_df], ignore_index=True)
        else :
            df = new_df
        df.to_csv(self.orderLine_file_path, index=False)
        new_df = None
        df = None

    def get_cash_transaction(self, pf_name:List[str]=None, funding_yn:str=None)->Generator[models.CashTransaction, None, None]:
        yield [models.CashTransaction(**i) for i in pd.read_csv(self.cash_transaction_file_path).to_dict(orient='records')]

    def get_asset_transaction(self, pf_name:List[str]=None, ticker:List[str]=None)->Generator[models.AssetTransaction, None, None]:
        yield [models.AssetTransaction(**i) for i in pd.read_csv(self.asset_transaction_file_path).to_dict(orient='records')]

    def get_orderLine(self, pf_name:List[str]=None, ticker:List[str]=None)->Generator[models.OrderLine, None, None]:
        yield [models.OrderLine(**i) for i in pd.read_csv(self.orderLine_file_path).to_dict(orient='records')]
