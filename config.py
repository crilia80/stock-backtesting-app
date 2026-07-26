from dataclasses import dataclass
from typing import List

@dataclass
class BacktestConfig:
    tickers: List[str]
    start: str
    end: str
    initial_cash: float = 0.0
    allocation_per_trade: float = 1000.0
    auto_adjust: bool = True
