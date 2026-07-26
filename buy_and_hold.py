
import pandas as pd
from strategies.base import BaseStrategy

class BuyAndHoldStrategy(BaseStrategy):
    def __init__(self, prices: pd.DataFrame, allocation_per_trade: float):
        super().__init__(prices, allocation_per_trade)
        self.entered = set()

    def on_day(self, date, open_positions):
        entries = []
        exits = []
        for ticker in self.prices.columns:
            price = self.prices.loc[date, ticker]
            if pd.isna(price):
                continue
            if ticker not in self.entered and ticker not in open_positions:
                entries.append((ticker, price, self.allocation_per_trade / price))
                self.entered.add(ticker)
        return entries, exits
