
import pandas as pd
from strategies.base import BaseStrategy

class Rotation52WeekTargetProfitStrategy(BaseStrategy):
    """
    Entry: pretul companiei atinge minimul din ultimele `window` zile (52-week low).
    Exit: pozitia atinge un profit tinta (implicit 100%) fata de pretul de intrare.
    O singura pozitie activa per ticker; pozitii simultane pe tickere diferite permise.
    """
    def __init__(self, prices: pd.DataFrame, allocation_per_trade: float, window: int = 252, target_profit_pct: float = 1.0):
        super().__init__(prices, allocation_per_trade)
        self.window = window
        self.target_profit_pct = target_profit_pct
        self.roll_low = prices.rolling(window).min()

    def on_day(self, date, open_positions):
        entries = []
        exits = []
        for ticker in self.prices.columns:
            price = self.prices.loc[date, ticker]
            if pd.isna(price):
                continue

            if ticker in open_positions:
                pos = open_positions[ticker]
                target_price = pos.entry_price * (1 + self.target_profit_pct)
                if price >= target_price:
                    exits.append((ticker, price))
                    continue

            if ticker not in open_positions and price <= self.roll_low.loc[date, ticker]:
                entries.append((ticker, price, self.allocation_per_trade / price))

        return entries, exits
