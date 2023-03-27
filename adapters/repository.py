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
        self.file_path = file_path
        self.cash_trsc_df = self.load_df(file_path.joinpath('cash_transaction.csv'))
        self.asset_trsc_df = self.load_df(file_path.joinpath('asset_transaction.csv'))
        self.orderLine_df = self.load_df(file_path.joinpath('orderLine.csv'))
    
    def load_df(self, file_path:Path)->pd.DataFrame:
        if file_path.exists():
            return pd.read_csv(file_path)
        return None

    def commit(self):
        self.cash_trsc_df.to_csv(self.file_path.joinpath('cash_transaction.csv'), index=False)
        self.asset_trsc_df.to_csv(self.file_path.joinpath('asset_transaction.csv'), index=False)
        self.orderLine_df.to_csv(self.file_path.joinpath('orderLine.csv'), index=False)

        self.cash_trsc_df = None
        self.asset_trsc_df = None
        self.orderLine_df = None

    def roll_back(self):
        self.cash_trsc_df = self.load_df(self.file_path.joinpath('cash_transaction.csv'))
        self.asset_trsc_df = self.load_df(self.file_path.joinpath('asset_transaction.csv'))
        self.orderLine_df = self.load_df(self.file_path.joinpath('orderLine.csv'))

    def add_cash_transaction(self, cash_transaction:List[models.CashTransaction])->None:
        new_df = pd.DataFrame([i.__dict__ for i in cash_transaction])
        if isinstance(self.cash_trsc_df, pd.DataFrame):
            self.cash_trsc_df = pd.concat([self.cash_trsc_df, new_df], ignore_index=True)
        else :
            self.cash_trsc_df = new_df

    def add_asset_transaction(self, asset_transaction:List[models.AssetTransaction])->None:
        new_df = pd.DataFrame([i.__dict__ for i in asset_transaction])
        if isinstance(self.asset_trsc_df, pd.DataFrame):
            self.asset_trsc_df = pd.concat([self.asset_trsc_df, new_df], ignore_index=True)
        else :
            self.asset_trsc_df = new_df

    def add_orderLine(self, orderLine:List[models.OrderLine])->None:
        new_df = pd.DataFrame([i.__dict__ for i in orderLine])
        if isinstance(self.orderLine_df, pd.DataFrame):
            self.orderLine_df = pd.concat([self.orderLine_df, new_df], ignore_index=True)
        else :
            self.orderLine_df = new_df

    def get_cash_transaction(self, pf_name:List[str]=None, funding_yn:str=None)->Generator[models.CashTransaction, None, None]:
        yield [models.CashTransaction(**i) for i in self.cash_trsc_df.to_dict(orient='records')]

    def get_asset_transaction(self, pf_name:List[str]=None, ticker:List[str]=None)->Generator[models.AssetTransaction, None, None]:
        yield [models.AssetTransaction(**i) for i in self.asset_trsc_df.to_dict(orient='records')]

    def get_orderLine(self, pf_name:List[str]=None, ticker:List[str]=None)->Generator[models.OrderLine, None, None]:
        yield [models.OrderLine(**i) for i in self.orderLine_df.to_dict(orient='records')]
