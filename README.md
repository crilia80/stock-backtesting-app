# Backtesting Framework

Framework Python reutilizabil pentru backtesting pe acțiuni SUA, date zilnice, cu strategii plug-in.

## Structură
- `config.py` — configurația backtestului
- `data_loader.py` — descărcare date cu yfinance
- `engine.py` — motor generic de backtesting
- `models.py` — modele pentru poziții și tranzacții
- `performance.py` — metrici de performanță (Sharpe, CAGR, volatility, max drawdown, win rate)
- `reporting.py` — export tabele și chart equity curve
- `strategies/base.py` — interfața de bază pentru strategii
- `strategies/rotation_52w.py` — implementarea strategiei 52w low/high
- `strategies/sma_crossover.py` — strategie generică SMA crossover
- `strategies/buy_and_hold.py` — benchmark simplu
- `run_backtest.py` — exemplu de rulare end-to-end

## Principii
- o singură poziție per ticker
- poziții simultane permise pe tickere diferite
- sumă fixă investită per entry
- strategii extensibile prin moștenire din `BaseStrategy`
- metrici standard de performanță și raportare exportabilă


## Interfata grafica (Streamlit)

Aplicatia are si o interfata grafica simpla, construita cu Streamlit, in fisierul `app.py`.

### Instalare si rulare locala

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se va deschide o pagina in browser unde poti:
- introduce simbolurile companiilor (ex: MSFT, AAPL, XOM, MCD, MA)
- alege intervalul de testare
- alege suma investita per pozitie
- alege strategia (Rotatie 52 saptamani, Crossover SMA, Buy & Hold) si parametrii ei
- vedea rezultatele: numar tranzactii, win rate, CAGR, Sharpe, max drawdown, curba de capital si tabelul de tranzactii
