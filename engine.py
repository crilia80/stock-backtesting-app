import pandas as pd
from models import Position, Trade

class BacktestEngine:
    def __init__(self, prices: pd.DataFrame, strategy):
        self.prices = prices
        self.strategy = strategy
        self.open_positions = {}
        self.trades = []
        self.equity_curve = []
        self.realized_pnl = 0.0

    def run(self):
        for date in self.prices.index:
            entries, exits = self.strategy.on_day(date, self.open_positions)

            for ticker, price in exits:
                pos = self.open_positions.pop(ticker)
                pnl = (price - pos.entry_price) * pos.shares
                self.realized_pnl += pnl
                for trade in reversed(self.trades):
                    if trade.ticker == ticker and trade.exit_date is None:
                        trade.exit_date = date
                        trade.exit_price = price
                        trade.pnl = pnl
                        break

            for ticker, price, shares in entries:
                if ticker not in self.open_positions:
                    self.open_positions[ticker] = Position(ticker, date, price, shares)
                    self.trades.append(Trade(ticker, date, price, shares))

            unrealized = 0.0
            for ticker, pos in self.open_positions.items():
                px = self.prices.loc[date, ticker]
                unrealized += (px - pos.entry_price) * pos.shares
            self.equity_curve.append({"date": date, "equity": self.realized_pnl + unrealized})

        trades_df = pd.DataFrame([t.__dict__ for t in self.trades])
        equity_df = pd.DataFrame(self.equity_curve).set_index("date")
        return trades_df, equity_df
