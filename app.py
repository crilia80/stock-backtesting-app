
import streamlit as st
import pandas as pd

from config import BacktestConfig
from data_loader import DataLoader
from engine import BacktestEngine
from performance import PerformanceAnalyzer
from reporting import ReportBuilder
from strategies.rotation_52w import Rotation52WeekStrategy
from strategies.sma_crossover import SMACrossoverStrategy
from strategies.buy_and_hold import BuyAndHoldStrategy
from strategies.rotation_52w_target_profit import Rotation52WeekTargetProfitStrategy

st.set_page_config(page_title="Backtesting Acțiuni US", layout="wide")
st.title("Backtesting strategii - acțiuni listate în SUA")

st.sidebar.header("Configurare backtest")

tickers_input = st.sidebar.text_input(
    "Simboluri companii (separate prin virgulă)",
    value="MSFT, AAPL, XOM, MCD, MA"
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

start_date = st.sidebar.date_input("Data de start", value=pd.Timestamp.today() - pd.DateOffset(years=10))
end_date = st.sidebar.date_input("Data de final", value=pd.Timestamp.today())

allocation = st.sidebar.number_input("Suma investită per poziție (USD)", value=1000.0, step=100.0)

strategy_name = st.sidebar.selectbox(
   "Strategie",
    ["Rotatie 52 saptamani (low/high)", "Rotatie 52 saptamani + Profit tinta", "Crossover medii mobile (SMA)", "Buy & Hold"]
)

if strategy_name == "Rotatie 52 saptamani (low/high)":
    window = st.sidebar.number_input("Fereastra (zile de tranzactionare)", value=252, step=1)
elif strategy_name == "Rotatie 52 saptamani + Profit tinta":
    window = st.sidebar.number_input("Fereastra (zile de tranzactionare)", value=252, step=1)
    target_profit_pct = st.sidebar.number_input("Profit tinta (%)", value=100.0, step=10.0, min_value=10.0)
elif strategy_name == "Crossover medii mobile (SMA)":
    fast_window = st.sidebar.number_input("SMA rapida (zile)", value=20, step=1)
    slow_window = st.sidebar.number_input("SMA lenta (zile)", value=50, step=1)

run_button = st.sidebar.button("Ruleaza backtest")

if run_button:
    if not tickers:
        st.error("Introdu cel putin un simbol de companie.")
        st.stop()

    config = BacktestConfig(
        tickers=tickers,
        start=str(start_date),
        end=str(end_date),
        allocation_per_trade=float(allocation),
    )

    with st.spinner("Descarc date istorice..."):
        prices = DataLoader(config).load_close_prices()

    if prices.empty:
        st.error("Nu am gasit date pentru simbolurile introduse. Verifica simbolurile.")
        st.stop()

    if strategy_name == "Rotatie 52 saptamani (low/high)":
        strategy = Rotation52WeekStrategy(prices, allocation_per_trade=config.allocation_per_trade, window=int(window))
    elif strategy_name == "Rotatie 52 saptamani + Profit tinta":
        strategy = Rotation52WeekTargetProfitStrategy(
            prices,
            allocation_per_trade=config.allocation_per_trade,
            window=int(window),
            target_profit_pct=float(target_profit_pct) / 100.0,
        )
    elif strategy_name == "Crossover medii mobile (SMA)":
        strategy = SMACrossoverStrategy(prices, allocation_per_trade=config.allocation_per_trade,
                                         fast_window=int(fast_window), slow_window=int(slow_window))
    else:
        strategy = BuyAndHoldStrategy(prices, allocation_per_trade=config.allocation_per_trade)

    with st.spinner("Rulez simularea..."):
        engine = BacktestEngine(prices, strategy)
        trades, equity = engine.run()
        metrics = PerformanceAnalyzer(equity, trades).summary()

    st.subheader("Rezultate")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Tranzactii", metrics["trade_count"])
    col2.metric("Win rate", f"{metrics['win_rate']*100:.1f}%" if pd.notna(metrics["win_rate"]) else "N/A")
    col3.metric("CAGR", f"{metrics['cagr']*100:.1f}%" if pd.notna(metrics["cagr"]) else "N/A")
    col4.metric("Sharpe", f"{metrics['sharpe']:.2f}")
    col5.metric("Max Drawdown", f"{metrics['max_drawdown']*100:.1f}%" if pd.notna(metrics["max_drawdown"]) else "N/A")

    st.subheader("Curba de capital (Equity Curve)")
    st.line_chart(equity["equity"])

    st.subheader("Tranzactii")
    st.dataframe(trades, use_container_width=True)

    report = ReportBuilder(output_dir="output")
    report.save_tables(trades, equity, metrics)

    st.success("Backtest finalizat. Rezultatele au fost salvate in folderul output/.")
else:
    st.info("Configureaza parametrii din stanga si apasa 'Ruleaza backtest'.")
