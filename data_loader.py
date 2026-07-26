import yfinance as yf
import pandas as pd
from config import BacktestConfig

class DataLoader:
    def __init__(self, config: BacktestConfig):
        self.config = config

    def load_close_prices(self) -> pd.DataFrame:
        data = yf.download(
            self.config.tickers,
            start=self.config.start,
            end=self.config.end,
            auto_adjust=self.config.auto_adjust,
            progress=False,
        )["Close"]
        if isinstance(data, pd.Series):
            data = data.to_frame()
        return data.dropna(how="all")
