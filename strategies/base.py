from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, prices: pd.DataFrame, allocation_per_trade: float):
        self.prices = prices
        self.allocation_per_trade = allocation_per_trade

    @abstractmethod
    def on_day(self, date, open_positions):
        pass
