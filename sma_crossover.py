
import pandas as pd
from strategies.base import BaseStrategy

class SMACrossoverStrategy(BaseStrategy):
    def __init__(self, prices: pd.DataFrame, allocation_per_trade: float, fast_window: int = 20, slow_window: int = 50):
        super().__init__(prices, allocation_per_trade)
        self.fast = prices.rolling(fast_window).mean()
        self.slow = prices.rolling(slow_window).mean()

    def on_day(self, date, open_positions):
        entries = []
        exits = []
        for ticker in self.prices.columns:
            price = self.prices.loc[date, ticker]
            if pd.isna(price):
                continue
            fast = self.fast.loc[date, ticker]
            slow = self.slow.loc[date, ticker]
            if pd.isna(fast) or pd.isna(slow):
                continue
            if ticker not in open_positions and fast > slow:
                entries.append((ticker, price, self.allocation_per_trade / price))
            elif ticker in open_positions and fast < slow:
                exits.append((ticker, price))
        return entries, exits
