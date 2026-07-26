
from pathlib import Path
import json
import pandas as pd
import plotly.graph_objects as go

class ReportBuilder:
    def __init__(self, output_dir='output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_tables(self, trades: pd.DataFrame, equity: pd.DataFrame, metrics: dict):
        trades.to_csv(self.output_dir / 'trades.csv', index=False)
        equity.to_csv(self.output_dir / 'equity_curve.csv')
        pd.DataFrame([metrics]).to_csv(self.output_dir / 'metrics.csv', index=False)

    def build_equity_chart(self, equity: pd.DataFrame, title: str = 'Equity curve'):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=equity.index, y=equity['equity'], mode='lines', fill='tozeroy', name='Equity'))
        fig.update_layout(title=title, showlegend=False)
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Equity')
        chart_path = self.output_dir / 'equity_curve.png'
        fig.write_image(str(chart_path), width=1200, height=700, scale=2)
        with open(str(chart_path) + '.meta.json', 'w') as f:
            json.dump({'caption': title, 'description': 'Equity curve chart'}, f)
