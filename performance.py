
import numpy as np
import pandas as pd

class PerformanceAnalyzer:
    def __init__(self, equity_curve: pd.DataFrame, trades: pd.DataFrame, periods_per_year: int = 252):
        self.equity = equity_curve['equity'].astype(float).copy()
        self.trades = trades.copy()
        self.periods_per_year = periods_per_year

    def returns(self):
        return self.equity.diff().fillna(0.0)

    def total_return(self):
        start = self.equity.iloc[0]
        end = self.equity.iloc[-1]
        if start == 0:
            return np.nan
        return end / start - 1

    def cagr(self):
        shifted = self.equity - self.equity.min() + 1.0
        years = len(shifted) / self.periods_per_year
        if years <= 0:
            return np.nan
        return shifted.iloc[-1] ** (1 / years) - 1

    def volatility(self):
        rets = self.returns()
        std = rets.std()
        if std == 0 or np.isnan(std):
            return 0.0
        return std * np.sqrt(self.periods_per_year)

    def sharpe(self, risk_free_rate: float = 0.0):
        rets = self.returns()
        rf = risk_free_rate / self.periods_per_year
        excess = rets - rf
        std = excess.std()
        if std == 0 or np.isnan(std):
            return 0.0
        return excess.mean() / std * np.sqrt(self.periods_per_year)

    def drawdown_series(self):
        shifted = self.equity - self.equity.min() + 1.0
        peak = shifted.cummax()
        return shifted / peak - 1

    def max_drawdown(self):
        return self.drawdown_series().min()

    def win_rate(self):
        closed = self.trades.dropna(subset=['pnl']) if 'pnl' in self.trades.columns else self.trades.iloc[0:0]
        if len(closed) == 0:
            return np.nan
        return (closed['pnl'] > 0).mean()

    def trade_count(self):
        closed = self.trades.dropna(subset=['pnl']) if 'pnl' in self.trades.columns else self.trades.iloc[0:0]
        return len(closed)

    def summary(self):
        return {
            'trade_count': self.trade_count(),
            'win_rate': self.win_rate(),
            'cagr': self.cagr(),
            'volatility': self.volatility(),
            'sharpe': self.sharpe(),
            'max_drawdown': self.max_drawdown(),
        }
