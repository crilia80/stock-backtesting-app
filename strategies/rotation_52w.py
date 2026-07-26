import pandas as pd
from strategies.base import BaseStrategy

class Rotation52WeekStrategy(BaseStrategy):
    def __init__(self, prices: pd.DataFrame, allocation_per_trade: float, window: int = 252):
        super().__init__(prices, allocation_per_trade)
        self.window = window
        self.roll_low = prices.rolling(window).min()
        self.roll_high = prices.rolling(window).max()

    def on_day(self, date, open_positions):
        entries = []
        exits = []
        for ticker in self.prices.columns:
            price = self.prices.loc[date, ticker]
            if pd.isna(price):
                continue
            if ticker not in open_positions and price <= self.roll_low.loc[date, ticker]:
                entries.append((ticker, price, self.allocation_per_trade / price))
            elif ticker in open_positions and price >= self.roll_high.loc[date, ticker]:
                exits.append((ticker, price))
        return entries, exits
