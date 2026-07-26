
from config import BacktestConfig
from data_loader import DataLoader
from engine import BacktestEngine
from performance import PerformanceAnalyzer
from reporting import ReportBuilder
from strategies.rotation_52w import Rotation52WeekStrategy
from strategies.sma_crossover import SMACrossoverStrategy
from strategies.buy_and_hold import BuyAndHoldStrategy

STRATEGY = 'rotation_52w'

config = BacktestConfig(
    tickers=['MSFT', 'AAPL', 'XOM', 'MCD', 'MA'],
    start='2016-07-25',
    end='2026-07-25',
    allocation_per_trade=1000.0,
)

prices = DataLoader(config).load_close_prices()

if STRATEGY == 'rotation_52w':
    strategy = Rotation52WeekStrategy(prices, allocation_per_trade=config.allocation_per_trade, window=252)
elif STRATEGY == 'sma_crossover':
    strategy = SMACrossoverStrategy(prices, allocation_per_trade=config.allocation_per_trade, fast_window=20, slow_window=50)
elif STRATEGY == 'buy_and_hold':
    strategy = BuyAndHoldStrategy(prices, allocation_per_trade=config.allocation_per_trade)
else:
    raise ValueError('Strategie necunoscuta')

engine = BacktestEngine(prices, strategy)
trades, equity = engine.run()
metrics = PerformanceAnalyzer(equity, trades).summary()

report = ReportBuilder(output_dir='output')
report.save_tables(trades, equity, metrics)
report.build_equity_chart(equity, title=f'Equity curve - {STRATEGY}')
print(metrics)
