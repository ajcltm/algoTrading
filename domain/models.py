from dataclasses import dataclass
from datetime import datetime

@dataclass
class CashTransaction:
    cash_trsc_id: str
    pf_name: str
    cash_trsc_time: datetime
    funding_yn: str
    amounts: float

@dataclass
class AssetTransaction:
    asset_trsc_id: str
    pf_name: str
    order_id: str
    asset_trsc_time: datetime
    ticker: str
    trsc_price: float
    trsc_quantity: float

@dataclass
class OrderLine:
    order_id: str
    pf_name: str
    order_type: str
    order_time: datetime
    ticker: str
    order_price: float
    order_quantity: float
    fee: float

    def __post_init__(self):
        if isinstance(self.order_time, str):
            self.order_time = datetime.strptime(self.order_time, '%Y-%m-%d %H:%M:%S.%f')
